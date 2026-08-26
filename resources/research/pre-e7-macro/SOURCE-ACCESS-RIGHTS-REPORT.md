# Source access & rights — what evidence we can legitimately obtain

**Task:** R3-A of `resources/tasks/RES-003-CLOUD-EVIDENCE-PROGRAM.md`
**Date:** 26 Aug 2026 · **Branch:** `work/res-003-evidence-topology`
**Register (source of truth):** `REQUEST-AND-EVAL-SOURCE-ACCESS-REGISTER.yaml` — 13 sources
**Validator:** `validators/check_source_register.py` — executed, exit 0

**No acquisition. No download. No account, login, form or terms acceptance. ₹0 / $0.**

---

## The limitation that shapes every claim below

**This session's egress proxy blocks the official pages.** `huggingface.co`, `arxiv.org`,
`poloclub.github.io` and `vidprom.github.io` all returned `EGRESS_BLOCKED` on direct fetch. Web
**search** worked.

So **nothing here is `officially_verified`.** Every rights fact is `search_supported` — from search
results that quote or summarise the official source — or `unknown`. The validator enforces this: it
fails if any field claims `officially_verified` while the register records the egress block.

**Consequence for the Controller:** no row below may drive an acquisition decision until a human
reads the actual licence file on the actual distribution page. That is one afternoon's work for
someone with unrestricted network access, and it is the cheapest de-risking available.

---

## 1. The headline: we can get request evidence, and the licences differ in ways that matter

| Source | Prompt text | Licence | Commercial use | Verdict |
|---|---|---|---|---|
| **LMArena open data** | full | **CC-BY-4.0** (prompts) | **permitted** | **Best-positioned request source** |
| **DiffusionDB** | full | **CC0 1.0** | permitted | Usable; stale images, hobbyist skew |
| **VidProM** | full | **CC BY-NC 4.0** | **non-commercial only** | Discovery only, NC unresolved |
| **TIP-I2V** | full + user images | **CC BY-NC 4.0** | **non-commercial only** | Text only; **images not cleared** |

**The single most useful finding: request-space evidence is genuinely obtainable.** Millions of real
user prompts are publicly available under permissive terms. Canon does not have to invent a request
taxonomy from synthetic briefs, which is precisely the failure the macro reset exists to correct.

**But three of the four carry a live rights problem**, and they are different problems:

**Non-commercial (VidProM, TIP-I2V).** CC BY-NC forbids commercial use. Our product is commercial.
Learning a taxonomy from NC data and shipping a commercial system informed by it are different acts,
and where the line sits is **a human legal judgement, not a worker's call**. Flagged, not resolved.

**Prompt-text provenance (DiffusionDB).** The images are CC0 and that is clean. The *prompts* are
user-written text, and the stated basis for treating them as free is the **Discord server's terms of
service**, under which users "forfeit all intellectual property rights claims… including forfeiture
of any/all copyright claim(s)". That is a third-party platform-terms argument, not a per-author
licence grant. It is the strongest such argument in the register and it is still an argument. Recorded
as the publisher's position, not restated as settled.

**User-uploaded images (TIP-I2V) — the most serious gap.** Every record includes a user-supplied
**image** prompt. Provenance is not stated: these may be third-party copyright works, and they may
depict identifiable people. The dataset records an NSFW flag for images, which tells us the publisher
expected problematic uploads. **The text prompts are usable for discovery; the uploaded images are
not cleared and must not be treated as person-reference material.** This is exactly the category
Resources has repeatedly declined to collect.

## 2. The circularity risk, named

**`Arena-T2I-Hard`'s 310 benchmark prompts are sampled from the same public arena pool that the
LMArena open data exposes.** Its own methodology confirms the shape: prompts drawn from a public
text-to-image arena leaderboard, Jan–Mar 2026, with a separate 10k training and disjoint 1k test
split taken from the same pool.

If **Canon** learns its request grammar from arena prompts and **Eval** then benchmarks on
Arena-T2I-Hard, the benchmark is a *descendant of the discovery set*, and any claim that the system
"generalises" is circular. The register records them as **one lineage** (`lin_lmarena`) and
`R3-C` builds the rule that keeps them out of a discovery role and a holdout role in the same
experiment.

**A second, quieter instance:** `src_imagerewarddb` — **already in our acquired corpus, 2,584 items** —
draws its images from DiffusionDB. Acquiring DiffusionDB would therefore not add an independent
lineage; it would enlarge one we already hold. That is `lin_diffusiondb`, and it is the kind of thing
a hash-based check cannot see.

**Three multi-member lineages** in total, machine-checked by the validator:

| Lineage | Members | Consequence |
|---|---|---|
| `lin_lmarena` | LMArena open data + Arena-T2I-Hard | never discovery-and-holdout together |
| `lin_pika_discord` | VidProM + TIP-I2V | same authors, same Discord, same method — one source |
| `lin_diffusiondb` | DiffusionDB + **our ImageRewardDB** | we already hold part of this lineage |

## 3. Benchmark resources: useful references, thin rights records

GenEval, T2I-CompBench(++), VBench and T2V-CompBench are all publicly reachable on GitHub with no
gate reported. Their **dataset/annotation licences are not separately established**, and that is
recorded as `unknown` rather than filled in.

**T2I-CompBench is the trap worth naming.** Search reports the repository as **MIT** — and MIT is the
**code** licence. The register carries an explicit caution: *do not record this as an "MIT-licensed
dataset"*. This project has already been caught by exactly that substitution once, with PVP, where a
search asserted the dataset was MIT and it was the repository's code licence. The practical risk here
is lower because these benchmarks are mostly prompt text rather than media — **the discipline is the
point, not the exposure**.

Two observations for Eval, offered as evidence and **not** as Resources deciding anything:

- **T2V-CompBench's dynamic-attribute and motion binding** are the closest external analogue to our
  `REQ-CAP-20/21/22` in-clip stability rows — still our sharpest uncovered gap.
- **Arena-T2I-Hard's dependency-aware DAG evaluator** (fail a parent question, its descendants zero
  out; ~13.9k questions over 310 prompts) is a methodologically interesting way to stop a scorer
  awarding credit for details inside a scene it already got wrong. **Eval's call entirely.**

## 4. Controlled packs: one open question closed, unfavourably

**ABO resolves to CC BY-NC 4.0.** The Resources V1 route research recorded a *contradiction* — the AWS
Open Data registry reporting CC BY-NC 4.0 while the dataset's own documentation was reported as
CC BY 4.0 — and marked it **blocked pending human verification rather than guessing**. That was the
right call, and tonight's search resolves it consistently to **CC BY-NC 4.0**, with a named licence
file (`LICENSE-CC-BY-NC-4.0.txt`) users must accept.

**The contradiction resolves to the restrictive reading.** ABO was structurally near-ideal for the
product reference pack — 8,222 listings with 24- or 72-view turntable sequences is exactly the
controlled-multi-view shape we need — and **non-commercial use rules it out as the pack for a
commercial system.** It remains usable for internal non-commercial evaluator calibration.

This strengthens rather than changes the V1 recommendation: **controlled first-party capture is the
route for the product pack.** The best public alternative just closed.

Unchanged from V1:

- **Google Scanned Objects** — CC BY 4.0, no NC problem, genuinely controlled multi-view — but
  **generic household objects with no wordmark and no brand colour spec**. Cannot serve
  `logo_wordmark_fidelity` or `packaging_brand_colour_fidelity` at all.
- **Pitt Ads** — the **email-request gate** is confirmed again from the official readme text. A human
  permission decision; not attempted. Still the only public candidate that addresses the commercial
  creative bank.
- **HiACC** — **audio only**, and CC BY-NC. Four of five speech capabilities need video of a speaking
  face. It does not substitute for the AV pack.

## 5. What this means in one paragraph

**We can legitimately obtain large-scale, real, permissively-licensed evidence about what people ask
generative systems to make** — principally from LMArena (CC-BY-4.0 prompts, commercial use permitted)
and DiffusionDB (CC0), with VidProM and TIP-I2V available for discovery if the non-commercial term is
cleared by a human. **We cannot obtain, from any public source reviewed, the controlled reference
material the capability work needs**: the product-pack front-runner is now non-commercial, the
commercial-creative candidate is behind a human permission gate, and there is no public AV pack with
faces, verified transcripts, turn boundaries and permissive terms. The asymmetry is the finding:
**request evidence is cheap and legally clean; controlled evidence is neither, and no amount of
searching changes that.**

## 6. Decisions this puts to the Controller

1. **Is CC BY-NC data usable for taxonomy discovery in a commercial product?** Affects VidProM and
   TIP-I2V. A legal judgement, not a worker's.
2. **Verify the four load-bearing licences against official pages** where they are reachable —
   LMArena prompt terms, DiffusionDB, ABO, and whichever benchmark Eval intends to adopt.
3. **Accept the arena lineage constraint** (`lin_lmarena`), which costs Eval the option of treating
   Arena-T2I-Hard as a clean holdout if Canon discovers from arena data.
4. **Pitt Ads: send the email or close the route.** Unchanged from V1 and still the only public path
   to a commercial creative bank.

## Sources consulted

- [DiffusionDB — Hugging Face dataset card](https://huggingface.co/datasets/poloclub/diffusiondb) · [project site](https://poloclub.github.io/diffusiondb/) · [paper](https://arxiv.org/html/2210.14896)
- [VidProM — Hugging Face](https://huggingface.co/datasets/WenhaoWang/VidProM) · [project site](https://vidprom.github.io/)
- [TIP-I2V — Hugging Face](https://huggingface.co/datasets/WenhaoWang/TIP-I2V) · [project site](https://tip-i2v.github.io/)
- [LMArena open data announcement](https://news.lmarena.ai/opendata-july2025/) · [Arena leaderboard dataset](https://arena.ai/blog/arena-leaderboard-dataset) · [Arena-Rank methodology](https://news.lmarena.ai/arena-rank/)
- [Arena-T2I-Hard — Hugging Face](https://huggingface.co/datasets/lmarena-ai/Arena-T2I-Hard) · [project page](https://banyuanhao.github.io/Arena-T2I-Hard-Page/)
- [T2I-CompBench — GitHub](https://github.com/Karine-Huang/T2I-CompBench) · [T2V-CompBench — GitHub](https://github.com/KaiyueSun98/T2V-CompBench) · [Video-Bench — GitHub](https://github.com/Video-Bench/Video-Bench)
- [Amazon Berkeley Objects — AWS Registry of Open Data](https://registry.opendata.aws/amazon-berkeley-objects/) · [Amazon Science](https://www.amazon.science/code-and-datasets/amazon-berkeley-objects-abo-dataset)
- [Google Scanned Objects — Google Research](https://research.google/blog/scanned-objects-by-google-research-a-dataset-of-3d-scanned-common-household-items/)
- [Pitt Image and Video Ads — official readme text](https://people.cs.pitt.edu/~kovashka/ads/readme_images.txt)
- [HiACC — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2352340925006109)
