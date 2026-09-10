# Spend reconciliation — EVAL-040, 10 September 2026

**What this is.** One table per run, built from the sealed ledgers alone, answering the question both
auditors raised: *how much money did the two-day run actually cost?* Rebuild it any time with
`python3 coordination/audits/tools/reconcile_spend.py`. Read-only, no provider call.

**The four numbers people have been mixing up.**

1. **Ledger consumed** — what the cap counted. Once a request may have left the machine, the harness
   settles the reservation at the estimate whatever comes back (`eval/harness-v2/adapters/base.py:355-387`).
   Safe for a cap; not a record of money.
2. **Delivered** — the part of it that produced a sealed artifact.
3. **No artifact** — the part that did not. Some of this was certainly never billed: the six Wan 2
   draws refused with HTTP 422 are recorded in the Controller's own spend record as *"nothing
   generated, nothing charged"* (`coordination/decisions/CONTROLLER-SPEND-AUTHORISATION-WAN2-CONTENDER-ROUND-2026-09-10.md:38`),
   yet USD 2.88 sits in the ledger as spent.
4. **Vendor billed** — **not in this repository.** It can only come from the fal, Google Cloud, Sarvam
   and ElevenLabs statements. The column is left empty on purpose rather than guessed.

**Headline.** Ledger consumed **USD 119.085109** across the run ledgers, plus **USD 3.156153** for the
vision-judge run which has no run ledger at all = **USD 122.241262** counted against caps. Of the
ledgered amount, **USD 108.970609** produced a sealed artifact and **USD 10.114500** produced nothing.
`coordination/CONTROL-STATE.md` previously said USD 110.7 with cash USD 67.0 and credits USD 43.8;
those figures do not reconcile and have been corrected on this branch.

**Two caps were crossed at the level the Controller signs them** — `authorization.video1`
(USD 10.364 against USD 9.96) and `authorization.wan2` (USD 11.840 against USD 11.53). Neither could
have been caught: the ledger enforces a cap inside one run directory, and both authorisations were
used by three or four runs. That mechanism is repaired on this branch; **the disposition of the two
historical crossings is the Controller's to make, and this document does not make it.**

---

```
run                      authorisation                              cap calls   consumed  delivered no-artifact vendor billed
aud-lip                  authorization.lip.local.yaml              1.57     6   0.840000   0.700000    0.140000       unknown
aud-lip-smoke            authorization.lip.local.yaml              1.57     1   0.140000   0.140000           0       unknown
aud-music-eleven-smoke   authorization.music-eleven.local.yaml     3.14     1          0          0           0       unknown
aud-music-lyria          authorization.music-lyria.local.yaml      3.14     4   0.240000   0.240000           0       unknown
aud-music-lyria-smoke    authorization.music-lyria.local.yaml      3.14     1   0.060000          0    0.060000       unknown
aud-music-lyria-smoke2   authorization.music-lyria.local.yaml      3.14     1   0.060000          0    0.060000       unknown
aud-music-lyria-smoke3   authorization.music-lyria.local.yaml      3.14     1   0.060000   0.060000           0       unknown
aud-tts-eleven           authorization.tts-eleven.local.yaml       1.05     6          0          0           0       unknown
aud-tts-eleven-smoke     authorization.tts-eleven.local.yaml       1.05     1          0          0           0       unknown
aud-tts-sarvam           authorization.tts-sarvam.local.yaml       1.05     6   0.008426   0.008426           0       unknown
aud-tts-sarvam-smoke     authorization.tts-sarvam.local.yaml       1.05     1   0.000943   0.000943           0       unknown
half2                    authorization.half2.local.yaml            7.34    36   3.300000   3.300000           0       unknown
half2-fixtures           authorization.half2.local.yaml            7.34    19   1.605000   1.538000    0.067000       unknown
half2-smoke              authorization.half2.local.yaml            7.34     1   0.150000   0.150000           0       unknown
img-r1                   authorization.local.yaml                 12.58    73   4.590000   4.306500    0.283500       unknown
img-r1-composite         authorization.local.yaml                 12.58     4   0.120000   0.120000           0       unknown
img-r1-redo              authorization.local.yaml                 12.58     8   0.511500   0.511500           0       unknown
img-r1-smoke             authorization.local.yaml                 12.58     1   0.067000   0.067000           0       unknown
topo3-nb-plates          authorization.nb.local.yaml               1.57     2   0.134000   0.134000           0       unknown
topo3-nb-video           authorization.nb.local.yaml               1.57     2   0.960000   0.960000           0       unknown
topo3-plates             authorization.video1.local.yaml           9.96     4   0.140000   0.140000           0       unknown
topo3-smoke              authorization.video1.local.yaml           9.96     1   0.480000   0.480000           0       unknown
topo3-video              authorization.video1.local.yaml           9.96    10   9.744000   9.744000           0       unknown
vid-2spk                 authorization.2spk.local.yaml             9.96     8   8.149760   5.461760    2.688000       unknown
vid-2spk-kling           authorization.2spk.local.yaml            13.63     2   2.688000   2.688000           0       unknown
vid-2spk-kling-smoke     authorization.2spk.local.yaml            11.53     1   1.344000   1.344000           0       unknown
vid-2spk-smoke           authorization.2spk.local.yaml             9.96     1   1.120000   1.120000           0       unknown
vid-i2v                  authorization.i2v.local.yaml             23.58    32  20.736000  20.736000           0       unknown
vid-knee                 authorization.knee.local.yaml             7.34     6   6.000000   6.000000           0       unknown
vid-ms                   authorization.ms.local.yaml              16.77     8  10.627200  10.627200           0       unknown
vid-ref                  authorization.ref2.local.yaml             4.72     4   3.200000   3.200000           0       unknown
vid-ref-smoke            authorization.ref.local.yaml              3.14     1   0.600000          0    0.600000       unknown
vid-ref-smoke2           authorization.ref2.local.yaml             4.72     1   0.800000   0.800000           0       unknown
vid-t2v                  authorization.t2v.local.yaml              37.2    40  28.289280  24.953280    3.336000       unknown
vid-t2v-smoke            authorization.t2v.local.yaml              37.2     1   0.480000   0.480000           0       unknown
vid-wan2                 authorization.wan2.local.yaml             8.39    16   8.000000   5.120000    2.880000       unknown
vid-wan2-i2v             authorization.wan2.local.yaml            11.53     6   2.880000   2.880000           0       unknown
vid-wan2-i2v-smoke       authorization.wan2.local.yaml            11.53     1   0.480000   0.480000           0       unknown
vid-wan2-smoke           authorization.wan2.local.yaml             8.39     1   0.480000   0.480000           0       unknown

PER AUTHORISATION FILE - the level the Controller signs a cap at:
authorisation                                 caps seen   consumed  delivered  calls  runs
authorization.lip.local.yaml                       1.57   0.980000   0.840000      7  aud-lip,aud-lip-smoke
authorization.music-eleven.local.yaml              3.14          0          0      1  aud-music-eleven-smoke
authorization.music-lyria.local.yaml               3.14   0.420000   0.300000      7  aud-music-lyria,aud-music-lyria-smoke,aud-music-lyria-smoke2,aud-music-lyria-smoke3
authorization.tts-eleven.local.yaml                1.05          0          0      7  aud-tts-eleven,aud-tts-eleven-smoke
authorization.tts-sarvam.local.yaml                1.05   0.009369   0.009369      7  aud-tts-sarvam,aud-tts-sarvam-smoke
authorization.half2.local.yaml                     7.34   5.055000   4.988000     56  half2,half2-fixtures,half2-smoke
authorization.local.yaml                          12.58   5.288500   5.005000     86  img-r1,img-r1-composite,img-r1-redo,img-r1-smoke
authorization.nb.local.yaml                        1.57   1.094000   1.094000      4  topo3-nb-plates,topo3-nb-video
authorization.video1.local.yaml                    9.96  10.364000  10.364000     15  topo3-plates,topo3-smoke,topo3-video  <<< CONSUMED ABOVE HIGHEST CAP
authorization.2spk.local.yaml          11.53/13.63/9.96  13.301760  10.613760     12  vid-2spk,vid-2spk-kling,vid-2spk-kling-smoke,vid-2spk-smoke
authorization.i2v.local.yaml                      23.58  20.736000  20.736000     32  vid-i2v
authorization.knee.local.yaml                      7.34   6.000000   6.000000      6  vid-knee
authorization.ms.local.yaml                       16.77  10.627200  10.627200      8  vid-ms
authorization.ref2.local.yaml                      4.72   4.000000   4.000000      5  vid-ref,vid-ref-smoke2
authorization.ref.local.yaml                       3.14   0.600000          0      1  vid-ref-smoke
authorization.t2v.local.yaml                       37.2  28.769280  25.433280     41  vid-t2v,vid-t2v-smoke
authorization.wan2.local.yaml                11.53/8.39  11.840000   8.960000     24  vid-wan2,vid-wan2-i2v,vid-wan2-i2v-smoke,vid-wan2-smoke  <<< CONSUMED ABOVE HIGHEST CAP

TOTALS BY BILLING POOL (usd-equivalent, native):
  cash                    77.523500    77.523500
  elevenlabs_credits              0         1198
  credits                 41.552240    41.552240
  sarvam_credits           0.009369     0.894000

  ledger consumed across all runs : USD 119.085109
    of which produced an artifact : USD 108.970609
    of which produced nothing     : USD 10.114500   <- upper bound on money never billed
  vision-judge run (own cap, no run ledger): USD 3.156153 (eval/experiments/EVAL-040/QUALIFICATION-REPORT-2026-09-09.yaml)
  grand total counted against caps: USD 122.241262

  vendor billed: NOT IN THIS REPOSITORY. Read it off the fal, Google Cloud, Sarvam and
  ElevenLabs statements and record it beside these numbers once.
```

---

## What the Controller still has to do with this

1. **Read the four statements once** (fal, Google Cloud, Sarvam, ElevenLabs) for 8–10 September and
   write the billed figure beside the ledgered figure. Until that is done the project has an upper
   bound on its own costs, not a cost. Every price quoted to a customer later rests on this.
2. **Rule on the two cap crossings** — accepted as recorded, or annulled. Do not rewrite the
   historical authorisations either way; record the ruling as a new decision.
3. **Decide whether ledger semantics or vendor billing governs a cap in future.** They are different
   numbers and the difference here was about USD 10.
