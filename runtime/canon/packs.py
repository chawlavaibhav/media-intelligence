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

Injection v1 (Controller ruling C-10, 14 Sep 2026: "Authorise USD-0 implementation of: Canon
Injection v1; template / empirical-memory integration."): the system block is the receipt-free
runtime/canon/INJECTION-PREFIX-v1.md, read by default. CANON-SHAPE-v1 §5 retired the forced-
consumption receipts ("The gate verifies mechanically; the model writes the plan only"), so the
block no longer asks for DOCTRINE_DEVIATIONS or per-check pass/fix lines. The v0 block in
canon/compilation/INJECTION-CONTRACT-v0.md §2 is not edited and stays selectable
(injection_version="v0") so a test can prove that path is byte-for-byte unchanged.

The prefix — system block, then (audio only) the coverage-gap notice, then the accepted packs'
terse text in canonical order — is the cache-served part of the prompt. Nothing request-specific
is in it: two jobs that select the same packs get byte-identical prefixes and one prefix_sha256.
The volatile Normalized Request begins after CACHE_BOUNDARY_MARKER, which is metadata about the
boundary and is never itself injected. Cache-read pricing is not pinned (CANON-SHAPE-v1 §6).
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

INJECTION_VERSIONS = ("v0", "v1")
DEFAULT_INJECTION_VERSION = "v1"
# Documents where the stable prefix ends and the volatile Normalized Request begins
# (COMPILED-PACK-CONTRACT-v0.1 §4). Recorded on the lookup as metadata; NEVER placed in the payload.
CACHE_BOUNDARY_MARKER = (
    "<<CANON_CACHE_BREAKPOINT: everything upstream is the byte-stable Canon prefix "
    "(system block + accepted packs); the Normalized Request begins downstream>>"
)
CACHE_PRICING_NOT_PINNED = "not pinned"
CACHE_PRICING_NOTE = (
    "cache-read pricing is not pinned (canon/CANON-SHAPE-v1.md §6: 'cache-read pricing, to be "
    "pinned'); no cost figure in this runtime rests on a cache-read rate"
)
# The v0 receipt vocabulary CANON-SHAPE-v1 §5 retired. Scanned for, never injected by the runtime.
RECEIPT_VOCABULARY = ("FAILURE_PREVENTION", "DOCTRINE_DEVIATIONS")


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
    # Injection v1 metadata (CANON-SHAPE-v1 §4-§6). Defaults keep older positional callers working.
    injection_version: str = DEFAULT_INJECTION_VERSION
    prefix_sha256: str = ""                 # sha over exactly the bytes upstream of the breakpoint
    cache_boundary_marker: str = CACHE_BOUNDARY_MARKER
    cache_pricing: str = CACHE_PRICING_NOT_PINNED
    cache_pricing_note: str = CACHE_PRICING_NOTE
    receipts_required: bool = False

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
        injection_version: str = DEFAULT_INJECTION_VERSION,
        injection_prefix_v1_path: str | Path | None = None,
    ):
        if injection_version not in INJECTION_VERSIONS:
            raise Refusal(
                Refusal.CANON_TRIGGER_TABLE_HOLE,
                f"no injection block exists for version {injection_version!r}",
                known=list(INJECTION_VERSIONS),
            )
        self.compilation_dir = Path(compilation_dir or paths.CANON_COMPILATION)
        self.triggers_path = str(triggers_path or paths.CANON_TRIGGERS)
        self.injection_contract_path = str(injection_contract_path or paths.CANON_INJECTION_CONTRACT)
        self.injection_prefix_v1_path = str(injection_prefix_v1_path or paths.INJECTION_PREFIX_V1)
        self.corpus_index_path = str(corpus_index_path or paths.CANON_CORPUS_INDEX)
        self.injection_version = injection_version
        self.triggers = load_yaml(self.triggers_path) or {}
        self.accepted_digest = self._accepted_digest()
        self.packs = self._load_packs()
        # v0: the receipt-bearing block of INJECTION-CONTRACT-v0 §2 (canon-owned, read verbatim).
        # v1: the receipt-free block of runtime/canon/INJECTION-PREFIX-v1.md (runtime-owned).
        self.system_prompt_block_v0 = self._fenced_block(self.injection_contract_path, "INJECTION-CONTRACT-v0 §2")
        self.system_prompt_block_v1 = self._fenced_block(self.injection_prefix_v1_path, "INJECTION-PREFIX-v1")
        self.system_prompt_block = (
            self.system_prompt_block_v1 if injection_version == "v1" else self.system_prompt_block_v0
        )

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

    @staticmethod
    def _fenced_block(path: str, label: str) -> str:
        """The invariant system block: the FIRST fenced block of the named file, read verbatim."""
        match = _FENCE.search(read_text(path))
        if not match:
            raise Refusal(
                Refusal.CANON_TRIGGER_TABLE_HOLE,
                f"{label} has no fenced system-prompt block to inject",
                source=path,
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

        # OBSERVED 14 Sep 2026: the compiled packs' own terse text still opens with the v0 receipt
        # sentence. The runtime never rewrites pack bytes (render by id, never paraphrase), so under
        # v1 it records which packs carry the retired vocabulary instead of pretending it is gone.
        if self.injection_version == "v1":
            carrying = [
                p for p in injected
                if any(word in self.packs[p].terse_injection_text for word in RECEIPT_VOCABULARY)
            ]
            if carrying:
                notices.append(
                    "receipt vocabulary retired by CANON-SHAPE-v1 §5 is still carried by the "
                    f"canon-owned pack text of {', '.join(carrying)}; the runtime does not require "
                    "receipts and the gate does not read them"
                )

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
            injection_version=self.injection_version,
            # In v1 the whole payload is the prefix: identical bytes to injected_context_sha256,
            # named again under CANON-SHAPE-v1's cache vocabulary so a consumer can find it.
            prefix_sha256=sha256_text(payload),
            cache_boundary_marker=CACHE_BOUNDARY_MARKER,
            cache_pricing=CACHE_PRICING_NOT_PINNED,
            cache_pricing_note=CACHE_PRICING_NOTE,
            receipts_required=self.injection_version == "v0",
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
