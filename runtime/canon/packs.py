"""The deterministic Canon pack lookup of CANON-SHAPE-v1 §4.

What this is:
  Normalized Request -> pack ids (a table lookup in canon/packs/pack-triggers-v0.yaml)
  -> the matching ACCEPTED COMPILED packs' bytes, concatenated in canonical order
  -> one sha256 over exactly those bytes.

What this is deliberately not:
  no free-form retrieval; no model deciding whether to consult Canon (the self-diagnosis trap
  that produced EVAL-037's 0/18); no HOLD material; no Q&A corpus. A trigger that fires with no
  compiled pack sets canon_gap and the job CONTINUES — a missing pack never blocks a job and
  never starts a compilation programme.

"Accepted" is mechanical, not a label: a compiled pack is injectable only if its corpus_digest
equals fingerprints.accepted_canon.combined_digest in canon/knowledge/CANON-CORPUS-INDEX.yaml.
HOLD candidates are not in that fingerprint, so they cannot reach a prompt through this path.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .. import paths
from ..errors import Refusal
from ..util import load_yaml, read_text, sha256_text, token_estimate

UNIVERSAL = "universal"
_FENCE = re.compile(r"^```\n(.*?)^```", re.S | re.M)


@dataclass(frozen=True)
class CompiledPack:
    pack_id: str
    path: str
    corpus_digest: str
    terse_injection_text: str
    check_ids: tuple
    pack_limits: tuple
    accepted: bool
    acceptance_reason: str


@dataclass(frozen=True)
class PackSelection:
    pack_id: str
    trigger: str
    status: str            # compiled_accepted | selected_uncompiled
    order_index: int

    def as_contract_row(self) -> dict:
        # PRODUCTION-SPEC-v0.canon.packs_selected: pack_id, trigger id, compiled|uncompiled
        return {
            "pack_id": self.pack_id,
            "trigger": self.trigger,
            "compiled": self.status == "compiled_accepted",
            "status": self.status,
        }


@dataclass(frozen=True)
class CanonLookup:
    selections: tuple
    injected_pack_ids: tuple
    gap_pack_ids: tuple
    payload: str
    injected_context_sha256: str
    canon_gap: bool
    missing_domain: str | None
    check_ids: tuple
    pack_limits: tuple
    tokens: int
    notices: tuple

    def packs_selected(self) -> list:
        return [s.as_contract_row() for s in self.selections]


class CanonCorpus:
    """Compiled packs on disk, plus the invariant system-prompt block they ride behind."""

    def __init__(
        self,
        compilation_dir: str | Path | None = None,
        triggers_path: str | Path | None = None,
        injection_contract_path: str | Path | None = None,
        corpus_index_path: str | Path | None = None,
    ):
        self.compilation_dir = Path(compilation_dir or paths.CANON_COMPILATION)
        self.triggers_path = str(triggers_path or paths.CANON_TRIGGERS)
        self.injection_contract_path = str(injection_contract_path or paths.CANON_INJECTION_CONTRACT)
        self.corpus_index_path = str(corpus_index_path or paths.CANON_CORPUS_INDEX)
        self.triggers = load_yaml(self.triggers_path) or {}
        self.accepted_digest = self._accepted_digest()
        self.packs = self._load_packs()
        self.system_prompt_block = self._system_prompt_block()

    # ---------------------------------------------------------------- loading
    def _accepted_digest(self) -> str:
        index = load_yaml(self.corpus_index_path) or {}
        return ((index.get("fingerprints") or {}).get("accepted_canon") or {}).get("combined_digest", "")

    def _load_packs(self) -> dict:
        out: dict[str, CompiledPack] = {}
        for path in sorted(self.compilation_dir.glob("PACK-*-v0.yaml")):
            doc = load_yaml(path) or {}
            pack_id = doc.get("pack_id")
            terse = doc.get("terse_injection_text") or ""
            digest = doc.get("corpus_digest") or ""
            accepted = bool(terse) and digest == self.accepted_digest and bool(self.accepted_digest)
            reason = (
                "corpus_digest == fingerprints.accepted_canon.combined_digest"
                if accepted
                else "corpus_digest does not match the accepted-Canon fingerprint, or no terse rendering"
            )
            out[pack_id] = CompiledPack(
                pack_id=pack_id,
                path=str(path),
                corpus_digest=digest,
                terse_injection_text=terse,
                check_ids=tuple(d.get("check_id") for d in doc.get("decisions", []) if d.get("check_id")),
                pack_limits=tuple(doc.get("pack_limits", []) or []),
                accepted=accepted,
                acceptance_reason=reason,
            )
        return out

    def _system_prompt_block(self) -> str:
        """The ~340-token invariant prefix, read verbatim from INJECTION-CONTRACT-v0 §2."""
        text = read_text(self.injection_contract_path)
        match = _FENCE.search(text)
        if not match:
            raise Refusal(
                Refusal.CANON_TRIGGER_TABLE_HOLE,
                "INJECTION-CONTRACT-v0 §2 has no fenced system-prompt block to inject",
                source=self.injection_contract_path,
            )
        return match.group(1)

    # ---------------------------------------------------------------- selection
    def select(self, nr) -> list:
        """NR -> pack ids, strictly by the trigger table. No judgment anywhere in here."""
        triggers = self.triggers
        base_sets = triggers.get("modality_base_packs", {})
        if nr.modality not in base_sets:
            raise Refusal(
                Refusal.CANON_TRIGGER_TABLE_HOLE,
                f"the trigger table has no base pack set for modality {nr.modality!r}",
                modality=nr.modality,
                table=self.triggers_path,
            )
        rows: list[tuple] = []
        for pack in triggers.get("universal_packs", []):
            rows.append((pack, UNIVERSAL))

        uncertainty = triggers.get("uncertainty_rule") or {}
        provenance = (nr.specification_provenance or {}).get("modality")
        union_fires = bool(uncertainty) and provenance == "customer_implied" and bool(nr.ambiguity_markers)
        if union_fires:
            union: list[str] = []
            for modality in _union_modalities(uncertainty):
                union.extend(base_sets.get(modality, []))
            for pack in _stable(union):
                rows.append((pack, f"uncertainty_rule:union({','.join(_union_modalities(uncertainty))})"))
        else:
            for pack in base_sets[nr.modality]:
                rows.append((pack, f"base:{nr.modality} (R05)"))

        for cond in triggers.get("conditional_packs", []):
            if _conditional_fires(cond["condition"], nr):
                rows.append((cond["pack"], f"{cond['condition']} ({cond.get('nr_field')})"))

        selections = []
        seen = set()
        for index, (pack_id, trigger) in enumerate(rows):
            if pack_id in seen:
                continue
            seen.add(pack_id)
            pack = self.packs.get(pack_id)
            status = "compiled_accepted" if (pack and pack.accepted) else "selected_uncompiled"
            selections.append(PackSelection(pack_id=pack_id, trigger=trigger, status=status, order_index=index))
        return selections

    # ---------------------------------------------------------------- injection
    def inject(self, nr) -> CanonLookup:
        selections = self.select(nr)
        parts = [self.system_prompt_block]
        notices = []
        gap_notice = self.triggers.get("coverage_gap_notice")
        if not self.triggers.get("modality_base_packs", {}).get(nr.modality) and gap_notice:
            # a modality with zero packs carries its coverage-gap notice verbatim, never silence
            notices.append(gap_notice)
            parts.append(gap_notice)

        injected, gaps, checks, limits = [], [], [], []
        for selection in selections:
            pack = self.packs.get(selection.pack_id)
            if pack and pack.accepted:
                injected.append(selection.pack_id)
                parts.append(pack.terse_injection_text)
                checks.extend(pack.check_ids)
                limits.extend(pack.pack_limits)
            else:
                gaps.append(selection.pack_id)

        payload = "\n\n".join(parts)
        tokens = token_estimate(payload)
        ceiling = self.triggers.get("per_request_max_tokens")
        if ceiling is not None and tokens > ceiling:
            raise Refusal(
                Refusal.CANON_BUDGET_EXCEEDED,
                "the injected Canon payload exceeds the trigger table's per-request token bound",
                tokens=tokens,
                per_request_max_tokens=ceiling,
            )

        return CanonLookup(
            selections=tuple(selections),
            injected_pack_ids=tuple(injected),
            gap_pack_ids=tuple(gaps),
            payload=payload,
            injected_context_sha256=sha256_text(payload),
            canon_gap=bool(gaps),
            # A trigger fired that no compiled pack answers. The job continues; this is the
            # record of what was missing when it did.
            missing_domain=", ".join(sorted(gaps)) if gaps else None,
            check_ids=tuple(checks),
            pack_limits=tuple(_stable(limits)),
            tokens=tokens,
            notices=tuple(notices),
        )


def lookup(nr, corpus: CanonCorpus | None = None) -> CanonLookup:
    return (corpus or CanonCorpus()).inject(nr)


def _union_modalities(rule: dict) -> list:
    action = str(rule.get("action", ""))
    found = re.search(r"\[([^\]]+)\]", action)
    if not found:
        return []
    return [m.strip() for m in found.group(1).split(",") if m.strip()]


def _conditional_fires(condition: str, nr) -> bool:
    """The four conditional triggers, each keyed to an NR field and never to model judgment."""
    if condition == "text_requirements_nonempty":
        return bool(nr.text_requirements)
    if condition == "product_or_packshot_entity_present":
        return bool(nr.facets.get("product_entity_present"))
    if condition == "language_topology_present_or_market_IN":
        return bool(nr.language_topology) or str(nr.market or "").upper() == "IN"
    if condition == "advertising_acceptance_intent":
        return bool((nr.acceptance_intent or {}).get("advertising"))
    raise Refusal(
        Refusal.CANON_TRIGGER_TABLE_HOLE,
        f"the trigger table names a conditional {condition!r} this runtime cannot evaluate",
        condition=condition,
    )


def _stable(items):
    seen, out = set(), []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out
