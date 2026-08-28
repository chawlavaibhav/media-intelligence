"""Request construction: exact provider contract, frozen identity, refusal before reserve."""
from decimal import Decimal

import pytest

import video_route as VR
from video_route import PilotVideoRoute


def test_build_body_matches_documented_contract():
    """The body carries exactly the documented fields, with the frozen pins applied."""
    route = PilotVideoRoute()
    body = route.build_body("A 6 second product shot of a prepaid wallet card", 6, "16:9")
    assert body == {
        "prompt": "A 6 second product shot of a prepaid wallet card",
        "duration": "6s",              # the provider enum is the string form
        "aspect_ratio": "16:9",
        "resolution": "720p",
        "generate_audio": True,
        "auto_fix": False,             # pinned: no silent prompt substitution, ever
    }
    assert "seed" not in body          # unseeded by policy, so the key never travels


def test_route_identity_is_frozen_and_version_pinned():
    route = PilotVideoRoute()
    ident = route.identity()
    assert ident["route"] == "fal-ai/veo3.1"
    assert ident["provider_surface"] == "fal"
    assert ident["model_family"] == "veo-3.1"
    assert ident["workflow_mode"] == "t2v"
    assert ident["route_version_pinned_in_path"] is True
    assert route.submit_url() == "https://queue.fal.run/fal-ai/veo3.1"
    assert route.request_url("abc", "/status") == \
        "https://queue.fal.run/fal-ai/veo3.1/requests/abc/status"


def test_unknown_slot_refused():
    with pytest.raises(ValueError, match="Controller decision"):
        PilotVideoRoute(slot="VID-SOMETHING-ELSE")


@pytest.mark.parametrize("prompt,duration,aspect", [
    ("", 6, "16:9"),                   # empty prompt
    ("   ", 6, "16:9"),                # whitespace prompt
    ("ok", 5, "16:9"),                 # duration outside the provider enum {4,6,8}
    ("ok", 6, "1:1"),                  # aspect outside the provider enum
])
def test_invalid_parameters_refused_before_anything_is_reserved_or_sent(
        guard, transport, fal_key, tmp_path, prompt, duration, aspect):
    route = PilotVideoRoute(transport=transport, guard=guard)
    with pytest.raises(ValueError):
        route.generate(prompt, duration, aspect, tmp_path)
    assert transport.submit_calls == []        # nothing was sent
    assert guard.reservations == []            # nothing was even reserved
    assert guard.spent_usd == Decimal("0")


def test_estimate_uses_committed_per_second_planning_rate():
    """USD 0.40/generated second with audio — the Controller's Veo pricing correction."""
    route = PilotVideoRoute()
    assert route.estimate_usd(6) == Decimal("2.40")
    assert route.estimate_usd(8) == Decimal("3.20")
    assert VR.VIDEO_ROUTES["VID-PILOT-01"]["billing_unit"] == "per_generated_second"
