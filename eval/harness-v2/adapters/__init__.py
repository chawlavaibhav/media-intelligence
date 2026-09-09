"""Route adapters for the Stage A battery. One dispatch = one trial, always.

    base                 the shared contract: build_request() feeds BOTH dry_run() and dispatch()
    fal_queue            queue.fal.run submit -> status -> response -> CDN download
    vertex_veo           :predictLongRunning -> :fetchPredictOperation (t2v / i2v / ref2v / extend)
    vertex_gemini_image  :generateContent on the global endpoint (image bytes inline)
    vertex_omni          /locations/global/interactions (Gemini Omni Flash video)
    vertex_lyria         lyria-002:predict (30-s WAV inline)
    sarvam_tts           api.sarvam.ai/text-to-speech (WAV inline)
    elevenlabs_direct    api.elevenlabs.io/v1/text-to-speech/{voice_id} and /v1/music (mp3 bytes; plan credits)

Nothing here contacts a provider by itself: every adapter needs an injected transport, an open
battery ledger and a sealed store before `dispatch()` does anything, and `build_request()` /
`dry_run()` never need any of them.
"""
from __future__ import annotations

from . import base as base  # noqa: F401


def adapter_for(entry, **kw):
    """Construct the adapter family named by a SurfaceEntry, or a NullAdapter for `adapter: none`."""
    from . import elevenlabs_direct, fal_queue, sarvam_tts, vertex_gemini_image, vertex_lyria, vertex_omni, vertex_veo
    families = {
        "fal_queue": fal_queue.FalQueueAdapter,
        "vertex_veo": vertex_veo.VertexVeoAdapter,
        "vertex_gemini_image": vertex_gemini_image.VertexGeminiImageAdapter,
        "vertex_omni": vertex_omni.VertexOmniAdapter,
        "vertex_lyria": vertex_lyria.VertexLyriaAdapter,
        "sarvam_tts": sarvam_tts.SarvamTTSAdapter,
        "elevenlabs_direct": elevenlabs_direct.ElevenLabsDirectAdapter,
    }
    cls = families.get(entry.adapter, base.NullAdapter)
    return cls(entry, **kw)
