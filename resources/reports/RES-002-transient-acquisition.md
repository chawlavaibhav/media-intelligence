# RES-002 — Transient acquisition: what worked, what was kept, what was deleted

**Date:** 24 Aug 2026

## The problem this solves

Some valuable public datasets ship as one very large file. RES-001 hit this with
VideoGen-RewardBench: 13.42 GB in a single zip. The conclusion then was that taking a small
sample was impossible, because you would have to download all 13.42 GB to get at any part of it.
It was marked `too_large_for_pilot` and abandoned.

**That conclusion was wrong, and this task proves it.**

## Why it was wrong — in plain terms

A zip file keeps a table of contents at the **end** of the file. That table lists every file
inside it, and exactly which bytes of the archive each one occupies.

Separately, most web servers support **HTTP range requests** — a way of asking for "just bytes
5,000,000 to 5,200,000 of this file" instead of the whole thing. A server that supports it replies
with status code **206 (Partial Content)** rather than 200.

Put those two facts together and you can:

1. Ask for the last megabyte → read the table of contents → now you know every file inside and
   where it lives.
2. Ask for just the byte ranges of the files you actually want.
3. Unpack those locally.

The full archive is never downloaded and never touches the disk.

**The catch, and why it must be tested rather than assumed:** a server that does *not* support
range requests silently ignores the request and sends the entire file with status 200. That would
defeat the whole purpose. Every script here checks for a 206 first and stops if it does not get one.

## Results

| Source | Archive size | Transferred | % of archive | Kept |
|---|---:|---:|---:|---:|
| VideoGen-RewardBench | 13.42 GB | 0.78 GB | **5.8%** | 288 videos, 755 MB |
| IndicSTR12 | 1.38 GB | 0.11 GB | 8.1% | 3,465 members, 96 MB |
| IIIT-ILST | 0.64 GB | see note | — | 1,569 members, 55 MB |
| BSTD (recognition) | 0.83 GB | 0.83 GB | 100% — full temp download | 25,246 images, 263 MB |

**Reading the index of the 13.42 GB archive cost 0.5 MB across 4 range requests — 0.004% of the
file — and took about six seconds.** That single number is the case for the method.

**BSTD is the exception and shows the limits.** Its archive sits on Google Drive, which does not
expose usable range access the way a plain web server does, so it was downloaded in full to
temporary staging, the Devanagari members extracted, and the archive deleted. That is still
transient — nothing large is retained — but it moved 0.83 GB instead of ~0.2 GB. At this size the
difference does not matter; at 13 GB it would.

**IIIT-ILST transfer figure is undercounted and is left as measured.** A first attempt failed
partway with HTTP/2 framing errors from that host; the successful rerun skipped members already on
disk, so the counter only reflects the rerun. All 1,569 members were verified present at their exact
recorded sizes with matching fingerprints. A clean single pass would move roughly 54 MB. **No
estimate was substituted for the measurement.**

## What is deliberately NOT recorded

For the three range-acquired sources there is **no full-archive fingerprint**, because the full
archive was never downloaded. Recording a hash of a file we never held would be inventing evidence.
What is recorded instead: the official URL, the exact remote archive size, the complete remote
member list, the selection rule, and a fingerprint for every member actually retained. That is
enough to reproduce the selection exactly.

Where an archive *was* downloaded (BSTD), its fingerprint **was** taken before deletion.

## Selection rules — all deterministic and content-blind

Nothing was chosen for what it depicts or how good it looks.

- **VideoGen-RewardBench:** 24 files from each of the 12 distributor-defined generator folders,
  sorted order within each. Equal representation, deliberately *not* "the first 288 files" — that
  would have loaded up on whichever generator happens to sort first and thrown away the generator
  diversity that makes this source worth having.
- **BSTD:** union of (a) annotation language is Hindi and (b) the transcription contains a
  Devanagari character.
- **IndicSTR12:** the distributor's `hindi/` and `marathi/` folders — the two Devanagari-script
  languages — plus their ground-truth text files.
- **IIIT-ILST:** the distributor's `Devanagari/` folder plus its README.

## Deletions

| What | Why |
|---|---|
| `recognition.zip` (829,120,510 bytes, sha256 `159fb044…3036`) | Transient staging. Fingerprinted before deletion; Devanagari members extracted and validated first. |
| Non-Devanagari members of all four archives | Never written to disk at all — they were simply not requested. |
| `KoNViD_1k_subjective.csv` | Separate, human-approved privacy deletion. See `RES-002-privacy-deletion-log.md`. |

## Disk floor

Never approached. The floor is 12 GB free; the lowest point during this task was **14.5 GB**, and
every script refuses to start work that would breach it.

## What remains uncertain

- Whether these hosts will keep honouring range requests. If one stops, the fallback is a full
  temporary download, which needs the disk headroom to be checked again at that time.
- The `videos.zip` archive could be re-uploaded by the publisher with different contents at the same
  URL. We record the remote size and member list, so a change would be detectable, but we cannot
  prove today's bytes match a future fetch the way a full-archive hash would.
