# MORNING-DECISIONS — EVAL-039B, for the Controller, morning of 5 September 2026

**What this is.** Ten numbered questions the Executor could not settle overnight without you. Each one says what is needed, why it matters, the options with their consequence, and what happens by default if you say nothing. Nothing has been spent, created, enabled, deployed or deleted; every check tonight was read-only. Companion files: `ROSTER-REFRESH-2026-09.yaml` (ids and prices), `ACCESS-STATUS-2026-09.yaml` (what each cloud allowed), `COST-PROJECTION-2026-09.md` (money), `ACCESS-LOG.md` (every command).

**Headline numbers (from the projection):** Tranche 1 ≈ **USD 161** (≈ 127 cash on fal/direct + ≈ 35 that would come off cloud credits *if the credits exist*) against the proposed USD 175 cap; minimum viable round one ≈ **USD 74**; Tranche 1a is ≈ USD 2.8 over its own USD 60 cap only because of three small additions (see MD-6).

---

## MD-1 — Credit balances and programme enrolment (AWS, GCP, Azure getaight)

- **Needed:** whether each of the three accounts actually holds startup/promotional credits, how much, and until when. No billing read was attempted tonight (it is a different permission and a different question from "can we reach the model").
- **Why it matters:** ≈ USD 35 of Tranche 1 (Veo, Nano Banana, Omni Flash, Lyria on Vertex; SD3.5 on Bedrock) is projected as "credits". If the credits do not exist, that is cash, and the cash line becomes ≈ USD 161. The cash/credits split cannot be trusted until the balances are known.
- **Options:** (a) you read the three billing consoles and write the balances into `ACCESS-STATUS-2026-09.yaml` under `credits`; (b) you tell the Executor to treat everything as cash for Tranche 1 and re-split later; (c) you grant a billing-read permission to the existing identities (a policy change on an existing user — not something a worker should do).
- **Default if unanswered:** the projection stands as written with `credit_balances: unknown`; Tranche 1 is authorised as a USD-equivalent ceiling across both pools, as the decision already says.

## MD-2 — Azure deployments that may not be possible as zero-standing-cost (Sora 2 gating; gpt-image-2 region; MAI-Image-2.6)

- **Needed:** your go/no-go on three Azure deployments once MD-9's resource exists: `gpt-image-2` (GA, eastus2, SKU GlobalStandard), `FLUX.2-pro` (GA, eastus2, GlobalStandard / DataZoneStandard), `sora-2` (Preview, eastus2 / swedencentral only; version 2025-12-08 — the older 2025-10-06 version shows a deprecation date already in the past).
- **Why it matters:** these are the only credit-eligible surfaces for GPT Image 2 and FLUX.2 Pro; until they exist both routes are projected on fal at cash prices (≈ USD 1.5 of Tranche 1 would move from cash to credits — small in money, but it changes which pool the Registry row records). Sora 2 preview access may be gated for this subscription (the survey reported gating threads; not testable read-only). MAI-Image-2.6 has **no published price** (the Retail Prices API has no 2.6 meters) and is not offered in eastus2.
- **Standing cost reading (INFERRED, please verify in the portal cost estimate):** GlobalStandard deployments are metered per token / megapixel / second only; hourly meters exist only for "Provisioned Managed" SKUs. An AI Services S0 resource has no base fee as far as the Retail API shows.
- **Options:** (a) deploy all three with `--sku-name GlobalStandard --sku-capacity 1`; (b) deploy gpt-image-2 and FLUX.2-pro only, skip Sora 2 (it is an addition, 0 generations in the plan's counts); (c) skip Azure entirely for Tranche 1 and keep both routes on fal cash.
- **Default if unanswered:** (c) — nothing is deployed; the projection already prices these routes on fal.

## MD-3 — New GCP project (only if billing is ambiguous)

- **Needed:** a decision only if you want a *separate* GCP project for the battery. Tonight's service account (`aight-gateway-sa`) cannot even list enabled services, so it certainly cannot create projects or read billing accounts; the checks that would have made a new project "unambiguous" (`gcloud projects create` permitted AND exactly one billing account visible) could not be run.
- **Why it matters:** a new project isolates the battery's usage from the gateway's, but a new project needs a billing link, and a wrong link is the one thing tonight's rules forbid.
- **Options:** (a) stay in `vertexaiproject-507518` with a new service account `mi-battery-sa` (MD-9) — no billing change; (b) you create the project and billing link yourself and hand over its id.
- **Default if unanswered:** (a).

## MD-4 — Bedrock offers: no fee found, but the EULA was not read

- **Needed:** your reading of the Stability / Luma offer terms before any agreement is accepted.
- **What was observed (read-only listing, nothing accepted):** all four offers carry *usage-based* pricing only — SD3.5 Large USD 0.08 / image, Stable Image Core 0.04, Stable Image Ultra 0.14, Luma Ray 2 USD 1.50 / s at 720p (0.75 at 540p) — plus "No refunds will be offered." No subscription, hourly or standing-fee term exists in the offer. Each offer names a legal-terms document (URL recorded in the evidence, presigned part stripped); **the document itself was not fetched or read**.
- **Also observed:** `get-foundation-model-availability` says `authorizationStatus AUTHORIZED, entitlementAvailability AVAILABLE` for all four — read as "this account can already invoke them without a new agreement" (INFERRED; one metered call in the morning proves it).
- **Options:** (a) read the four legal documents and, if acceptable, let the first metered call happen under Tranche 1; (b) accept the agreements explicitly with `create-foundation-model-agreement` (MD-9 lists the command) — only if an invoke says an agreement is required.
- **Default if unanswered:** no agreement is created; SD3.5 Large stays in the projection (credits, USD 0.64) and is dropped if the first call is refused.

## MD-5 — Runway account (VID-04 edit-existing-footage)

- **Needed:** whether to open a Runway account. Workers never create vendor accounts.
- **Why it matters:** VID-04 (Runway Aleph) is the only route for "edit existing footage"; without an account it is deferred to Stage B and contributes USD 0 tonight.
- **Options:** (a) you open the account and put the key on this machine (name to be recorded, value never printed); (b) defer VID-04 to Stage B.
- **Default if unanswered:** (b), as the plan already says.

## MD-6 — Caps (60 / 115 / 250 / 150), the H3 Max promotion, and the Veo unit reading

- **Needed:** accept or amend the caps; confirm "regular price only".
- **What the projection shows:** T1a ≈ USD 62.8 vs cap 60 (**over by ≈ 2.8**); T1b ≈ 98.5 vs 115; T2 ≈ 133 vs 250 (blended estimate); T3 ≈ 81 vs 150 (blended estimate). T1a is over *only* because three additions the plan named but did not count in §E were included: SD3.5 Large on AWS credits (8 gens, USD 0.64), Veo 3.1 Lite (4 gens, USD 1.20) and H3 Max 480p (4 gens, USD 1.20) for the VID-05 cost knee. Without them T1a ≈ USD 59.8.
- **H3 Max:** fal's 75 % launch promotion (USD 0.02 / s at 768p) ends **7 September**; the projection uses the regular USD 0.08 / s everywhere and the roster flags the promo with `used_in_totals: false`. If you run H3 Max lines before 7 Sep the real bill will be lower; the *record* must still carry the regular price for CpAO.
- **Veo unit:** the Vertex pricing page prints "$0.40 / 1 count" under "Price (USD)" and never defines "count" in the fetched bytes. The survey and fal read it as *per second*; the projection does too and says so as assumption A-01. If "count" turns out to be per video, Veo lines are ≈ 6× cheaper than projected.
- **Options:** (a) keep the caps and drop the three additions from T1a (or move them to T1b, which has USD 16.5 headroom); (b) raise T1a to USD 65; (c) keep caps and accept that a cap is a ceiling, not a target.
- **Default if unanswered:** regular prices only; caps unchanged; the three additions are moved to Tranche 1b's authorisation when the spend record is written.

## MD-7 — Lyria id and the music-lane count

- **Needed:** which Lyria the music lane uses, and whether "2 briefs × 2" means 4 or 8 generations.
- **What was observed, not reconciled:** the pricing page lists **Lyria 3** (USD 0.04 per 30-second clip), Lyria 3 Pro (0.08 per song) and **Lyria 2** (0.06); the publisher endpoint answers **only `lyria-002`** (GA) — `lyria-3` and `lyria-3-generate-preview` are NOT_FOUND. The roster records `lyria-002` as the id that exists and prices it at 0.06 (reading `-002` as the Lyria 2 row — INFERRED); Lyria 3 is kept as an unpinned variant.
- **Money:** trivial either way (4 clips ≈ USD 0.24; 8 ≈ USD 0.48 on Lyria, plus ElevenLabs Music USD 0.60 per clip on fal).
- **Options:** (a) run `lyria-002` at 0.06 and count 4; (b) count 8; (c) you know the Lyria 3 Vertex id and supply it.
- **Default if unanswered:** `lyria-002`, 4 in the totals, 8 shown.

## MD-8 — Polly Kajal needs an IAM change on an existing user (forbidden tonight)

- **Needed:** whether the future `mi-battery` IAM user (MD-9) should carry `polly:SynthesizeSpeech` (and `polly:DescribeVoices`) so Hindi Polly can be screened on AWS credits.
- **Why it matters:** `claude-aight` is denied Polly and is never edited by a worker; without the extra permission Polly Kajal stays `no_access` (USD 0 in the projection; USD 16 per 1M characters when priced).
- **Options:** (a) include the two Polly actions in the `mi-battery` inline policy (still least-privilege: Bedrock invoke/list/get + Polly synthesise/describe, resource `*`); (b) leave Polly out — Azure Neural TTS (USD 15 / 1M) and Chirp 3 HD (USD 30 / 1M) cover the "cloud TTS" question.
- **Default if unanswered:** (a) — it costs nothing until a call is made.

## MD-9 — Isolated resource creation — needs the Controller's own session

- **What the task planned (§2b) and why it was moved here:** fresh, isolated, zero-standing-cost resources in all three clouds, keys under `~/.mi-battery-keys/` (mode 700 / 600). At the between-role review this was taken out of tonight's scope. Tonight's checks also show the worker identities are too weak to do it: `claude-aight` is denied `iam:GetUser` (so IAM writes are near-certain to fail), and `aight-gateway-sa` cannot list services (so SA creation / API enablement is near-certain to fail). **Run these from your own admin session.** Every step below has its undo. Nothing here has been executed.

### AWS (account 528730633804; region us-west-2 for models)
```
mkdir -m 700 ~/.mi-battery-keys
aws iam create-user --user-name mi-battery --output json
cat > /tmp/mi-battery-policy.json <<'EOF'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":[
 "bedrock:InvokeModel","bedrock:InvokeModelWithResponseStream","bedrock:ListFoundationModels","bedrock:GetFoundationModel",
 "bedrock:GetFoundationModelAvailability","bedrock:ListFoundationModelAgreementOffers","bedrock:CreateFoundationModelAgreement",
 "bedrock:GetUseCaseForModelAccess","bedrock:PutUseCaseForModelAccess",
 "polly:SynthesizeSpeech","polly:DescribeVoices"],"Resource":"*"}]}
EOF
aws iam put-user-policy --user-name mi-battery --policy-name mi-battery-least-privilege --policy-document file:///tmp/mi-battery-policy.json
aws iam create-access-key --user-name mi-battery --output json --query 'AccessKey' > ~/.mi-battery-keys/aws-mi-battery.json && chmod 600 ~/.mi-battery-keys/aws-mi-battery.json
# model access: tonight's read-only check already shows AUTHORIZED / AVAILABLE for all four us-west-2 media models.
# Only if a first invoke says an agreement is required (and only after reading the offer's legal document, MD-4):
aws bedrock list-foundation-model-agreement-offers --region us-west-2 --model-id stability.sd3-5-large-v1:0 --output json   # take offerToken from here
aws bedrock create-foundation-model-agreement --region us-west-2 --model-id stability.sd3-5-large-v1:0 --offer-token <offerToken>
```
Undo: `aws iam delete-access-key --user-name mi-battery --access-key-id <id>` · `aws iam delete-user-policy --user-name mi-battery --policy-name mi-battery-least-privilege` · `aws iam delete-user --user-name mi-battery` · `aws bedrock delete-foundation-model-agreement --region us-west-2 --model-id <id>` · `rm ~/.mi-battery-keys/aws-mi-battery.json`. (Drop the two `polly:` actions if MD-8 = no.)

### GCP (project vertexaiproject-507518) — use your owner account, never the Wherehouse default config
```
export CLOUDSDK_CONFIG=$(mktemp -d); gcloud auth login   # your account; isolated config
gcloud iam service-accounts create mi-battery-sa --project vertexaiproject-507518 --display-name "mi-battery (EVAL-040)"
gcloud projects add-iam-policy-binding vertexaiproject-507518 --member serviceAccount:mi-battery-sa@vertexaiproject-507518.iam.gserviceaccount.com --role roles/aiplatform.user
gcloud iam service-accounts keys create ~/.mi-battery-keys/gcp-mi-battery-sa.json --iam-account mi-battery-sa@vertexaiproject-507518.iam.gserviceaccount.com && chmod 600 ~/.mi-battery-keys/gcp-mi-battery-sa.json
gcloud services enable texttospeech.googleapis.com --project vertexaiproject-507518     # for Chirp 3 HD Hindi
# a NEW project only if both of these succeed unambiguously (MD-3): gcloud billing accounts list  → exactly one;  gcloud projects create mi-battery-<suffix>
```
Undo: `gcloud services disable texttospeech.googleapis.com --project vertexaiproject-507518` · `gcloud iam service-accounts keys delete <KEY_ID> --iam-account mi-battery-sa@…` · `gcloud projects remove-iam-policy-binding vertexaiproject-507518 --member serviceAccount:mi-battery-sa@… --role roles/aiplatform.user` · `gcloud iam service-accounts delete mi-battery-sa@vertexaiproject-507518.iam.gserviceaccount.com` · `rm ~/.mi-battery-keys/gcp-mi-battery-sa.json`. Note: `roles/aiplatform.user` covers Vertex prediction; Cloud Text-to-Speech needs no extra role beyond the enabled API for a service account in the same project (verify with one `voices:list` call, which is free).

### Azure (getaight subscription only)
```
SUB=b832f4a1-79be-4fb2-ae93-6ba6efd209d2
az group create -n mi-battery -l eastus2 --subscription $SUB
az cognitiveservices account create -n mi-battery-foundry -g mi-battery -l eastus2 --kind AIServices --sku S0 --custom-domain mi-battery-foundry --subscription $SUB
az cognitiveservices account deployment create -g mi-battery -n mi-battery-foundry --deployment-name gpt-image-2 --model-name gpt-image-2 --model-version 2026-04-21 --model-format OpenAI --sku-name GlobalStandard --sku-capacity 1 --subscription $SUB
az cognitiveservices account deployment create -g mi-battery -n mi-battery-foundry --deployment-name flux-2-pro --model-name FLUX.2-pro --model-version 1 --model-format "Black Forest Labs" --sku-name GlobalStandard --sku-capacity 1 --subscription $SUB
az cognitiveservices account deployment create -g mi-battery -n mi-battery-foundry --deployment-name sora-2 --model-name sora-2 --model-version 2025-12-08 --model-format OpenAI --sku-name GlobalStandard --sku-capacity 1 --subscription $SUB   # only if MD-2 = yes; preview may be gated
{ printf 'AZURE_MI_BATTERY_ENDPOINT='; az cognitiveservices account show -g mi-battery -n mi-battery-foundry --subscription $SUB --query properties.endpoint -o tsv; printf 'AZURE_MI_BATTERY_KEY='; az cognitiveservices account keys list -g mi-battery -n mi-battery-foundry --subscription $SUB --query key1 -o tsv; } > ~/.mi-battery-keys/azure-mi-battery.env && chmod 600 ~/.mi-battery-keys/azure-mi-battery.env
```
Before running: confirm in the portal's cost estimate that AI Services S0 and GlobalStandard capacity 1 carry no hourly charge (tonight's Retail-API reading says they do not — INFERRED). Undo: `az cognitiveservices account deployment delete -g mi-battery -n mi-battery-foundry --deployment-name <name> --subscription $SUB` · `az cognitiveservices account delete -g mi-battery -n mi-battery-foundry --subscription $SUB` · `az group delete -n mi-battery --subscription $SUB --yes` · `rm ~/.mi-battery-keys/azure-mi-battery.env`.

- **After creation:** one metered image on `gpt-image-2` tells us tokens-per-image, which turns Azure's USD 30 per 1M output tokens into a per-image price (today's projection uses fal's 0.053 at medium quality instead).
- **Default if unanswered:** nothing is created; Tranche 1 runs Google routes on Vertex with the existing service account (which already reaches every needed model), Stability on Bedrock with `claude-aight` if its invoke is allowed (untested), and everything Azure-only stays on fal.

## MD-10 — Sarvam key is present by name but EMPTY

- **Needed:** the Sarvam API key value placed into `~/.mi-keys` as `SARVAM_API_KEY=…` (the line exists with nothing after `=`; length check returned 0).
- **Why it matters:** AUD-01 (bulbul v3 Hindi TTS, ₹3.00 per 1,000 characters — pinned) is `no_access`; its 6 generations count USD 0 in the projection and the TTS comparison collapses to ElevenLabs alone.
- **Options:** (a) paste the key into the file yourself (never in chat); (b) drop AUD-01 from Tranche 1.
- **Default if unanswered:** (b); the route stays in the roster as `no_access`.

---

### Not decisions, but things you should know before authorising
- **Veo and Lyria ids are region-scoped on the publisher API:** the global endpoint returns 404 for them; `us-central1-aiplatform.googleapis.com` returns them. The harness must call the regional endpoint.
- **fal ids changed from the plan's shorthand:** Qwen Image 3 is `alibaba/qwen-image-3/text-to-image`; Wan 3.0 Prime is `alibaba/wan-3.0-prime/text-to-video` / `…/image-to-video`; Kling v3 "elements" has no endpoint (404) — the ref2v line for Kling is excluded (4 gens).
- **fal's H3 Max is fal's own post-trained variant** of MiniMax H3 ("fal's H3 Max is a post-trained variant of MiniMax H3"); the Registry row must say so.
- **Seedance 2.5 on fal also offers 1080p** (USD 1.164 / s), contrary to the §0 note "480p/720p only"; 720p at 0.473 / s is used.
- **gpt-image-2 on fal defaults to quality=high (USD 0.211 per 1024² image)**; the projection's 0.053 assumes quality=medium — the harness must set it.
- **Acceptance of these outputs** as the price/access basis for EVAL-040's spend record is itself a Controller decision (task §HUMAN APPROVAL TRIGGERS).
