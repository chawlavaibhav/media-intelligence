# Route catalogue for the Stage A freeze package (EVAL-039A), aligned to the sibling's
# eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml (EVAL-039B, present at build time, read-only).
# Every priced line names the roster record (roster_key, variant) it was taken from; build.py cross-checks
# the value against the roster and fails loudly on drift. Where the roster has no record or the price is not
# projectable per unit, the line is `unpinned` (0 in totals, summed separately, outside the cap).
#
# price_status: pinned = roster route_status pinned for that record/variant (bytes + sha in PIN-INDEX.yaml);
#               unpinned = no pin, or pinned-but-not-projectable (token-metered with no per-image table);
#               plan_indicative is no longer used — every number below is either a pin or absent.
# seed_support from EVAL-010 (WORKFLOW-CONTROL-MATRIX.yaml reproducibility_summary); 'undocumented' otherwise.

PINS = "eval/empirical-planning/price-pins-2026-09/"
ROSTER = "eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml"
R = {}

def route(key, route_id, surface, pool, status, arm, unit, price, price_status, pin_ref, seed,
          roster_key=None, roster_variant=None, plan_ref="plan §C.3", note=None, credit_alternative=None,
          conditional=False, family=None, quantity_rule=None, in_cap=True, priced_surface=None, roster_base_price=None, addon=None):
    R[key] = dict(key=key, route_id=route_id, surface=surface, billing_pool=pool, route_status=status, arm=arm,
                  unit=unit, unit_price=price, price_status=price_status,
                  price_ref=(pin_ref if pin_ref else "unpinned — no projectable price in " + ROSTER),
                  seed_support=seed, roster_key=roster_key or key, roster_variant=roster_variant, plan_ref=plan_ref,
                  note=note, credit_alternative=credit_alternative, conditional=conditional, family=family or key,
                  quantity_rule=quantity_rule, in_cap=in_cap, priced_surface=priced_surface, roster_base_price=roster_base_price, addon=addon)

VX = PINS + "vertex-shared/vertex-generative-ai-pricing.html"
# ---- image core (6) ---------------------------------------------------------------------------
route("gpt-image-2", "openai/gpt-image-2", "fal", "cash", "pinned", "cheap", "per_image", 0.053, "pinned",
      PINS + "gpt-image-2/fal-openai-gpt-image-2.html", "absent_in_api", roster_variant="fallback",
      priced_surface="fal (the roster's fallback record, route_status pinned); the credit surface azure_foundry gpt-image-2 is needs_controller_enablement", note="fal fallback pinned at 0.053/image for 1024x1024 at quality=medium (fal's default is high at 0.211 — the harness must set quality=medium); the credit surface is Azure gpt-image-2 (token-metered $30/1M output tokens, per-image unknown) and needs a Controller deployment (roster: needs_controller_enablement; MD-9)",
      credit_alternative="azure_foundry gpt-image-2 (credits) only if the Controller deploys a resource — morning decision 3")
route("nano-banana-2", "gemini-3.1-flash-image", "vertex", "credits", "pinned", "cheap", "per_image", 0.067, "pinned", VX, "exposed")
route("nano-banana-pro", "gemini-3-pro-image", "vertex", "credits", "pinned", "premium", "per_image", 0.134, "pinned", VX, "exposed")
route("seedream-5-pro", "bytedance/seedream/v5/pro/text-to-image", "fal", "cash", "pinned", "premium", "per_image", 0.0675, "pinned",
      PINS + "seedream-5-pro/fal-api-models-seedream-v5-pro-t2i.json", "undocumented")
route("flux-2-pro", "fal-ai/flux-2-pro", "fal", "cash", "pinned", "cheap", "per_image", 0.03, "pinned",
      PINS + "flux-2-pro/fal-api-models-flux-2-pro.json", "undocumented", roster_variant="fallback",
      priced_surface="fal (the roster's fallback record, route_status pinned); the credit surface azure_foundry FLUX.2-pro is needs_controller_enablement", note="fal fallback pinned at 0.03 first megapixel (1 MP outputs); Azure FLUX.2-pro lists the same 0.03 on credits but no deployment exists (roster: needs_controller_enablement; MD-9)",
      credit_alternative="azure_foundry FLUX.2-pro (credits, eastus/southindia) only if the Controller deploys — morning decision 3")
route("qwen-image-3", "alibaba/qwen-image-3", "fal", "cash", "pinned", "cheap", "per_image", 0.04, "pinned",
      PINS + "qwen-image-3/fal-api-models-qwen-image-3-t2i.json", "undocumented")
# conditional credit-only image extras (task §B.1: recorded as needs_controller_enablement)
route("sd3.5-large", "stability.sd3-5-large-v1:0", "bedrock", "credits", "needs_controller_enablement", "cheap", "per_image", 0.08, "pinned",
      PINS + "sd3.5-large/aws-bedrock-list-foundation-model-agreement-offers-sd3.5-large.json", "undocumented", plan_ref="plan §C.3c", conditional=True,
      note="roster: price pinned from the Bedrock offer rate card and the account reads AUTHORIZED (INFERRED, to be confirmed by one metered call — MD-9); the task records the route as needs_controller_enablement (morning decision 4)")
route("mai-image-2.6", "MAI-Image-2.6", "azure", "credits", "needs_controller_enablement", "cheap", "per_image", None, "unpinned",
      None, "undocumented", plan_ref="plan §C.3c", conditional=True, note="roster: price unpublished (Retail Prices API has no 2.6 meters)")
# text arm B extra
route("recraft-v4", "fal-ai/recraft/v4 (text-to-image)", "fal", "cash", "pinned", "premium", "per_image", 0.04, "pinned",
      PINS + "recraft-v4/fal-recraft-v4-text-to-image.html", "absent_in_api",
      note="EVAL-010 verified the text-to-vector path has no seed; the raster path is the pinned one")
# ---- edit / reference (4) ---------------------------------------------------------------------
route("flux-2-pro-edit", "fal-ai/flux-2-pro/edit", "fal", "cash", "pinned", "edit", "per_image", 0.045, "pinned",
      PINS + "flux-2-pro-edit/fal-api-models-flux-2-pro-edit.json", "undocumented",
      quantity_rule="0.03 first output megapixel + 0.015 per input megapixel (price_addons.additional_megapixel): one 1-MP reference → 0.045 per edit generation (roster after Auditor AF-2, commit 3434b37)",
      roster_base_price=0.03, addon="0.015 per input megapixel × 1 reference (roster price_addons.additional_megapixel, pinned in the same bytes)",
      note="priced at 0.045 = pinned base 0.03 + pinned 0.015 addon for one 1-MP reference, as the committed roster's projection does; a 2- or 3-reference case (IMG-COMP-01, IMG-REF-*) may bill more addon megapixels — recorded, not projected",
      credit_alternative="azure_foundry FLUX.2-pro with reference image (credits) if deployed — morning decision 3")
route("nano-banana-pro-edit", "fal-ai/nano-banana-pro/edit", "fal", "cash", "pinned", "edit", "per_image", 0.15, "pinned",
      PINS + "nano-banana-pro-edit/fal-api-models-nano-banana-pro-edit.json", "exposed",
      note="roster records the fal edit route as the plan names it; the same model edits on Vertex (gemini-3-pro-image with image inputs, 0.134 + 560 input tokens per reference) on credits — the roster and this package both flag that the Controller may switch the surface (open question)",
      credit_alternative="vertex gemini-3-pro-image with image inputs (credits, 0.134 pinned + input tokens) — Controller may switch")
route("seedream-5-pro-edit", "bytedance/seedream/v5/pro/edit", "fal", "cash", "pinned", "edit", "per_image", 0.0675, "pinned",
      PINS + "seedream-5-pro-edit/fal-api-models-seedream-v5-pro-edit.json", "undocumented")
route("gpt-image-2-edit", "openai/gpt-image-2/edit", "fal", "cash", "pinned", "edit", "per_image", None, "unpinned",
      PINS + "gpt-image-2-edit/fal-api-models-openai-gpt-image-2-edit.json", "absent_in_api",
      note="pinned but not projectable: only the token meter ($30/1M output tokens) is in the pinned bytes; no per-image table for the edit path → 0 in totals, listed under unpinned (the roster's own reading)",
      credit_alternative="azure_foundry gpt-image-2 edit (credits) if deployed — morning decision 3")
# ---- text-to-video core (6) -------------------------------------------------------------------
route("veo-3.1-fast", "veo-3.1-fast-generate-001", "vertex", "credits", "pinned", "cheap", "per_second", 0.10, "pinned", VX, "exposed", roster_variant="t2v")
route("kling-v3-pro-audio", "fal-ai/kling-video/v3/pro/text-to-video (audio on)", "fal", "cash", "pinned", "cheap", "per_second", 0.168, "pinned",
      PINS + "kling-v3-pro/fal-api-models-kling-v3-pro-t2v.json", "absent_in_api", roster_key="kling-v3-pro", roster_variant="t2v-audio-on", family="kling-v3-pro",
      note="the roster pins two Kling t2v prices: 0.112/s silent, 0.168/s with native audio; the core runs with audio where native, so the audio-on price applies")
route("kling-v3-pro", "fal-ai/kling-video/v3/pro/text-to-video (silent)", "fal", "cash", "pinned", "cheap", "per_second", 0.112, "pinned",
      PINS + "kling-v3-pro/fal-api-models-kling-v3-pro-t2v.json", "absent_in_api", roster_variant="t2v")
route("minimax-h3-max", "minimax/h3-max/text-to-video (768p)", "fal", "cash", "pinned", "cheap", "per_second", 0.08, "pinned",
      PINS + "minimax-h3-max/fal-api-models-minimax-h3-max-t2v.json", "undocumented", roster_variant="t2v-768p",
      note="regular 0.08/s; the 0.02/s promotion ending 7 Sep is recorded in the roster and never used")
route("wan-3.0-prime", "alibaba/wan-3.0-prime/text-to-video", "fal", "cash", "pinned", "cheap", "per_second", 0.14, "pinned",
      PINS + "wan-3.0-prime/fal-api-models-wan-3.0-prime-t2v.json", "undocumented", roster_variant="t2v")
route("gemini-omni-1.1-flash", "gemini-omni-1.1-flash-preview", "vertex", "credits", "pinned", "cheap", "per_second", 0.10136, "pinned", VX, "exposed",
      roster_key="gemini-omni-flash-1.1", roster_variant="t2v")
route("seedance-2.5", "bytedance/seedance-2.5/text-to-video", "fal", "cash", "pinned", "premium", "per_second", 0.473, "pinned",
      PINS + "seedance-2.5/fal-api-models-seedance-2.5-t2v.json", "undocumented", roster_variant="t2v")
route("sora-2", "sora-2", "azure", "credits", "needs_controller_enablement", "cheap", "per_second", 0.10, "pinned",
      PINS + "sora-2/azure-retail-prices-sora-2.json", "undocumented", plan_ref="plan §C.3c", conditional=True,
      note="preview; eastus2/swedencentral; new Azure resource needed; gating unknown (MD-2)")
# ---- cost knee tiers -------------------------------------------------------------------------
route("veo-3.1-lite", "veo-3.1-lite-generate-001", "vertex", "credits", "pinned", "cheap", "per_second", 0.05, "pinned", VX, "exposed",
      note="PUBLIC_PREVIEW; the Vertex cell reads '$0.05 / 1 count' — read as per second (roster assumption, recorded)")
route("veo-3.1-full", "veo-3.1-generate-001", "vertex", "credits", "pinned", "premium", "per_second", 0.40, "pinned", VX, "exposed")
route("minimax-h3-max-480p", "minimax/h3-max/text-to-video (480p)", "fal", "cash", "pinned", "cheap", "per_second", 0.05, "pinned",
      PINS + "minimax-h3-max/fal-api-models-minimax-h3-max-t2v.json", "undocumented", roster_key="minimax-h3-max", roster_variant="t2v-480p", family="minimax-h3-max")
# ---- image-to-video ---------------------------------------------------------------------------
route("veo-3.1-fast-i2v", "veo-3.1-fast-generate-001 (image input)", "vertex", "credits", "pinned", "cheap", "per_second", 0.10, "pinned", VX, "exposed",
      roster_key="veo-3.1-fast", roster_variant="i2v", family="veo-3.1-fast")
route("kling-v3-pro-i2v", "fal-ai/kling-video/v3/pro/image-to-video", "fal", "cash", "pinned", "cheap", "per_second", 0.112, "pinned",
      PINS + "kling-v3-pro/fal-api-models-kling-v3-pro-i2v.json", "undocumented", roster_key="kling-v3-pro", roster_variant="i2v", family="kling-v3-pro")
route("minimax-h3-max-i2v", "minimax/h3-max/image-to-video (768p)", "fal", "cash", "pinned", "cheap", "per_second", 0.08, "pinned",
      PINS + "minimax-h3-max/fal-api-models-minimax-h3-max-i2v.json", "undocumented", roster_key="minimax-h3-max", roster_variant="i2v-768p", family="minimax-h3-max",
      note="cheapest PINNED image-to-video route at 720p-class (0.08/s) — used for TOPO-03 arm C and the VID-2SPK-01 chain; H3 Max i2v-480p (0.05/s) is cheaper but below round one's 720p")
route("wan-3.0-prime-i2v", "alibaba/wan-3.0-prime/image-to-video", "fal", "cash", "pinned", "cheap", "per_second", 0.14, "pinned",
      PINS + "wan-3.0-prime/fal-api-models-wan-3.0-prime-i2v.json", "undocumented", roster_key="wan-3.0-prime", roster_variant="i2v", family="wan-3.0-prime")
route("seedance-2.5-i2v", "bytedance/seedance-2.5/image-to-video", "fal", "cash", "pinned", "premium", "per_second", 0.473, "pinned",
      PINS + "seedance-2.5/fal-api-models-seedance-2.5-i2v.json", "undocumented", roster_key="seedance-2.5", roster_variant="i2v", family="seedance-2.5")
route("veo-3.1-lite-i2v", "veo-3.1-lite-generate-001 (image input)", "vertex", "credits", "unpinned", "cheap", "per_second", None, "unpinned",
      None, "exposed", roster_key="veo-3.1-lite", family="veo-3.1-lite",
      note="task-fixed arm-A route for TOPO-03; the roster pins Veo 3.1 Lite t2v at 0.05/s but records no i2v variant and capabilities null → this line is unpinned (0 in totals; the Controller may price it at 0.05/s if Lite accepts an image input)")
# ---- reference-to-video -----------------------------------------------------------------------
route("seedance-2.5-ref2v", "bytedance/seedance-2.5/reference-to-video", "fal", "cash", "pinned", "premium", "per_second", 0.473, "pinned",
      PINS + "seedance-2.5/fal-api-models-seedance-2.5-ref2v.json", "undocumented", roster_key="seedance-2.5", roster_variant="ref2v", family="seedance-2.5")
route("veo-3.1-fast-ref2v", "veo-3.1-fast-generate-001 (reference-to-video)", "vertex", "credits", "pinned", "native", "per_second", 0.10, "pinned", VX, "undocumented",
      roster_key="veo-3.1-fast", roster_variant="ref2v", family="veo-3.1-fast",
      note="the plan names 'veo-3.1 reference-to-video' without a tier; the roster pins the Fast tier's ref2v variant at 0.10/s, so that tier is used (credits); EVAL-010: the fal veo3.1 reference-to-video path has no seed — Vertex path undocumented")
route("kling-v3-elements", "fal-ai/kling-video/v3/pro/elements", "fal", "cash", "unpinned", "cheap", "per_second", None, "unpinned",
      None, "undocumented", roster_key="kling-v3-pro", roster_variant="elements-ref2v", conditional=True, family="kling-v3-pro",
      note="plan: 'if pinned' — the roster records the elements variant as unpinned")
# ---- multi-shot / long ------------------------------------------------------------------------
route("kling-v3-pro-15s", "fal-ai/kling-video/v3/pro/text-to-video (15 s)", "fal", "cash", "pinned", "cheap", "per_second", 0.112, "pinned",
      PINS + "kling-v3-pro/fal-api-models-kling-v3-pro-t2v.json", "absent_in_api", roster_key="kling-v3-pro", roster_variant="15s", plan_ref="plan §C.3d", family="kling-v3-pro",
      note="silent price; VID-MS-01 runs ambient audio where native — if audio-on is chosen the 0.168/s variant applies (recorded)")
route("seedance-2.5-15s", "bytedance/seedance-2.5/text-to-video (15 s)", "fal", "cash", "pinned", "premium", "per_second", 0.473, "pinned",
      PINS + "seedance-2.5/fal-api-models-seedance-2.5-t2v.json", "undocumented", roster_key="seedance-2.5", roster_variant="15s", plan_ref="plan §C.3d", family="seedance-2.5")
route("gemini-omni-1.1-flash-long", "gemini-omni-1.1-flash-preview (longest supported ≤ 15 s)", "vertex", "credits", "pinned", "cheap", "per_second", 0.10136, "pinned", VX, "exposed",
      roster_key="gemini-omni-flash-1.1", roster_variant="multishot-10s", plan_ref="plan §C.3d", family="gemini-omni-1.1-flash",
      note="the roster pins a 10-s multishot variant; the longest supported duration ≤ 15 s is not stated (capabilities null) — priced at 15 s × 0.10136 as the ceiling")
route("veo-3.1-fast-extend", "veo-3.1-fast-generate-001 + extend (8 s + 7 s)", "vertex", "credits", "pinned", "cheap", "per_second", 0.10, "pinned", VX, "exposed",
      roster_key="veo-3.1-fast", roster_variant="extend-15s", plan_ref="plan §C.3d", family="veo-3.1-fast", note="one trial = 2 API calls; 15 billed seconds")
route("kling-v3-pro-10s", "fal-ai/kling-video/v3/pro/text-to-video (10 s multi-shot prompt)", "fal", "cash", "pinned", "cheap", "per_second", 0.112, "pinned",
      PINS + "kling-v3-pro/fal-api-models-kling-v3-pro-t2v.json", "absent_in_api", roster_key="kling-v3-pro", roster_variant="multishot-10s", family="kling-v3-pro")
route("gemini-omni-1.1-flash-10s", "gemini-omni-1.1-flash-preview (10 s)", "vertex", "credits", "pinned", "cheap", "per_second", 0.10136, "pinned", VX, "exposed",
      roster_key="gemini-omni-flash-1.1", roster_variant="multishot-10s", family="gemini-omni-1.1-flash")
# ---- TTS --------------------------------------------------------------------------------------
route("sarvam-bulbul-v3", "bulbul:v3", "direct", "sarvam_credits", "pinned", "native", "per_1k_chars_inr", 3.0, "pinned",
      PINS + "sarvam-bulbul-v3/sarvam-api-pricing.html", "absent_in_api",
      note="key present: the Controller session stated it and EVAL-039B's Tester (DEFECT-1, commit a24b197) corrected the overnight 'empty value' reading to a 36-character value (length check only; never read by this task); price pinned ₹3.00 per 1,000 characters; the roster labels Sarvam's prepaid balance 'cash', this package keeps the task's 'sarvam_credits' pool name — same money")
route("elevenlabs-v3", "fal-ai/elevenlabs/tts/eleven-v3", "fal", "cash", "pinned", "native", "per_1k_chars", 0.10, "pinned",
      PINS + "elevenlabs-v3/fal-elevenlabs-tts-eleven-v3.html", "exposed", note="EVAL-010: ElevenLabs direct exposes seed; the fal wrapper's seed support is what the harness records")
route("chirp-3-hd-hi-in", "hi-IN-Chirp3-HD-<voice> (Cloud Text-to-Speech)", "vertex", "credits", "needs_controller_enablement", "native", "per_1M_chars", None, "unpinned",
      None, "undocumented", plan_ref="plan §C.3c", conditional=True, note="Text-to-Speech API not enabled in the project; price page JS-rendered")
route("azure-neural-tts-hi-in", "Azure Neural TTS hi-IN", "azure", "credits", "needs_controller_enablement", "native", "per_1M_chars", 15.0, "pinned",
      PINS + "azure-neural-tts-hi-in/azure-retail-prices-speech-neural-centralindia.json", "undocumented", plan_ref="plan §C.3c", conditional=True, note="no Speech resource exists yet")
# ---- lipsync ----------------------------------------------------------------------------------
route("sync-lipsync-v3", "fal-ai/sync-lipsync/v3", "fal", "cash", "unpinned", "chain", "per_second", None, "unpinned",
      None, "undocumented", quantity_rule="per output second (the August figure USD 8/min = 0.1333/s belongs to the sibling endpoint fal-ai/sync-lipsync/v3/image-to-video, not to this one)",
      note="UNPINNED at the committed roster (EVAL-039B Auditor AF-1, commit 3434b37): the exact endpoint's pricing field is empty in fal's JSON and page; the only price string in the bytes is the sibling image-to-video endpoint's 0.1333/s. 12 calls outside the cap until pinned. EVAL-010 verified v2/pro has no seed; v3 not enumerated there")
route("kling-lipsync-a2v", "fal-ai/kling-video/lipsync/audio-to-video", "fal", "cash", "pinned", "chain", "per_second", 0.014, "pinned",
      PINS + "kling-lipsync-audio-to-video/fal-api-models-kling-lipsync-a2v.json", "undocumented", roster_key="kling-lipsync-audio-to-video",
      quantity_rule="per input video second, rolled up to the nearest 5-s increment (a 6-s or 8-s plate bills as 10 s)",
      note="the second lipsync route (plan: 'LatentSync-class or Kling lipsync'); the roster added it and notes fal-ai/latentsync exists ($0.2/video, not pinned)")
# ---- music ------------------------------------------------------------------------------------
route("lyria", "lyria-002", "vertex", "credits", "pinned", "native", "per_clip", 0.06, "pinned", VX, "undocumented", plan_ref="plan §C.3d",
      note="NOT RECONCILED (contradiction 1 / MD-7): the plan says 'Lyria 3' (priced 0.04 per 30-s clip on the page) but only lyria-002 answers on the publisher endpoint; the roster prices lyria-002 at the 'Lyria 2' row 0.06 per clip — used here; morning decision 10")
route("elevenlabs-music", "fal-ai/elevenlabs/music", "fal", "cash", "pinned", "native", "per_minute", 0.6, "pinned",
      PINS + "elevenlabs-music/fal-api-models-elevenlabs-music.json", "undocumented", plan_ref="plan §C.3d",
      quantity_rule="per output minute, rounded up (a 30-s clip bills as 1 minute)")

# Evaluator unit prices (nominal, plan §E) — not provider generation calls; not pinned by the roster.
EVAL_PRICES = {
    "cloud-vision-text-detection": dict(unit="per_image", price=0.0015, status="plan_indicative", ref="plan §E: Cloud Vision ≈ USD 1.5 per 1k images (not pinned)", pool="credits (GCP) — unverified", surface="google_cloud_vision (GOOGLE_CLOUD_VISION_API_KEY present by name)"),
    "vlm-triage": dict(unit="per_call", price=0.01, status="plan_indicative", ref="plan §E: VLM triage ≈ USD 0.01 per call (not pinned)", pool="cash", surface="anthropic/gemini (screened_not_qualified)"),
    "asr-vs-script": dict(unit="per_clip", price=None, status="unpinned", ref="plan §D names ASR but no model or price", pool="unknown", surface="unresolved"),
}
USD_INR_REF = 95.4211  # display-only reference from the August file; Sarvam invoices in INR
