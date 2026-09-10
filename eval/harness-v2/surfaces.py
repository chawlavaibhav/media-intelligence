"""SurfaceRegistry: every Stage A route key mapped to the surface it would be called on.

One entry per key of `TEST-CASES.yaml -> route_catalogue` (47 keys; set equality is a test), plus the
EXTENSION_ROUTES: surfaces added after the freeze that have no catalogue row (today: the two ElevenLabs
DIRECT routes on the user's own account, billed in plan credits, pool `elevenlabs_credits`).
An entry says WHICH adapter family would build the request, WHERE it would go, which pinned
request-body schema it is built from, which price pin and billing pool it is charged to, and
which credential NAME would be read at dispatch. It never holds a key value.

`shape_status`:
  verified    the body shape comes from a pinned fal OpenAPI schema (schemas/fal/), a pinned
              vendor reference page (schemas/vertex/, schemas/sarvam/) or a live-proven module
              (eval/experiments/EVAL-038/tools/generate_media.py); dry-run renders it and live
              dispatch may send it.
  unverified  no pinned source for the exact endpoint; dry-run renders a marker body, live
              dispatch refuses (task §EXPANSION TRIGGERS: never guess a field name).
  not_built   no adapter tonight (Bedrock / Azure / Cloud TTS); dry-run prices the row as a
              conditional line; live dispatch refuses.

Nothing here contacts a provider. Constructing the registry opens no network connection and reads no key.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Iterable

GCP_PROJECT = "vertexaiproject-507518"
GCP_REGION = "us-central1"
VERTEX_REGIONAL = f"https://{GCP_REGION}-aiplatform.googleapis.com/v1/projects/{GCP_PROJECT}/locations/{GCP_REGION}/publishers/google/models"
VERTEX_GLOBAL = f"https://aiplatform.googleapis.com/v1/projects/{GCP_PROJECT}/locations/global/publishers/google/models"
VERTEX_INTERACTIONS = f"https://aiplatform.googleapis.com/v1beta1/projects/{GCP_PROJECT}/locations/global/interactions"
FAL_QUEUE = "https://queue.fal.run"
SARVAM_TTS = "https://api.sarvam.ai/text-to-speech"
ELEVENLABS_TTS = "https://api.elevenlabs.io/v1/text-to-speech"      # + /{voice_id}?output_format=mp3_44100_128 (adapter)
ELEVENLABS_MUSIC = "https://api.elevenlabs.io/v1/music"             # the docs URL says /music/compose; the endpoint is /v1/music

AZURE_SUBSCRIPTION = "b832f4a1-79be-4fb2-ae93-6ba6efd209d2"       # getaight; never Wherehouse
AZURE_PRECONDITION = f"subscription == {AZURE_SUBSCRIPTION}"

# Credential NAMES only. The GCP file choice is MD-C3: the mi-battery file if MD-9 created it,
# else the aight-litellm service-account file. Which one was used is recorded on every attempt.
FAL_KEY_NAME = "FAL_KEY"
SARVAM_KEY_NAME = "SARVAM_API_KEY"
ELEVENLABS_KEY_NAME = "ELEVENLABS_API_KEY"
MI_KEYS_FILE = "~/.mi-keys"
GCP_CREDENTIAL_CANDIDATES = ("~/.mi-battery-keys/gcp-mi-battery-sa.json",
                             "~/.aight-litellm-keys/vertex-sa.json")
GCP_KEY_NAME = "gcloud auth print-access-token (service-account key file, MD-C3)"

VERTEX_PIN = "eval/empirical-planning/price-pins-2026-09/vertex-shared/vertex-generative-ai-pricing.html"
PINS = "eval/empirical-planning/price-pins-2026-09"
ELEVENLABS_PRICING_PIN = f"{PINS}/elevenlabs-direct/elevenlabs-pricing.html"

# 2026-09-09 Gemini Developer API surface (CONTROLLER-GEMINI-MODELS-VIA-GEMINI-KEY-2026-09-09 + CONTROLLER-FAL-LAST-CHOICE-CREDITS-FIRST):
# every Gemini-named model is called on generativelanguage.googleapis.com with the key NAMED GOOGLE_API_KEY in ~/.mi-keys (name only),
# billed as GCP credits via that key (pool `credits`). Veo / Lyria stay on Vertex. Pins: price-pins-2026-09/gemini-api/PIN-INDEX.yaml.
GEMINI_API_KEY_NAME = "GOOGLE_API_KEY"
GEMINI_API_MODELS = "https://generativelanguage.googleapis.com/v1beta/models"          # + /<id>:generateContent (image)
GEMINI_API_INTERACTIONS = "https://generativelanguage.googleapis.com/v1beta/interactions"   # Omni video (Interactions API)
GEMINI_API_PRICING_PIN = f"{PINS}/gemini-api-judge/gemini-api-pricing.html"
GEMINI_API_PIN_INDEX = f"{PINS}/gemini-api/PIN-INDEX.yaml"
GEMINI_API_SCHEMA = "eval/harness-v2/schemas/gemini_api/SCHEMA-INDEX.yaml"
GEMINI_API_BILLING_NOTE = "GCP credits via the Gemini API key"
GEMINI_API_PRICES = {   # exact strings on the pinned Gemini API pricing page (Standard tier); test_surfaces checks them against the bytes
    "gemini-3.1-flash-image": "$0.067 per 1K image",
    "gemini-3-pro-image": "$0.134 per 1K/2K image",
    "gemini-omni-1.1-flash": "$17.50 (video)",     # per 1M output tokens; "5,792 tokens per second of 720p video" -> 0.10136 USD/s derived
}
# Route keys whose registry surface / pool the freeze package (COST-TABLE route_catalogue, roster) has NOT yet been rebuilt for, as
# {route_key: (package surface, package pool)}. test_surfaces checks this table EXACTLY against the committed catalogue and dry_run.py lists
# every entry in the manifest. EMPTY since 2026-09-10: the roster records were re-pointed to gemini_api / credits and the package rebuilt
# (tools/build.py), so the catalogue, the roster and this registry agree for every Gemini-named key.
GEMINI_API_REPOINT_PENDING_PACKAGE: dict[str, tuple[str, str]] = {}
# Routes outside the freeze catalogue (no TEST-CASES / COST-TABLE row): registered so the adapter, ledger pool and cap
# are tested code, but never planned by run_live from the catalogue and never counted in the freeze reconciliation.
EXTENSION_ROUTES: tuple[str, ...] = ()   # 2026-09-09: the ElevenLabs direct routes entered the freeze catalogue (Controller decision); none left


@dataclass(frozen=True)
class SurfaceEntry:
    route_key: str
    adapter: str                      # fal_queue | vertex_veo | vertex_gemini_image | vertex_omni | gemini_api_image | gemini_api_omni | vertex_lyria | sarvam_tts | elevenlabs_direct | none
    surface: str                      # fal | vertex | gemini_api | sarvam_direct | elevenlabs_direct | bedrock | azure_foundry | cloud_tts
    surface_model_id: str
    endpoint: str
    params_schema: str                # pinned schema ref (path#Component) or a reason
    price_pin_ref: str | None
    billing_pool: str                 # cash | credits | sarvam_credits | elevenlabs_credits (plan credits, 0 USD cash)
    currency: str                     # USD | INR
    key_name: str
    credential_file_name: str
    shape_status: str                 # verified | unverified | not_built
    roster_key: str
    roster_variant: str | None
    workflow: str                     # t2i | edit | t2v | i2v | ref2v | extend | tts | lipsync | music
    lane: str                         # V1 lane vocabulary: image | general_video | native_av | lipsync | tts | music
    media_kind: str                   # image | video | audio
    dispatch_preconditions: tuple = ()
    api_calls_per_trial: int = 1
    notes: str = ""

    def as_dict(self) -> dict:
        d = asdict(self)
        d["dispatch_preconditions"] = list(self.dispatch_preconditions)
        return d


def _fal(key, model_id, schema_file, schema_input, roster_key, variant, workflow, lane, media_kind,
         pin, shape="verified", notes="", pool="cash"):
    return SurfaceEntry(
        route_key=key, adapter="fal_queue", surface="fal", surface_model_id=model_id,
        endpoint=f"{FAL_QUEUE}/{model_id}",
        params_schema=(f"eval/harness-v2/schemas/fal/{schema_file}#{schema_input}"
                       if schema_file else "no OpenAPI schema returned for this endpoint id"),
        price_pin_ref=pin, billing_pool=pool, currency="USD",
        key_name=FAL_KEY_NAME, credential_file_name=MI_KEYS_FILE, shape_status=shape,
        roster_key=roster_key, roster_variant=variant, workflow=workflow, lane=lane,
        media_kind=media_kind, notes=notes)


def _veo(key, model_id, variant, workflow, roster_key="veo-3.1-fast", calls=1, notes=""):
    return SurfaceEntry(
        route_key=key, adapter="vertex_veo", surface="vertex", surface_model_id=model_id,
        endpoint=f"{VERTEX_REGIONAL}/{model_id}:predictLongRunning",
        params_schema=("eval/harness-v2/schemas/vertex/SCHEMA-INDEX.yaml#veo "
                       "(VideoGenerationModelParams + VideoGenerationModelInstance + guide pages)"),
        price_pin_ref=VERTEX_PIN, billing_pool="credits", currency="USD",
        key_name=GCP_KEY_NAME, credential_file_name=" | ".join(GCP_CREDENTIAL_CANDIDATES),
        shape_status="verified", roster_key=roster_key, roster_variant=variant,
        workflow=workflow, lane="native_av" if workflow != "i2v" else "general_video",
        media_kind="video", api_calls_per_trial=calls, notes=notes)


def _omni(key, variant, notes=""):
    """Gemini Omni Flash on the Gemini Developer API (2026-09-09; before that the same routes ran on Vertex, adapter vertex_omni,
    model gemini-omni-1.1-flash-preview at VERTEX_INTERACTIONS - the Vertex adapter stays importable and tested, the registry rows
    are not duplicated because the catalogue key set is frozen). Draws already made on Vertex are evidence of the same model."""
    return SurfaceEntry(
        route_key=key, adapter="gemini_api_omni", surface="gemini_api",
        surface_model_id="gemini-omni-1.1-flash", endpoint=GEMINI_API_INTERACTIONS,
        params_schema=f"{GEMINI_API_SCHEMA}#omni_interactions (Gemini API Omni guide + model page + Interactions API reference)",
        price_pin_ref=GEMINI_API_PRICING_PIN, billing_pool="credits", currency="USD",
        key_name=GEMINI_API_KEY_NAME, credential_file_name=MI_KEYS_FILE,
        shape_status="verified", roster_key="gemini-omni-flash-1.1", roster_variant=variant,
        workflow="t2v", lane="native_av", media_kind="video",
        notes=(f"{GEMINI_API_BILLING_NOTE}; pinned Gemini API price (Standard): video output '{GEMINI_API_PRICES['gemini-omni-1.1-flash']}' per 1M "
               "tokens at '5,792 tokens per second of 720p video' = 0.10136 USD/s derived (the roster's figure, from the Vertex page); "
               "the roster record (re-pointed 2026-09-10) carries the same surface, id and pin"
               + (f"; {notes}" if notes else "")))


def _gemini_image(key, model_id, workflow, roster_key, notes=""):
    """Gemini image models on the Gemini Developer API (2026-09-09): the generateContent body the Vertex adapter sends, byte for byte,
    on generativelanguage.googleapis.com with the key NAMED GOOGLE_API_KEY. The Vertex rows are not kept under a -vertex suffix (the
    catalogue key set is frozen); adapters/vertex_gemini_image.py stays importable and tested."""
    return SurfaceEntry(
        route_key=key, adapter="gemini_api_image", surface="gemini_api", surface_model_id=model_id,
        endpoint=f"{GEMINI_API_MODELS}/{model_id}:generateContent",
        params_schema=f"{GEMINI_API_SCHEMA}#gemini_image (generateContent reference + image-generation guide; live-proven by "
                      "eval/experiments/EVAL-038/tools/generate_media.py on this surface)",
        price_pin_ref=GEMINI_API_PRICING_PIN, billing_pool="credits", currency="USD",
        key_name=GEMINI_API_KEY_NAME, credential_file_name=MI_KEYS_FILE, shape_status="verified",
        roster_key=roster_key, roster_variant=None, workflow=workflow, lane="image", media_kind="image",
        notes=f"{GEMINI_API_BILLING_NOTE}; pinned Gemini API price (Standard, 1K output, no imageSize sent): '{GEMINI_API_PRICES[model_id]}'"
              + (f"; {notes}" if notes else ""))


def _none(key, surface, model_id, roster_key, pool, workflow, lane, media_kind, pin, precond=(),
          notes="", currency="USD"):
    return SurfaceEntry(
        route_key=key, adapter="none", surface=surface, surface_model_id=model_id,
        endpoint="not_built_tonight", params_schema="no adapter (needs_controller_enablement, MD-9)",
        price_pin_ref=pin, billing_pool=pool, currency=currency,
        key_name="none (no adapter)", credential_file_name="none", shape_status="not_built",
        roster_key=roster_key, roster_variant=None, workflow=workflow, lane=lane,
        media_kind=media_kind, dispatch_preconditions=tuple(precond), notes=notes)


_ENTRIES: list[SurfaceEntry] = [
    # ---------------------------------------------------------------- image, text-to-image
    _fal("gpt-image-2", "openai/gpt-image-2", "openai_gpt-image-2.json", "GptImage2Input",
         "gpt-image-2", "fallback", "t2i", "image", "image",
         f"{PINS}/gpt-image-2/fal-openai-gpt-image-2.html",
         notes="quality=medium is pinned (README OQ-15 / MD-C8); the credit surface (Azure) is needs_controller_enablement"),
    _gemini_image("nano-banana-2", "gemini-3.1-flash-image", "t2i", "nano-banana-2",
                  notes="0.067 USD per 1K image, the same figure as the Vertex line the roster carried until its 2026-09-10 re-point"),
    _gemini_image("nano-banana-pro", "gemini-3-pro-image", "t2i", "nano-banana-pro",
                  notes="0.134 USD per 1K/2K image, the same figure as the Vertex line the roster carried until its 2026-09-10 re-point"),
    _fal("seedream-5-pro", "bytedance/seedream/v5/pro/text-to-image",
         "bytedance_seedream_v5_pro_text-to-image.json", "Seedream5ProTextToImageInput",
         "seedream-5-pro", None, "t2i", "image", "image",
         f"{PINS}/seedream-5-pro/fal-api-models-seedream-v5-pro-t2i.json"),
    _fal("flux-2-pro", "fal-ai/flux-2-pro", "fal-ai_flux-2-pro.json", "Flux2ProInput",
         "flux-2-pro", "fallback", "t2i", "image", "image",
         f"{PINS}/flux-2-pro/fal-api-models-flux-2-pro.json",
         notes="credit surface (Azure FLUX.2-pro) is needs_controller_enablement; fal fallback pinned"),
    _fal("qwen-image-3", "alibaba/qwen-image-3/text-to-image", "alibaba_qwen-image-3_text-to-image.json",
         "QwenImage3TextToImageInput", "qwen-image-3", None, "t2i", "image", "image",
         f"{PINS}/qwen-image-3/fal-api-models-qwen-image-3-t2i.json"),
    _none("sd3.5-large", "bedrock", "stability.sd3-5-large-v1:0", "sd3.5-large", "credits",
          "t2i", "image", "image",
          f"{PINS}/sd3.5-large/aws-bedrock-list-foundation-model-agreement-offers-sd3.5-large.json",
          notes="conditional; Bedrock adapter not built tonight (MD-4 / MD-9)"),
    _none("mai-image-2.6", "azure_foundry", "MAI-Image-2.6", "mai-image-2.6", "credits",
          "t2i", "image", "image", None, precond=(AZURE_PRECONDITION,),
          notes="conditional; unpinned price; Azure adapter not built tonight (MD-2 / MD-9)"),
    _fal("recraft-v4", "fal-ai/recraft/v4/text-to-image", "fal-ai_recraft_v4_text-to-image.json",
         "RecraftV4TextToImageInput", "recraft-v4", None, "t2i", "image", "image",
         f"{PINS}/recraft-v4/fal-recraft-v4-text-to-image.html"),
    # ---------------------------------------------------------------- image, edit / reference
    _fal("flux-2-pro-edit", "fal-ai/flux-2-pro/edit", "fal-ai_flux-2-pro_edit.json", "Flux2ProEditInput",
         "flux-2-pro-edit", None, "edit", "image", "image",
         f"{PINS}/flux-2-pro-edit/fal-api-models-flux-2-pro-edit.json",
         notes="price = 0.03 first output megapixel + 0.015 per input megapixel (roster price_addons)"),
    _gemini_image("nano-banana-pro-edit", "gemini-3-pro-image", "edit", "nano-banana-pro-edit",
                  notes="re-pointed 2026-09-09 from fal-ai/nano-banana-pro/edit (cash, 0.15 USD per image) to the same model on the Gemini API "
                        "(Controller: fal is the last choice); reference images go inline; the pinned page adds input images at "
                        "'Image input is set at 560 tokens' = '$0.0011 per image'. Roster re-pointed 2026-09-10 (surface gemini_api, id gemini-3-pro-image, "
                        "pool credits, regular_price 0.134 per_image, price_addons.input_image 0.0011, pin_ref the Gemini API pricing page): pricing.py "
                        "reserves the 0.134 output line per call; the input-image addon is recorded in the roster / COST-TABLE quantity rule, not projected"),
    _fal("seedream-5-pro-edit", "bytedance/seedream/v5/pro/edit", "bytedance_seedream_v5_pro_edit.json",
         "Seedream5ProEditInput", "seedream-5-pro-edit", None, "edit", "image", "image",
         f"{PINS}/seedream-5-pro-edit/fal-api-models-seedream-v5-pro-edit.json",
         notes="image_size pinned to auto_1K so the <= 1536x1536 price tier applies (default auto_2K would bill 0.135)"),
    _fal("gpt-image-2-edit", "openai/gpt-image-2/edit", "openai_gpt-image-2_edit.json", "GptImage2EditInput",
         "gpt-image-2-edit", None, "edit", "image", "image",
         f"{PINS}/gpt-image-2-edit/fal-api-models-openai-gpt-image-2-edit.json",
         notes="price unpinned (token meter only) - outside the cap, refuses live dispatch (MD-C9)"),
    # ---------------------------------------------------------------- video, text-to-video
    _veo("veo-3.1-fast", "veo-3.1-fast-generate-001", "t2v", "t2v"),
    _fal("kling-v3-pro-audio", "fal-ai/kling-video/v3/pro/text-to-video",
         "fal-ai_kling-video_v3_pro_text-to-video.json", "KlingVideoV3ProTextToVideoInput",
         "kling-v3-pro", "t2v-audio-on", "t2v", "native_av", "video",
         f"{PINS}/kling-v3-pro/fal-api-models-kling-v3-pro-t2v.json"),
    _fal("kling-v3-pro", "fal-ai/kling-video/v3/pro/text-to-video",
         "fal-ai_kling-video_v3_pro_text-to-video.json", "KlingVideoV3ProTextToVideoInput",
         "kling-v3-pro", "t2v", "t2v", "general_video", "video",
         f"{PINS}/kling-v3-pro/fal-api-models-kling-v3-pro-t2v.json"),
    _fal("minimax-h3-max", "minimax/h3-max/text-to-video", "minimax_h3-max_text-to-video.json",
         "MinimaxH3TurboTextToVideoInput", "minimax-h3-max", "t2v-768p", "t2v", "general_video", "video",
         f"{PINS}/minimax-h3-max/fal-api-models-minimax-h3-max-t2v.json",
         notes="fal's H3 Max is fal's own post-trained variant of MiniMax H3; no audio parameter exists in the schema"),
    _fal("wan-3.0-prime", "alibaba/wan-3.0-prime/text-to-video", "alibaba_wan-3.0-prime_text-to-video.json",
         "Wan3PrimeTextToVideoInput", "wan-3.0-prime", "t2v", "t2v", "native_av", "video",
         f"{PINS}/wan-3.0-prime/fal-api-models-wan-3.0-prime-t2v.json"),
    _fal("wan-2.2-a14b", "fal-ai/wan/v2.2-a14b/text-to-video", "fal-ai_wan_v2.2-a14b_text-to-video.json",
         "WanV22A14bTextToVideoInput", "wan-2.2-a14b", "t2v", "t2v", "general_video", "video",
         f"{PINS}/wan-2.2-a14b/fal-wan-v2.2-a14b-text-to-video-2026-09-09.html",
         notes="Wan 2 contender (Controller decision 2026-09-09): the cheapest live Wan 2.x tier on fal that renders the 6-s / 8-s rows; pinned USD 0.08 per "
               "video second at 720p from the exact id's endpointBilling record and prose; silent family (no audio field in the pinned schema); "
               "num_frames = 16 x duration + 1; rows only where Wan 3.0 Prime passed"),
    _omni("gemini-omni-1.1-flash", "t2v"),
    _fal("seedance-2.5", "bytedance/seedance-2.5/text-to-video", "bytedance_seedance-2.5_text-to-video.json",
         "Seedance25TextToVideoInput", "seedance-2.5", "t2v", "t2v", "native_av", "video",
         f"{PINS}/seedance-2.5/fal-api-models-seedance-2.5-t2v.json"),
    _none("sora-2", "azure_foundry", "sora-2", "sora-2", "credits", "t2v", "general_video", "video",
          f"{PINS}/sora-2/azure-retail-prices-sora-2.json", precond=(AZURE_PRECONDITION,),
          notes="conditional; Azure adapter not built tonight (MD-2 / MD-9)"),
    _veo("veo-3.1-lite", "veo-3.1-lite-generate-001", None, "t2v", roster_key="veo-3.1-lite"),
    _veo("veo-3.1-full", "veo-3.1-generate-001", None, "t2v", roster_key="veo-3.1-full"),
    _fal("minimax-h3-max-480p", "minimax/h3-max/text-to-video", "minimax_h3-max_text-to-video.json",
         "MinimaxH3TurboTextToVideoInput", "minimax-h3-max", "t2v-480p", "t2v", "general_video", "video",
         f"{PINS}/minimax-h3-max/fal-api-models-minimax-h3-max-t2v.json"),
    # ---------------------------------------------------------------- video, image-to-video
    _veo("veo-3.1-fast-i2v", "veo-3.1-fast-generate-001", "i2v", "i2v"),
    _fal("kling-v3-pro-i2v", "fal-ai/kling-video/v3/pro/image-to-video",
         "fal-ai_kling-video_v3_pro_image-to-video.json", "KlingVideoV3ProImageToVideoInput",
         "kling-v3-pro", "i2v", "i2v", "general_video", "video",
         f"{PINS}/kling-v3-pro/fal-api-models-kling-v3-pro-i2v.json"),
    _fal("minimax-h3-max-i2v", "minimax/h3-max/image-to-video", "minimax_h3-max_image-to-video.json",
         "MinimaxH3TurboImageToVideoInput", "minimax-h3-max", "i2v-768p", "i2v", "general_video", "video",
         f"{PINS}/minimax-h3-max/fal-api-models-minimax-h3-max-i2v.json"),
    _fal("wan-3.0-prime-i2v", "alibaba/wan-3.0-prime/image-to-video", "alibaba_wan-3.0-prime_image-to-video.json",
         "Wan3PrimeImageToVideoInput", "wan-3.0-prime", "i2v", "i2v", "general_video", "video",
         f"{PINS}/wan-3.0-prime/fal-api-models-wan-3.0-prime-i2v.json"),
    _fal("wan-2.2-a14b-i2v", "fal-ai/wan/v2.2-a14b/image-to-video", "fal-ai_wan_v2.2-a14b_image-to-video.json",
         "WanV22A14bImageToVideoInput", "wan-2.2-a14b", "i2v", "i2v", "general_video", "video",
         f"{PINS}/wan-2.2-a14b/fal-wan-v2.2-a14b-image-to-video-2026-09-09.html",
         notes="Wan 2 contender (Controller decision 2026-09-09): image-to-video on the same accepted stills as the wan-3.0-prime-i2v rows; pinned USD 0.08 per "
               "video second at 720p (exact id's endpointBilling record); silent family; aspect follows the plate (schema default auto)"),
    _fal("seedance-2.5-i2v", "bytedance/seedance-2.5/image-to-video", "bytedance_seedance-2.5_image-to-video.json",
         "Seedance25ImageToVideoInput", "seedance-2.5", "i2v", "i2v", "general_video", "video",
         f"{PINS}/seedance-2.5/fal-api-models-seedance-2.5-i2v.json"),
    _veo("veo-3.1-lite-i2v", "veo-3.1-lite-generate-001", None, "i2v", roster_key="veo-3.1-lite",
         notes="price unpinned (no Lite image-input variant in the roster) - outside the cap, refuses live dispatch (MD-C9 / OQ-3)"),
    # ---------------------------------------------------------------- video, reference-to-video
    _fal("seedance-2.5-ref2v", "bytedance/seedance-2.5/reference-to-video",
         "bytedance_seedance-2.5_reference-to-video.json", "Seedance25ReferenceToVideoInput",
         "seedance-2.5", "ref2v", "ref2v", "general_video", "video",
         f"{PINS}/seedance-2.5/fal-api-models-seedance-2.5-ref2v.json"),
    _veo("veo-3.1-fast-ref2v", "veo-3.1-fast-generate-001", "ref2v", "ref2v"),
    _fal("kling-v3-elements", "fal-ai/kling-video/v3/pro/elements", None, None,
         "kling-v3-pro", "elements-ref2v", "ref2v", "general_video", "video", None, shape="unverified",
         notes="conditional and unpinned: fal has no model under this endpoint id (re-checked 2026-09-09: model page and /api sub-page HTTP 404, "
               "the id is absent from fal's own keyword search, the schema endpoint answers 'OpenAPI schema not available'; bytes in "
               f"{PINS}/kling-v3-elements/PIN-INDEX.yaml). No price exists for this route; the nearest live ids (kling-video/v1.6/pro/elements, "
               "kling-video/o3/pro/reference-to-video) are other models and are not pinned to this key"),
    # ---------------------------------------------------------------- video, longer / multi-shot
    _fal("kling-v3-pro-15s", "fal-ai/kling-video/v3/pro/text-to-video",
         "fal-ai_kling-video_v3_pro_text-to-video.json", "KlingVideoV3ProTextToVideoInput",
         "kling-v3-pro", "15s", "t2v", "native_av", "video",
         f"{PINS}/kling-v3-pro/fal-api-models-kling-v3-pro-t2v.json"),
    _fal("seedance-2.5-15s", "bytedance/seedance-2.5/text-to-video", "bytedance_seedance-2.5_text-to-video.json",
         "Seedance25TextToVideoInput", "seedance-2.5", "15s", "t2v", "native_av", "video",
         f"{PINS}/seedance-2.5/fal-api-models-seedance-2.5-t2v.json"),
    _omni("gemini-omni-1.1-flash-long", "multishot-10s",
          notes="the pinned Vertex page caps Omni Flash at 10 s (duration '3s'..'10s'); the case row bills 15 s at the "
                "multishot-10s variant rate (COST-TABLE rule) - the body renders 10 s and the manifest explains the delta"),
    _veo("veo-3.1-fast-extend", "veo-3.1-fast-generate-001", "extend-15s", "extend", calls=2,
         notes="one trial = two API calls: 8-s generate then extend (fixed 7 s per the pinned extend page); 15 billed seconds"),
    _fal("kling-v3-pro-10s", "fal-ai/kling-video/v3/pro/text-to-video",
         "fal-ai_kling-video_v3_pro_text-to-video.json", "KlingVideoV3ProTextToVideoInput",
         "kling-v3-pro", "multishot-10s", "t2v", "native_av", "video",
         f"{PINS}/kling-v3-pro/fal-api-models-kling-v3-pro-t2v.json"),
    _omni("gemini-omni-1.1-flash-10s", "multishot-10s"),
    # ---------------------------------------------------------------- audio, TTS
    SurfaceEntry(route_key="sarvam-bulbul-v3", adapter="sarvam_tts", surface="sarvam_direct",
                 surface_model_id="bulbul:v3", endpoint=SARVAM_TTS,
                 params_schema="eval/harness-v2/schemas/sarvam/SCHEMA-INDEX.yaml#text-to-speech",
                 price_pin_ref=f"{PINS}/sarvam-bulbul-v3/sarvam-api-pricing.html",
                 billing_pool="sarvam_credits", currency="INR",
                 key_name=SARVAM_KEY_NAME, credential_file_name=MI_KEYS_FILE, shape_status="verified",
                 roster_key="sarvam-bulbul-v3", roster_variant=None, workflow="tts", lane="tts",
                 media_kind="audio", notes="INR per 1,000 characters; USD-equivalent at the display rate 95.4211 for the cap only"),
    _fal("elevenlabs-v3", "fal-ai/elevenlabs/tts/eleven-v3", "fal-ai_elevenlabs_tts_eleven-v3.json",
         "ElevenlabsTtsElevenV3Input", "elevenlabs-v3", None, "tts", "tts", "audio",
         f"{PINS}/elevenlabs-v3/fal-elevenlabs-tts-eleven-v3.html"),
    _none("chirp-3-hd-hi-in", "cloud_tts", "hi-IN-Chirp3-HD-*", "chirp-3-hd-hi-in", "credits",
          "tts", "tts", "audio", None,
          notes="conditional; unpinned; Cloud Text-to-Speech API not enabled; no adapter tonight (MD-9)"),
    _none("azure-neural-tts-hi-in", "azure_foundry", "Azure Speech S1 Neural Text To Speech (hi-IN voice)",
          "azure-neural-tts-hi-in", "credits", "tts", "tts", "audio",
          f"{PINS}/azure-neural-tts-hi-in/azure-retail-prices-speech-neural-centralindia.json",
          precond=(AZURE_PRECONDITION,), notes="conditional; Azure adapter not built tonight (MD-9)"),
    # ---------------------------------------------------------------- audio, lip-sync
    _fal("sync-lipsync-v3", "fal-ai/sync-lipsync/v3", "fal-ai_sync-lipsync_v3.json", "SyncLipsyncV3Input",
         "sync-lipsync-v3", None, "lipsync", "lipsync", "video",
         f"{PINS}/sync-lipsync-v3/fal-sync-lipsync-v3-2026-09-09.html",
         notes="price evidence pinned 2026-09-09 for the EXACT id: the model page's endpointBilling record reads billing_unit 'minutes', price 8 "
               "(USD 8.00 per output minute = 0.1333/s; the prose 0.1333/s string still belongs to the sibling image-to-video endpoint - Auditor AF-1). "
               f"Index: {PINS}/sync-lipsync-v3/PIN-INDEX.yaml. The roster and the freeze package still carry the route unpinned (roster sha256 is bound "
               "to the running lane; rebuild staged) - outside the cap, refuses live dispatch until the package is rebuilt (MD-C9)"),
    _fal("kling-lipsync-a2v", "fal-ai/kling-video/lipsync/audio-to-video",
         "fal-ai_kling-video_lipsync_audio-to-video.json", "KlingVideoLipsyncAudioToVideoInput",
         "kling-lipsync-audio-to-video", None, "lipsync", "lipsync", "video",
         f"{PINS}/kling-lipsync-audio-to-video/fal-api-models-kling-lipsync-a2v.json",
         notes="bills input video seconds rolled up to the next 5-s increment"),
    # ---------------------------------------------------------------- music
    SurfaceEntry(route_key="lyria", adapter="vertex_lyria", surface="vertex", surface_model_id="lyria-002",
                 endpoint=f"{VERTEX_REGIONAL}/lyria-002:predict",
                 params_schema="eval/harness-v2/schemas/vertex/SCHEMA-INDEX.yaml#lyria",
                 price_pin_ref=VERTEX_PIN, billing_pool="credits", currency="USD",
                 key_name=GCP_KEY_NAME, credential_file_name=" | ".join(GCP_CREDENTIAL_CANDIDATES),
                 shape_status="verified", roster_key="lyria", roster_variant=None, workflow="music",
                 lane="tts", media_kind="audio",
                 notes="lyria-002 is the only Lyria id the publisher endpoint answers (MD-7 / MD-C7); 30-s WAV per clip"),
    _fal("elevenlabs-music", "fal-ai/elevenlabs/music", "fal-ai_elevenlabs_music.json", "ElevenlabsMusicInput",
         "elevenlabs-music", None, "music", "tts", "audio",
         f"{PINS}/elevenlabs-music/fal-api-models-elevenlabs-music.json",
         notes="bills per output minute rounded up (30 s -> 1 minute)"),
    # ---------------------------------------------------------------- EXTENSION_ROUTES: ElevenLabs DIRECT (plan credits)
    SurfaceEntry(route_key="elevenlabs-v3-direct", adapter="elevenlabs_direct", surface="elevenlabs_direct",
                 surface_model_id="eleven_v3", endpoint=ELEVENLABS_TTS,
                 params_schema="eval/harness-v2/schemas/elevenlabs/SCHEMA-INDEX.yaml#elevenlabs_tts",
                 price_pin_ref=ELEVENLABS_PRICING_PIN, billing_pool="elevenlabs_credits", currency="USD",
                 key_name=ELEVENLABS_KEY_NAME, credential_file_name=MI_KEYS_FILE, shape_status="verified",
                 roster_key="elevenlabs-v3", roster_variant=None, workflow="tts", lane="tts", media_kind="audio",
                 notes="direct API on the user's account: 0 USD cash, plan credits recorded natively (pinned pricing page: "
                       "'Text to Speech 1 credit per character'); roster_key names the fal row of the same model, which pricing.py "
                       "does NOT use for this pool; capped by elevenlabs_cap_credits"),
    SurfaceEntry(route_key="elevenlabs-music-direct", adapter="elevenlabs_direct", surface="elevenlabs_direct",
                 surface_model_id="music_v1", endpoint=ELEVENLABS_MUSIC,
                 params_schema="eval/harness-v2/schemas/elevenlabs/SCHEMA-INDEX.yaml#elevenlabs_music",
                 price_pin_ref=ELEVENLABS_PRICING_PIN, billing_pool="elevenlabs_credits", currency="USD",
                 key_name=ELEVENLABS_KEY_NAME, credential_file_name=MI_KEYS_FILE, shape_status="verified",
                 roster_key="elevenlabs-music", roster_variant=None, workflow="music", lane="music", media_kind="audio",
                 notes="direct API on the user's account: 0 USD cash, plan credits recorded natively (pinned pricing page: "
                       "'Eleven Music 900 credits per minute', whole minutes rounded up); roster_key names the fal row of the same "
                       "model, which pricing.py does NOT use for this pool; capped by elevenlabs_cap_credits"),
]


class SurfaceRegistry:
    """The 47 route keys and their surfaces, plus EXTENSION_ROUTES. Set equality with the route catalogue is tested."""

    def __init__(self, entries: Iterable[SurfaceEntry] = _ENTRIES):
        self._entries: dict[str, SurfaceEntry] = {}
        for e in entries:
            if e.route_key in self._entries:
                raise ValueError(f"duplicate route_key {e.route_key!r} in SurfaceRegistry")
            self._entries[e.route_key] = e

    def keys(self) -> set[str]:
        return set(self._entries)

    def catalogue_keys(self) -> set[str]:
        """The freeze catalogue's keys: every registry key that is not an extension route."""
        return set(self._entries) - set(EXTENSION_ROUTES)

    def get(self, route_key: str) -> SurfaceEntry:
        try:
            return self._entries[route_key]
        except KeyError:
            raise KeyError(
                f"route_key {route_key!r} is not in SurfaceRegistry; the registry covers exactly the "
                f"route_catalogue keys of TEST-CASES.yaml and adding one is a Controller decision") from None

    def __iter__(self):
        return iter(self._entries.values())

    def __len__(self):
        return len(self._entries)

    def by_adapter(self, adapter: str) -> list[SurfaceEntry]:
        return [e for e in self._entries.values() if e.adapter == adapter]

    def as_dict(self) -> dict:
        return {k: v.as_dict() for k, v in self._entries.items()}


REGISTRY = SurfaceRegistry()
