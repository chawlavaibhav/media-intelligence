# Integrity report — full corpus

**Generated from the manifest and registry. Do not hand-edit — rerun `resources/scripts/build_reports.py`.**

Method: SHA256 over every retained file plus an `ffprobe` decode of every item. Deterministic;
no model is involved and nothing is judged on content.

## Totals

| | |
|---|---|
| Retained items | **34,786** |
| Distinct files (unique SHA256) | **34,586** |
| Media bytes (manifest) | **5.70 GB** |
| Decoding cleanly | **34,786 / 34,786** |

## Byte accounting — three figures, all correct, measuring different things

These differ and none is wrong. Quoting one without saying which causes avoidable confusion.

1. **Media bytes** — the sum of the media files in the manifest. The evaluation payload.
2. **Folder bytes** — media *plus* retained annotations, transcriptions, licence files and
   member lists. Larger, and the annotations are the reason several sources are useful at all.
3. **Disk usage (`du`)** — allocated filesystem blocks. A source made of tens of thousands of
   tiny images pays real block overhead; one made of a few large videos pays almost none.

| source | media bytes | folder bytes | non-media | items |
|---|---:|---:|---:|---:|
| `src_bstd_devanagari` | 201.4 MB | 224.3 MB | 22.9 MB | 25,246 |
| `src_iiit_ilst_devanagari` | 52.8 MB | 53.9 MB | 1.1 MB | 1,390 |
| `src_imagerewarddb` | 1125.6 MB | 1126.8 MB | 1.2 MB | 2,584 |
| `src_indicstr12_devanagari` | 90.3 MB | 93.5 MB | 3.2 MB | 3,086 |
| `src_konvid1k` | 2412.9 MB | 2413.2 MB | 0.2 MB | 1,200 |
| `src_videofeedback` | 181.6 MB | 181.9 MB | 0.3 MB | 987 |
| `src_videogen_rewardbench` | 782.6 MB | 790.9 MB | 8.3 MB | 288 |
| `src_youtube_ugc` | 855.1 MB | 855.3 MB | 0.2 MB | 5 |
| **total** | **5.70 GB** | **5.74 GB** | **37.5 MB** | **34,786** |

The largest gap is the Devanagari scene-text material, whose retained transcription files are
a meaningful share of its folder — those transcriptions are precisely what makes it calibration
material rather than a pile of pictures.

## Decode validation

- Clean: **34,786 / 34,786**
- Zero-byte: **0**
- Undecodable: **0**

## Exact duplicates

- Distinct files: **34,586** across **34,786** items
- Duplicate hashes: **200**  (**27** within a single source, **173** spanning two sources)
- Redundant copies: **200**

**Duplicates are reported, never removed.** Deleting them would improve the number and destroy
the finding.

| source | within-source | involved in cross-source | source items |
|---|---:|---:|---:|
| `src_bstd_devanagari` | 19 | 0 | 25,246 |
| `src_iiit_ilst_devanagari` | 0 | 173 | 1,390 |
| `src_imagerewarddb` | 5 | 0 | 2,584 |
| `src_indicstr12_devanagari` | 3 | 173 | 3,086 |

### Cross-source duplicates — the one that matters

| sources sharing byte-identical files | hashes |
|---|---:|
| `src_iiit_ilst_devanagari` ↔ `src_indicstr12_devanagari` | **173** |

For each pair below, the overlap is stated as a share of each source, because "173 files"
means something very different for a 1,390-item source than for a 3,086-item one.

- **173 of `src_iiit_ilst_devanagari`'s 1,390 items** (12.4%) are byte-identical to an item in the other source.
- **173 of `src_indicstr12_devanagari`'s 3,086 items** (5.6%) are byte-identical to an item in the other source.

## Archive deletions

Archives were deleted only after all five conditions held, and each was fingerprinted **before**
deletion so a future re-download stays verifiable.

| source | archive | sha256 |
|---|---|---|
| `src_bstd_devanagari` | `recognition.zip` | `159fb044fba701f87e41a98b…` |
| `src_imagerewarddb` | `validation_1.zip` | `8eb57656d6c424b9451240d5…` |
| `src_imagerewarddb` | `validation_2.zip` | `5349f894b1b1571fbe1aed6a…` |
| `src_konvid1k` | `KoNViD_1k_videos.zip` | `3528bf99b4d8bad23ced543a…` |
| `src_konvid1k` | `KoNViD_1k_metadata.zip` | `13af8b028536bf1864361396…` |

Sources acquired by HTTP range have **no full-archive hash on purpose** — the archive was
never downloaded, so any hash would be fabricated. Their reproduction record is the remote size,
the complete member list, the selection rule and a hash per retained member, in
`_transient_acquisition.json`.

### Files removed

- `src_konvid1k/KoNViD_1k_subjective.csv` — approved privacy deletion (crowdworker IP addresses,
  worker IDs, city/region/country). See `RES-002-privacy-deletion-log.md`.
- `src_youtube_ugc/Animation_360P-188f.mkv` — fetched under a superseded selection rule; removed
  so the corpus reproduces exactly from the script. A reproducibility correction, not a cleanup.
