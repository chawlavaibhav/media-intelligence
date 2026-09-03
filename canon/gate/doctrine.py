"""Render-by-id registry of the 21 committed check lines (CANON-GATE-001 plan §B doctrine.py).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

The registry is loaded from the two committed packs at runtime; no check text lives here.
Loading fails closed: a pack whose check_id is not `<decision_id>-check`, whose decision
count is not the committed 10/11, whose Devanagari limit line is missing, or which carries
any id-shaped token resolving under canon/candidates/ (the HOLD lane) is refused. The HOLD
scan reuses the id regex of canon/validation/validate_compiled_pack.py check (9); the full
validator (closure, markers, digests, ~15 s) is offered by the CLI's --validate-packs, not
run here.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
from dataclasses import dataclass

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK_PATHS = [
    ROOT / "canon/compilation/PACK-product_appearance-v0.yaml",
    ROOT / "canon/compilation/PACK-composition_and_attention-v0.yaml",
]
CANDIDATES = ROOT / "canon/candidates"
TRIGGERS = ROOT / "canon/packs/pack-triggers-v0.yaml"

# Identical to the pack-file scan in validate_compiled_pack.validate_pack check (9).
ID_TOKEN_RE = re.compile(r"\b(?:sk|scs)_[a-z0-9_]+\b")
EXPECTED_DECISIONS = {"product_appearance": 10, "composition_and_attention": 11}
DEVANAGARI_MARK = "never generate Devanagari glyphs"
PRODUCT_CONDITION = "product_or_packshot_entity_present"

# Modality scope per check line (plan §B): CA-D7/8/9 are cut decisions (video and
# image_sequence); CA-D10/11 are shot-length and camera-move decisions (video only).
ALL_MODALITIES = ("static_image", "video", "image_sequence")
MODALITY_SCOPE = {
    "CA-D7-check": ("video", "image_sequence"),
    "CA-D8-check": ("video", "image_sequence"),
    "CA-D9-check": ("video", "image_sequence"),
    "CA-D10-check": ("video",),
    "CA-D11-check": ("video",),
}


class RegistryError(Exception):
    """The registry refuses to load — fail closed."""


@dataclass(frozen=True)
class CheckLine:
    check_id: str
    decision_id: str
    pack_id: str
    text: str
    feeds_sections: tuple
    question: str


@dataclass(frozen=True)
class PackInfo:
    pack_id: str
    path: pathlib.Path
    sha256: str
    modalities: tuple
    limits: tuple


@dataclass
class Registry:
    checks: dict          # check_id -> CheckLine, in pack order
    packs: dict           # pack_id -> PackInfo
    limit_text: str       # the verbatim Devanagari limit line (LIMIT-TEXT source)
    triggers: dict        # the trigger table document

    def checks_by_pack(self) -> list:
        """Pack ids in registry (pack file) order."""
        return list(dict.fromkeys(line.pack_id for line in self.checks.values()))

    def select_packs(self, modality: str, product_entity: bool) -> list:
        """Mirror canon/packs/pack-triggers-v0.yaml, restricted to the compiled packs."""
        bases = self.triggers.get("modality_base_packs") or {}
        if modality not in bases:
            raise RegistryError(f"unknown modality {modality!r}; the trigger table knows "
                                f"{sorted(bases)}")
        chosen = list(bases[modality] or [])
        if product_entity:
            for c in self.triggers.get("conditional_packs") or []:
                if c.get("condition") == PRODUCT_CONDITION:
                    chosen.append(c.get("pack"))
        # A pack applies only to the modalities its own `applicability` names (audio → none).
        return [p for p in chosen if p in self.packs and modality in self.packs[p].modalities]

    def applicable(self, check_id: str, modality: str) -> bool:
        if modality not in ALL_MODALITIES:
            return False
        return modality in MODALITY_SCOPE.get(check_id, ALL_MODALITIES)

    def applicability_reason(self, check_id: str, modality: str) -> str:
        line = self.checks[check_id]
        scope = MODALITY_SCOPE.get(check_id, ALL_MODALITIES)
        return (f"{line.decision_id} is a {'/'.join(scope)} decision ('{line.question}') — "
                f"not applicable to {modality}")


def candidate_ids(candidates_dir: pathlib.Path = CANDIDATES) -> set:
    """Every sk_/scs_ id under canon/candidates/ — the HOLD lane, read dynamically."""
    ids = set()
    for p in candidates_dir.rglob("source-knowledge.yaml"):
        for o in (yaml.safe_load(p.read_text()) or {}).get("source_knowledge") or []:
            ids.add(o.get("sk_id"))
    for p in candidates_dir.rglob("source-concept-systems.yaml"):
        for s in (yaml.safe_load(p.read_text()) or {}).get("source_concept_systems") or []:
            ids.add(s.get("scs_id"))
    ids.discard(None)
    return ids


def load_registry(pack_paths=PACK_PATHS, candidates_dir: pathlib.Path = CANDIDATES,
                  triggers_path: pathlib.Path = TRIGGERS) -> Registry:
    hold = candidate_ids(candidates_dir)
    checks: dict = {}
    packs: dict = {}
    limit_lines = []
    for path in pack_paths:
        path = pathlib.Path(path)
        if not path.exists():
            raise RegistryError(f"{path.name}: pack missing")
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        found = sorted(t for t in set(ID_TOKEN_RE.findall(text)) if t in hold)
        if found:
            raise RegistryError(f"{path.name}: HOLD-lane id(s) {found} resolve under "
                                f"{candidates_dir.name}/ — fail closed")
        pack = yaml.safe_load(text) or {}
        pack_id = pack.get("pack_id")
        if pack_id not in EXPECTED_DECISIONS:
            raise RegistryError(f"{path.name}: unknown pack_id {pack_id!r}")
        decisions = pack.get("decisions") or []
        if len(decisions) != EXPECTED_DECISIONS[pack_id]:
            raise RegistryError(f"{path.name}: {len(decisions)} decisions, expected "
                                f"{EXPECTED_DECISIONS[pack_id]}")
        for d in decisions:
            did = d.get("decision_id")
            cid = d.get("check_id")
            if cid != f"{did}-check":
                raise RegistryError(f"{path.name}: {did}: check_id is {cid!r}, expected "
                                    f"'{did}-check'")
            if cid in checks:
                raise RegistryError(f"{path.name}: duplicate check_id {cid}")
            check_text = str(d.get("check") or "").strip()
            if not check_text:
                raise RegistryError(f"{path.name}: {did}: `check` is empty")
            checks[cid] = CheckLine(
                check_id=cid, decision_id=did, pack_id=pack_id, text=d["check"],
                feeds_sections=tuple(d.get("feeds_sections") or ()),
                question=str(d.get("question") or ""))
        limits = tuple(pack.get("pack_limits") or ())
        dev = [l for l in limits if DEVANAGARI_MARK in l]
        if len(dev) != 1:
            raise RegistryError(f"{path.name}: Devanagari limit line missing or duplicated")
        limit_lines.append(dev[0])
        packs[pack_id] = PackInfo(
            pack_id=pack_id, path=path, sha256=hashlib.sha256(raw).hexdigest(),
            modalities=tuple((pack.get("applicability") or {}).get("modalities") or ()),
            limits=limits)
    if len(set(limit_lines)) != 1:
        raise RegistryError("the packs disagree on the Devanagari limit line — fail closed")
    if set(packs) != set(EXPECTED_DECISIONS):
        raise RegistryError(f"expected packs {sorted(EXPECTED_DECISIONS)}, loaded {sorted(packs)}")
    triggers = yaml.safe_load(pathlib.Path(triggers_path).read_text()) or {}
    return Registry(checks=checks, packs=packs, limit_text=limit_lines[0], triggers=triggers)
