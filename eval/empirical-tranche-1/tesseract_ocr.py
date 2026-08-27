#!/usr/bin/env python3
"""EVAL-023 — local literal OCR candidate: Tesseract 5 with the dictionary priors removed.

WHAT THIS EXPERIMENT IS ACTUALLY TESTING

    Sonnet 5, Gemini 3.5 Flash-Lite and Cloud Vision TEXT_DETECTION all failed the same gate the
    same way: shown a rendered word with a deliberate corruption, they returned the word that was
    MEANT rather than the glyphs that were DRAWN. Three failures with one shape.

    Every one of those systems has a language prior. A generative model has one by construction;
    Cloud Vision has one because a general OCR service is tuned to produce plausible text. The
    hypothesis here is narrow and falsifiable: that the auto-correction is the language prior
    doing its job, and that removing the prior removes the failure.

    Tesseract is the right instrument for that question because the prior is a discrete,
    documented, switchable component — six dictionary files — rather than something diffused
    through the weights. Turn them off and the same engine reads the same pixels without a
    vocabulary to snap toward.

    If this candidate ALSO auto-corrects with every dictionary disabled, the mechanism is not the
    lexicon and the programme's working explanation is wrong. That is a result worth having.

WHY PSM 13 AND OEM 1

    Tesseract's documentation describes PSM 13 as "raw line" — treat the image as a single text
    line, bypassing Tesseract-specific hacks. The battery is single words and short lines, and
    the hacks are exactly the layer we are trying not to measure. OEM 1 is the LSTM engine only,
    so the legacy engine's own heuristics are not silently mixed in.

FROZEN BEFORE ANY RESULT WAS READ

    Every value below was committed before a single battery image was passed to Tesseract. The
    configuration fingerprint binds the binary version, both traineddata hashes, the languages,
    the engine mode, the page-segmentation mode and all six dictionary flags — so "which
    Tesseract was this" is answerable from the evidence rather than from memory.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Callable

from providers import AmbiguousDispatch, DispatchRefused, EvaluatorResponse, verify_blind_payload

CANDIDATE_ALIAS = "tesseract5-hin-eng-literal-psm13-v1"
LANGUAGES = "hin+eng"
OEM = "1"          # LSTM only
PSM = "13"         # raw line: one text line, no Tesseract-specific hacks

# Every lexical aid Tesseract exposes, all off. This is the independent variable of the whole
# experiment; if any one of these silently flipped back on, the run would measure nothing.
DAWG_FLAGS = (
    ("load_system_dawg", "0"),
    ("load_freq_dawg", "0"),
    ("load_unambig_dawg", "0"),
    ("load_bigram_dawg", "0"),
    ("load_punc_dawg", "0"),
    ("load_number_dawg", "0"),
)

# Pinned official tessdata_best provenance. Tag rather than branch head: a branch moves.
TESSDATA_SOURCE = "https://github.com/tesseract-ocr/tessdata_best"
TESSDATA_TAG = "4.1.0"
TESSDATA_COMMIT = "e2aad9b983032bb1beff9133104a67cdbb87ca4d"

# Local, not a paid API. The ledger must record zero provider spend for this candidate.
USD_PER_EXECUTION = Decimal("0")

DEFAULT_TESSDATA_DIR = (Path(__file__).resolve().parent / "text_qualification" / "build"
                        / "tessdata")


class TesseractUnavailable(RuntimeError):
    """Tesseract is missing, the wrong major version, or its traineddata is absent."""


def tesseract_version(binary: str = "tesseract") -> str:
    """The exact build string, read from the binary rather than assumed."""
    path = shutil.which(binary)
    if not path:
        raise TesseractUnavailable(
            f"{binary!r} is not on PATH. EVAL-023 requires a local Tesseract 5.x.")
    out = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=30)
    first = (out.stdout or out.stderr).strip().splitlines()[0].strip()
    if not first.startswith("tesseract 5"):
        raise TesseractUnavailable(
            f"EVAL-023 requires Tesseract 5.x; found {first!r}. A different major version is a "
            f"different instrument, not a variant of this one.")
    return first


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class TesseractLiteralOcr:
    """One frozen Tesseract configuration, behind an injected subprocess seam.

    ONE FRESH PROCESS PER TRIAL, DELIBERATELY

        Tesseract can be driven as a long-lived API, and that would be faster. It would also let
        state — adaptive classifier data in particular — carry from one image to the next, so
        trial N would be scored by an engine that had already seen trials 1..N-1. That is not the
        same measurement, and the contamination would be invisible in the output. A fresh process
        per trial costs wall-clock and buys independence.
    """

    family: str = field(init=False, default="ocr")
    provider: str = field(init=False, default="local_tesseract")
    config_alias: str = CANDIDATE_ALIAS
    binary: str = "tesseract"
    tessdata_dir: Path = field(default_factory=lambda: DEFAULT_TESSDATA_DIR)
    timeout_s: float = 120.0
    runner: Callable | None = None          # injected subprocess seam; None = real subprocess
    guard: object | None = None
    call_context: dict = field(default_factory=dict)
    _version: str | None = field(init=False, default=None)
    _hashes: dict | None = field(init=False, default=None)

    # -- provenance --------------------------------------------------------------------------
    def version(self) -> str:
        if self._version is None:
            self._version = tesseract_version(self.binary)
        return self._version

    def traineddata_hashes(self) -> dict:
        if self._hashes is None:
            files = {}
            for lang in LANGUAGES.split("+"):
                p = self.tessdata_dir / f"{lang}.traineddata"
                if not p.exists():
                    raise TesseractUnavailable(
                        f"{p} is missing. EVAL-023 pins official tessdata_best {TESSDATA_TAG}; "
                        f"a run that cannot name the model it used is not reproducible.")
                files[f"{lang}.traineddata"] = _sha256(p)
            self._hashes = files
        return self._hashes

    def identity(self) -> dict:
        return {
            "family": self.family,
            "provider": self.provider,
            "config_alias": self.config_alias,
            "tesseract_version": self.version(),
            "languages": LANGUAGES,
            "oem": OEM,
            "psm": PSM,
            "dawg_flags": {k: v for k, v in DAWG_FLAGS},
            "tessdata_source": TESSDATA_SOURCE,
            "tessdata_tag": TESSDATA_TAG,
            "tessdata_commit": TESSDATA_COMMIT,
            "traineddata_sha256": self.traineddata_hashes(),
            "one_process_per_trial": True,
            "preprocessing": "none",
            "user_words": None,
            "config_pinned_at_execution": True,
        }

    def config_sha256(self) -> str:
        """Binds version, both traineddata hashes, languages, OEM, PSM and every DAWG flag."""
        return hashlib.sha256(
            json.dumps(self.identity(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    # -- command building (no execution) -----------------------------------------------------
    def build_command(self, image_path: str) -> list[str]:
        """Blind by construction: takes a path and nothing else.

        The image path is a caller-owned temp file whose name is derived from the trial
        coordinates, never from the target.
        """
        cmd = [self.binary, image_path, "stdout",
               "--tessdata-dir", str(self.tessdata_dir),
               "-l", LANGUAGES, "--oem", OEM, "--psm", PSM]
        for key, value in DAWG_FLAGS:
            cmd += ["-c", f"{key}={value}"]
        return cmd

    def subprocess_env(self) -> dict:
        """A minimal, explicit environment. The parent environment is NOT inherited wholesale.

        Inheriting os.environ would carry provider API keys into a subprocess that has no business
        seeing them, and would also make the run depend on whatever happened to be exported.
        """
        return {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "TESSDATA_PREFIX": str(self.tessdata_dir),
            "LC_ALL": "C.UTF-8",
            "LANG": "C.UTF-8",
        }

    # -- execution ---------------------------------------------------------------------------
    def transcribe(self, image_bytes: bytes, blind_check_target: str = "",
                   trial_id: str = "trial") -> EvaluatorResponse:
        """One image, one fresh process, one trial. No retry, ever."""
        safe_name = "".join(ch if (ch.isalnum() or ch in "-_.") else "_" for ch in trial_id)

        with tempfile.TemporaryDirectory(prefix="eval023-") as tmp:
            image_path = os.path.join(tmp, f"{safe_name}.png")
            Path(image_path).write_bytes(image_bytes)

            cmd = self.build_command(image_path)
            env = self.subprocess_env()

            # BLINDNESS, mechanically. The command, the path and the environment are all checked
            # for the target before anything executes — the same rule the API families are held
            # to, applied to a local process.
            payload = {"command": cmd, "image_path": image_path, "env": env}
            violations = verify_blind_payload(payload, "transcribe", blind_check_target)
            if violations:
                raise DispatchRefused(
                    "BLINDNESS VIOLATION — refusing to execute: " + "; ".join(violations))

            started = time.monotonic()
            try:
                result = (self.runner or _run_subprocess)(cmd, env, self.timeout_s)
            except Exception as exc:                      # noqa: BLE001
                # A local process that crashed, timed out or could not be launched is
                # INFRASTRUCTURE. It says nothing about recognition quality.
                return EvaluatorResponse(
                    "", None, None, USD_PER_EXECUTION, None, "error",
                    f"local_execution_{type(exc).__name__.lower()}",
                    cost_basis="local_zero_cost",
                    raw_status_note=str(exc)[:200],
                    billing_state="reported", ambiguous_dispatch=False)
            elapsed = time.monotonic() - started

        returncode, stdout, stderr = result
        if returncode != 0:
            return EvaluatorResponse(
                "", None, None, USD_PER_EXECUTION, None, "error",
                f"local_execution_exit_{returncode}", cost_basis="local_zero_cost",
                raw_status_note=(stderr or "")[:200], billing_state="reported",
                ambiguous_dispatch=False)

        text = (stdout or "").strip()
        if not text:
            # THE OCR-FAMILY RULE, unchanged: the process succeeded and read nothing from an image
            # a human confirmed carries visible text. Scientific evidence, never a match.
            return EvaluatorResponse(
                "", None, None, USD_PER_EXECUTION, None, "error", "empty_transcription",
                cost_basis="local_zero_cost",
                raw_status_note=f"exit 0, empty stdout, {elapsed:.3f}s",
                billing_state="reported")

        return EvaluatorResponse(text, None, None, USD_PER_EXECUTION, None, "ok",
                                 cost_basis="local_zero_cost",
                                 raw_status_note=f"{elapsed:.3f}s")


def _run_subprocess(cmd: list[str], env: dict, timeout_s: float):
    """The only place this module starts a process. Injected as `runner=` in every test."""
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, env=env)
    return p.returncode, p.stdout, p.stderr
