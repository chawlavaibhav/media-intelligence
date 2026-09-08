"""Deterministic instruments for the Stage A battery (task EVAL-039C §3).

    imageio             stdlib PNG codec + ffmpeg/ffprobe wrappers (the only local-subprocess decoders)
    common              PASS-CRITERIA loader, the frozen-gate rule, result shapes, Instrument factory
    format_probe        container / size / aspect / duration / fps / audio presence  -> delivery_format_compliance, reliability_pass_at_k
    masked_diff         MAE + SSIM outside a mask                                     -> edit_preservation
    brand_colour        CIELAB dE*ab (CIE76) of the mean colour inside a mask          -> packaging_brand_colour_fidelity
    av_offset           audio-track offset vs the drive we supplied (partial claim)   -> audio_video_synchronisation (MD-C6)
    repeat_consistency  dHash Hamming + SSIM between repeats, unseeded / held apart   -> reproducibility
    ledger_metrics      latency, status counts, refusal rate, settled cost             -> latency_errors_refusals, cost_and_cpao
    gate_wrapper        canon/gate/run_gate.py post, observation only, provisional
    registry_gate       the only path to a Registry row: capability + instrument eligibility, uncertainty

Every instrument fails closed (unparseable input -> absent / parse_failure) and, while its entry in
PASS-CRITERIA-v0.yaml says `frozen: false`, stores its measurement but returns absent / other with the
note `criterion_not_frozen` (Controller between-role note 4). No third-party Python is imported.
"""
