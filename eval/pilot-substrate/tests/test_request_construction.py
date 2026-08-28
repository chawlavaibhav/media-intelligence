"""Request construction: exact Gemini/Veo contract, frozen identity, refusal before reserve."""
from decimal import Decimal

import pytest

import video_route as VR
from video_route import GeminiVeoRoute


def test_build_body_matches_documented_predict_long_running_contract():
    """The body carries exactly the documented fields, with the frozen pins applied."""
    route = GeminiVeoRoute()
    body = route.build_body("A festive premium motion plate", 8, "9:16")
    assert body == {
        "instances": [{"prompt": "A festive premium motion plate"}],
        "parameters": {
            "aspectRatio": "9:16",
            "durationSeconds": 8,
            "resolution": "720p",       # pinned for T1
        },
    }
    # No invented parameters: audio is native (no parameter exists), no seed, no
    # personGeneration policy decided here.
    assert "seed" not in body["parameters"]
    assert "personGeneration" not in body["parameters"]
    assert "generateAudio" not in body["parameters"]


def test_nine_sixteen_aspect_for_the_aight_pilot():
    route = GeminiVeoRoute()
    body = route.build_body("p", 8, "9:16")
    assert body["parameters"]["aspectRatio"] == "9:16"


def test_exact_model_identifier_and_endpoint():
    route = GeminiVeoRoute()
    ident = route.identity()
    assert ident["model_id"] == "veo-3.1-fast-generate-preview"
    assert ident["model_version"] == "veo-3.1-fast-generate-preview"
    assert ident["provider"] == "google"
    assert ident["provider_surface"] == "gemini-developer-api"
    assert ident["workflow"] == "t2v"
    assert ident["lane"] == "native_av"
    assert route.submit_url() == (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "veo-3.1-fast-generate-preview:predictLongRunning")
    assert route.operation_url("models/x/operations/op1") == (
        "https://generativelanguage.googleapis.com/v1beta/models/x/operations/op1")


def test_unknown_slot_refused():
    with pytest.raises(ValueError, match="Controller decision"):
        GeminiVeoRoute(slot="VID-SOMETHING-ELSE")


@pytest.mark.parametrize("prompt,duration,aspect", [
    ("", 8, "9:16"),                   # empty prompt
    ("   ", 8, "9:16"),                # whitespace prompt
    ("ok", 5, "9:16"),                 # duration outside the provider enum {4,6,8}
    ("ok", 12, "9:16"),                # 12s is the FIXTURE length, not a Veo duration
    ("ok", 8, "1:1"),                  # aspect outside the provider enum
])
def test_invalid_parameters_refused_before_anything_is_reserved_or_sent(
        guard, transport, gemini_key, tmp_path, prompt, duration, aspect):
    route = GeminiVeoRoute(transport=transport, guard=guard)
    with pytest.raises(ValueError):
        route.generate(prompt, duration, aspect, tmp_path)
    assert transport.submit_calls == []        # nothing was sent
    assert guard.reservations == []            # nothing was even reserved
    assert guard.spent_usd == Decimal("0")


def test_estimate_uses_current_official_per_second_rate():
    """USD 0.10/generated second, 720p, audio included — official pricing page."""
    route = GeminiVeoRoute()
    assert route.estimate_usd(8) == Decimal("0.80")
    assert route.estimate_usd(4) == Decimal("0.40")
    assert VR.VIDEO_ROUTES["VID-PILOT-01"]["billing_unit"] == "per_generated_second"
