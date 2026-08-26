#!/usr/bin/env python3
"""Derive the three independent lineage keys for a committed manifest record.

THE WHOLE POINT OF THIS MODULE
Deduplication by file hash is the check everyone reaches for, and on this corpus it is the check
that would have missed the most important problem. Three DIFFERENT things can make two items
non-independent, and only the first is visible to a hash:

  1. BYTE IDENTITY   - the same file. Caught by SHA-256.
  2. CONTENT LINEAGE - different bytes, same underlying content. A crop of a photograph shares no
                       bytes with its parent, but scoring both is scoring the same signage twice.
  3. SOURCE LINEAGE  - different content, same collection/lab/derivative ancestry. IndicSTR12 and
                       IIIT-ILST are different files of different regions from the same lab's
                       overlapping collection effort.

Verified on this corpus (cloud session, 26 Aug 2026, from the committed manifest):
  * 173 byte-identical files across the two CVIT sources, ALL of them scene photographs;
  * 1,205 of IIIT-ILST's 1,214 crops descend from photographs shared with IndicSTR12, sharing
    NO bytes with them - invisible to any hash check;
  * both CVIT sources belong to one source lineage.

If independence is enforced at level 1 only, a "clean" holdout can be 99% contaminated.
"""
import os

# --- Level 3: source lineage --------------------------------------------------------------------
# Sources sharing a lineage id are NOT independent of each other, whatever their file hashes say.
SOURCE_LINEAGE = {
    "src_indicstr12_devanagari": "lin_cvit_iiit_hyderabad",
    "src_iiit_ilst_devanagari":  "lin_cvit_iiit_hyderabad",   # <- same lineage, deliberately
    "src_bstd_devanagari":       "lin_bhashini_iitj",
    "src_imagerewarddb":         "lin_diffusiondb_imagereward",
    "src_konvid1k":              "lin_konstanz_yfcc100m",
    "src_videofeedback":         "lin_tigerlab_videofeedback",
    "src_videogen_rewardbench":  "lin_kwaivgi_videogen",
    "src_youtube_ugc":           "lin_google_youtube_ugc",
}

LINEAGE_NOTES = {
    "lin_cvit_iiit_hyderabad": (
        "IndicSTR12 + IIIT-ILST. ONE lineage. 173 byte-identical scene photographs (98.3% of "
        "IIIT-ILST's scene set) and 1,205/1,214 of its crops descend from shared parents. Never "
        "hold one out against the other."),
    "lin_bhashini_iitj": (
        "BSTD. The only Devanagari lineage independent of CVIT. The genuine cross-lineage reserve "
        "candidate. NOTE: its own train/test split is not a safe boundary - 2 duplicate hash pairs "
        "cross it."),
    "lin_konstanz_yfcc100m": (
        "KoNViD-1k, sampled from YFCC100M for DEGRADATION variety. Shares an upstream population "
        "with other YFCC100M-derived datasets; if such a dataset is ever acquired, it joins this "
        "lineage rather than forming a new one."),
    "lin_diffusiondb_imagereward": "ImageRewardDB, images collected from DiffusionDB.",
    "lin_tigerlab_videofeedback": "VideoFeedback. Source generators are NOT named by the publisher.",
    "lin_kwaivgi_videogen": "VideoGen-RewardBench, 12 named generators, 24 clips each.",
    "lin_google_youtube_ugc": "YouTube-UGC, CC BY 4.0 with per-item attribution. Audio removed.",
}


UNKNOWN_LINEAGE_PREFIX = "lin_unknown::"


def source_lineage_key(rec):
    """Level 3. Unknown sources get an explicit unknown marker, never a silent default.

    R-C4: the marker is deliberately keyed on the source id so it is TRACEABLE, but a caller must
    NEVER read two different lin_unknown:: keys as two independent lineages. Two unregistered sources
    that happen to have different ids may well be the same lab, the same collection effort, or one
    derived from the other - nothing in the id says otherwise. `is_unknown_lineage` exists so callers
    detect this case explicitly instead of comparing keys and concluding "different, therefore
    independent", which is how an unregistered source silently gets certified as a clean holdout.
    """
    return SOURCE_LINEAGE.get(rec["source_id"], f"{UNKNOWN_LINEAGE_PREFIX}{rec['source_id']}")


def is_unknown_lineage(key):
    """True when a lineage key means 'not established', not 'a distinct lineage'."""
    return str(key).startswith(UNKNOWN_LINEAGE_PREFIX)


def byte_key(rec):
    """Level 1. Exact file identity."""
    return rec["sha256"]


def content_key(rec):
    """Level 2. The underlying content an item depicts.

    For the two CVIT sources the crop filename encodes its parent photograph, so a crop and its
    parent resolve to the same content key. Crucially the key is built from the PARENT'S BYTE HASH
    where the parent is known, so that the 173 photographs shared across the two sources collapse
    into one content group - which is what makes the 1,205 derived crops visible as non-independent.

    Any item whose content ancestry cannot be established returns a key derived from its own
    identity. That is correct-by-default: it means 'independent as far as we can tell', and it is
    the caller's job to treat an unresolved key as unproven rather than proven.
    """
    return rec.get("_content_key") or f"content::self::{rec['sha256']}"


def build_content_index(records):
    """Resolve content keys across the whole manifest and annotate records in place.

    Returns a dict of diagnostics so a caller can report how much ancestry was actually resolved
    rather than assuming it all was.
    """
    by_name = {}
    for r in records:
        by_name.setdefault(r["source_id"], {})[os.path.basename(r["relative_path"])] = r

    # Canonical hash for each CVIT scene photograph, keyed (source, scene id).
    scene_hash = {}
    for r in records:
        sid = r["source_id"]
        n = os.path.basename(r["relative_path"])
        if sid == "src_iiit_ilst_devanagari" and "__cropped__" not in n:
            scene_hash[(sid, n.split("__Devanagari__")[1].rsplit(".", 1)[0])] = r["sha256"]
        elif sid == "src_indicstr12_devanagari" and "__cropped_images__" not in n:
            parts = n.rsplit(".", 1)[0].split("__")
            if len(parts) >= 3:
                scene_hash[(sid, parts[1] + "/" + parts[2])] = r["sha256"]

    resolved = unresolved = 0
    orphan_parents = set()
    for r in records:
        sid = r["source_id"]
        n = os.path.basename(r["relative_path"])
        parent = None
        if sid == "src_iiit_ilst_devanagari" and "__cropped__Devanagari__" in n:
            parent = (sid, n.split("__cropped__Devanagari__")[1].split("_")[0])
        elif sid == "src_indicstr12_devanagari" and "__cropped_images__" in n:
            parts = n.split("__cropped_images__")
            lang = parts[0].split("__")[1]
            parent = (sid, lang + "/" + parts[1].split("_")[0])
        if parent is not None:
            h = scene_hash.get(parent)
            if h:
                # Key on the PARENT'S hash: shared parents collapse across sources.
                r["_content_key"] = f"content::parent::{h}"
                resolved += 1
            else:
                # Parent photograph was not acquired. Do not pretend the crop is independent.
                r["_content_key"] = f"content::parent_unacquired::{sid}::{parent[1]}"
                orphan_parents.add(f"{sid}::{parent[1]}")
                unresolved += 1
        elif sid in ("src_iiit_ilst_devanagari", "src_indicstr12_devanagari"):
            r["_content_key"] = f"content::parent::{r['sha256']}"   # a scene photograph IS its parent
        else:
            r["_content_key"] = f"content::self::{r['sha256']}"
    return {"crops_resolved_to_parent": resolved,
            "crops_with_unacquired_parent": unresolved,
            "orphan_parent_ids": sorted(orphan_parents)}


LEVELS = {
    "byte": byte_key,
    "content": content_key,
    "source_lineage": source_lineage_key,
}
