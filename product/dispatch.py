"""The one paid-dispatch path. Every generation in the product goes through `Dispatcher`.

Order for every paid call (unchanged from the job kits, now shared and store-backed):
  1. route allowed + priced (runtime PriceBook; an unpriced route is refused)
  2. prompt guard (no-lettering clause; no exact copy string; no forbidden word) — refused locally, USD 0
  3. reserve against the job budget, atomically minting the attempt id (store.reserve)
  4. send; for long-running operations record the operation id BEFORE polling
  5. classify any failure (runtime.execute.provider_errors) — provider errors are never model-quality failures
  6. settle (failed calls included) and register the artifact against the attempt

Uncertain outcomes: an attempt found `reserved` after a worker restart is resumed if it has an
operation id (poll, don't resubmit); otherwise it is settled `uncertain` with its reservation kept
as spent, and the draw counts — nothing is silently re-sent.
"""
from __future__ import annotations

import re
import time
from decimal import Decimal
from pathlib import Path

from product.config import Settings, scrub
from product.providers import ROUTES, ProviderResult, providers_for
from product.store import Store, dec, utc_now
from runtime.execute import provider_errors

NO_LETTERING = ("no text", "no lettering", "textless")
NOT_CHARGED_HTTP = {400, 401, 403, 404, 409, 422, 429}   # rejected before generation: provider does not bill


class GuardRefused(Exception):
    pass


class IdenticalRequestRefused(GuardRefused):
    """Spec §6.2: never send the same request to the same generator a third time; a retry must change something."""


# Outcomes that count as the generator having answered THIS request (a take was made, or the provider refused the
# content). A transient infrastructure failure (5xx, timeout, 429) is not an answer: resending it is not a retry of
# the same creative request, so it does not count towards the limit.
MAX_IDENTICAL_SENDS = 2


def fingerprint(route: str, **inputs) -> str:
    from product.store import sha256_bytes, sha256_json
    norm = {}
    for k, v in inputs.items():
        if k in ("refs",):
            norm[k] = [sha256_bytes(b) for _, b in (v or [])]
        elif k == "image" and v is not None:
            norm[k] = sha256_bytes(v[1])
        else:
            norm[k] = v
    return sha256_json({"route": route, **norm})


class DispatchFailed(Exception):
    def __init__(self, msg, failure_class, retryable):
        super().__init__(msg)
        self.failure_class, self.retryable = failure_class, retryable


_PRICEBOOK = None


def pricebook():
    global _PRICEBOOK
    if _PRICEBOOK is None:
        from runtime.route.cli import build_router
        _PRICEBOOK = build_router()[0].prices
    return _PRICEBOOK


def quote(route: str, **params) -> Decimal:
    q = pricebook().quote(route, {"params": params})
    if not q.priced:
        raise GuardRefused(f"route {route} is unpriced ({q.reason}); nothing sent")
    return Decimal(str(q.expected_cost_usd))


# Voice prices per character (kitchen v3). The route roster has no voice rows yet (adding one is a Controller decision),
# so the product pins these from the saved price pages — eval/empirical-planning/price-pins-2026-09/:
#   sarvam      sarvam-bulbul-v3/sarvam-api-pricing.html: "Text to Speech is priced at ₹3.00 per 1,000 characters"
#               (USD at ₹83 = 0.0000361; rounded up to 0.00004)
#   azure       azure-neural-tts-hi-in/...centralindia.json: "Neural HD Text to Speech Characters" USD 22 per 1M (the higher
#               HD rate is used so standard neural voices are never under-reserved)
#   elevenlabs  elevenlabs-direct: 1 credit per character; USD 0.0003 per character is a deliberate over-estimate
#   google      Gemini speech is billed in audio tokens; USD 0.0002 per character is a deliberate over-estimate
SPEECH_USD_PER_CHAR = {"sarvam": Decimal("0.00004"), "azure": Decimal("0.000022"), "elevenlabs": Decimal("0.0003"),
                       "google": Decimal("0.0002")}


def speech_price(provider: str, text: str) -> Decimal:
    per = SPEECH_USD_PER_CHAR.get(provider)
    if per is None:
        raise GuardRefused(f"voice provider {provider} is unpriced; nothing sent")
    return max(Decimal("0.001"), (per * len(text or "")).quantize(Decimal("0.000001")))


def prompt_guard(prompt: str, *, exact_strings: list, forbidden_words: list, needs_no_lettering: bool = True, copy_lines=()):
    low = prompt.lower()
    for w in forbidden_words:
        if w and re.search(r"\b" + re.escape(w.lower()) + r"\b", low):
            raise GuardRefused(f"forbidden word {w!r} in a generation prompt (brand/IP/claim words are code-set or banned)")
    for s in exact_strings:
        if s and len(s) > 3 and s.lower() in low:
            raise GuardRefused(f"exact copy string {s!r} appears in a generation prompt (exact text is code-set)")
    if needs_no_lettering and not any(k in low for k in NO_LETTERING):
        raise GuardRefused("the prompt must carry the no-lettering clause")


class Dispatcher:
    def __init__(self, settings: Settings, store: Store, providers=None):
        self.s, self.store = settings, store
        self.p = providers or providers_for(settings)

    def _out(self, job_id: str, node_id: str, attempt_id: str, ext: str) -> Path:
        d = self.s.media_dir / job_id / "gen"
        d.mkdir(parents=True, exist_ok=True)
        return d / f"{node_id}__{attempt_id.split(':')[-1]}.{ext}"

    def _fail(self, att: str, res: ProviderResult, reserved: Decimal):
        cls = provider_errors.classify(http_status=res.http_status, message=res.message, timed_out=res.timed_out)
        fc = cls.get("failure_class") or cls.get("class") or "unclassified"
        charged = Decimal(0) if res.http_status in NOT_CHARGED_HTTP else reserved
        if "refusal" in res.message or "safety" in res.message:
            fc = "provider_refusal"
        self.store.settle(att, status="failed", settled_usd=charged, failure_class=fc,
                          counts_against_route=bool(cls.get("counts_against_route_quality", False)),
                          detail=f"{res.http_status} {scrub(res.message)[:400]}")
        return DispatchFailed(f"{fc}: {scrub(res.message)[:200]}", fc, bool(cls.get("retry_eligible")) or res.timed_out
                              or (res.http_status or 0) >= 500 or res.http_status == 429)

    def _check_identical(self, job_id, node_id, route, fp):
        row = self.store.q1("SELECT sent FROM request_fingerprints WHERE job_id=? AND fingerprint=?", (job_id, fp))
        if row and row["sent"] >= MAX_IDENTICAL_SENDS:
            self.store.event(job_id, "system", "identical_request_refused", {"node": node_id, "route": route, "fingerprint": fp[:16],
                                                                            "sent_before": row["sent"]})
            raise IdenticalRequestRefused(f"{node_id}: this exact request was already answered {row['sent']} times by {route}; "
                                          f"a retry must change the route, the source image or the instruction")

    def _count(self, job_id, node_id, route, fp):
        now = utc_now()
        with self.store.tx() as c:
            c.execute("INSERT INTO request_fingerprints (job_id, fingerprint, route, node_id, sent, first_utc, last_utc) VALUES (?,?,?,?,1,?,?) "
                      "ON CONFLICT(job_id, fingerprint) DO UPDATE SET sent=sent+1, last_utc=excluded.last_utc", (job_id, fp, route, node_id, now, now))

    def _register(self, job_id, node_id, att, res: ProviderResult, kind: str, ext: str, meta: dict) -> str:
        out = self._out(job_id, node_id, att, ext)
        out.write_bytes(res.data)
        return self.store.add_asset(job_id, path=out, kind=kind, source="generated", content_type=res.content_type or "",
                                    node_id=node_id, attempt_id=att, meta={**meta, "request_ref": res.request_ref})

    def image(self, job_id, node_id, *, prompt, aspect, refs, guard: dict, is_repair=False, meta=None) -> str:
        prompt_guard(prompt, **guard)
        fp = fingerprint("nano-banana-2", prompt=prompt, aspect=aspect, refs=refs)
        self._check_identical(job_id, node_id, "nano-banana-2", fp)
        cost = quote("nano-banana-2")
        att = self.store.reserve(job_id, route="nano-banana-2", category="provider", amount_usd=cost, node_id=node_id,
                                 is_repair=is_repair)
        with self.store.timed(job_id, "provider", f"{node_id} still"):
            res = self.p.image(prompt, aspect, refs)
        if res.status != "ok":
            err = self._fail(att, res, cost)
            if err.failure_class == "provider_refusal":
                self._count(job_id, node_id, "nano-banana-2", fp)
            raise err
        self._count(job_id, node_id, "nano-banana-2", fp)
        aid = self._register(job_id, node_id, att, res, "image", "png",
                             {"prompt": prompt, "aspect": aspect, "route": "nano-banana-2", **(meta or {})})
        self.store.settle(att, status="ok", settled_usd=cost, detail=f"{len(res.data)} bytes")
        return aid

    def video(self, job_id, node_id, *, prompt, image, duration_s, aspect, negative, guard: dict, is_repair=False,
              meta=None) -> str:
        prompt_guard(prompt, **guard)
        fp = fingerprint("veo-3.1-fast-i2v", prompt=prompt, image=image, duration_s=duration_s, aspect=aspect, negative=negative)
        self._check_identical(job_id, node_id, "veo-3.1-fast-i2v", fp)
        cost = quote("veo-3.1-fast-i2v", duration_s=duration_s)
        att = self.store.reserve(job_id, route="veo-3.1-fast-i2v", category="provider", amount_usd=cost, node_id=node_id,
                                 is_repair=is_repair)
        silent = False
        with self.store.timed(job_id, "provider", f"{node_id} clip"):
            res = self.p.video_submit(prompt, image, duration_s, aspect, negative)
            if res.status == "pending":
                self.store.mark_request(att, res.request_ref)
                res = self.p.video_poll(res.request_ref)
            if res.status != "ok" and "audio" in (res.message or "").lower() and "safety" in (res.message or "").lower():
                # live 2026-09-25: the model's own AUDIO tripped its safety filter (the picture was fine, and a refusal is not
                # billed). The film has its own music bed, so the same clip is asked for once more without generated sound.
                silent = True
                self.store.event(job_id, "system", "clip_audio_refused", {"node": node_id, "detail": (res.message or "")[:200]})
                res = self.p.video_submit(prompt, image, duration_s, aspect, negative, generate_audio=False)
                if res.status == "pending":
                    self.store.mark_request(att, res.request_ref)
                    res = self.p.video_poll(res.request_ref)
        if res.status != "ok":
            err = self._fail(att, res, cost)
            if err.failure_class == "provider_refusal":
                self._count(job_id, node_id, "veo-3.1-fast-i2v", fp)
            raise err
        self._count(job_id, node_id, "veo-3.1-fast-i2v", fp)
        aid = self._register(job_id, node_id, att, res, "video", "mp4",
                             {"prompt": prompt, "negative": negative, "duration_s": duration_s, "aspect": aspect,
                              "route": "veo-3.1-fast-i2v", "generated_audio": not silent, **(meta or {})})
        self.store.settle(att, status="ok", settled_usd=cost, detail=f"{len(res.data)} bytes")
        return aid

    def music(self, job_id, node_id, *, prompt, negative, guard: dict, is_repair=False) -> str:
        prompt_guard(prompt, needs_no_lettering=False, **guard)
        fp = fingerprint("lyria", prompt=prompt, negative=negative)
        self._check_identical(job_id, node_id, "lyria", fp)
        cost = quote("lyria")
        att = self.store.reserve(job_id, route="lyria", category="provider", amount_usd=cost, node_id=node_id,
                                 is_repair=is_repair)
        with self.store.timed(job_id, "provider", f"{node_id} music"):
            res = self.p.music(prompt, negative)
        if res.status != "ok":
            raise self._fail(att, res, cost)
        self._count(job_id, node_id, "lyria", fp)
        aid = self._register(job_id, node_id, att, res, "audio", "mp3" if (res.content_type or "").endswith(("mpeg", "mp3")) else "wav",
                             {"prompt": prompt, "route": "lyria"})
        self.store.settle(att, status="ok", settled_usd=cost)
        return aid

    # ── voice (kitchen v3: voice-over when the customer asks) ───────────────────────
    def speech(self, job_id, node_id, *, provider: str, text: str, voice: str, language_code: str, settings: dict, ssml: str = "",
               is_repair=False) -> str:
        route = f"tts-{provider}"
        fp = fingerprint(route, text=text, voice=voice, lang=language_code, settings=settings, ssml=ssml)
        self._check_identical(job_id, node_id, route, fp)
        cost = speech_price(provider, ssml if (provider == "azure" and ssml) else text)
        att = self.store.reserve(job_id, route=route, category="provider", amount_usd=cost, node_id=node_id, is_repair=is_repair)
        with self.store.timed(job_id, "provider", f"{node_id} voice"):
            res = self.p.speech(provider, text, voice=voice, language_code=language_code, settings=settings, ssml=ssml)
        if res.status != "ok":
            raise self._fail(att, res, cost)
        self._count(job_id, node_id, route, fp)
        ext = "mp3" if (res.content_type or "").endswith(("mpeg", "mp3")) else "wav"
        aid = self._register(job_id, node_id, att, res, "audio", ext,
                             {"route": route, "provider": provider, "voice": voice, "language_code": language_code,
                              "settings": settings, "text": text, "ssml": ssml})
        self.store.settle(att, status="ok", settled_usd=cost)
        return aid

    # ── restart recovery ─────────────────────────────────────────────────────────
    def recover(self, job_id: str) -> list:
        """Resolve attempts left `reserved` by a dead worker. Returns a list of (attempt, outcome)."""
        outcomes = []
        for a in self.store.attempts(job_id):
            if a["status"] != "reserved" or a["category"] != "provider":
                continue
            if a["route"] == "veo-3.1-fast-i2v" and a["request_ref"]:
                res = self.p.video_poll(a["request_ref"])
                if res.status == "ok":
                    self.store.settle(a["id"], status="ok", settled_usd=a["reserved_usd"], detail="recovered by resumed poll")
                    aid = self._register(job_id, a["node_id"], a["id"], res, "video", "mp4",
                                         {"route": a["route"], "recovered": True})
                    outcomes.append((a["id"], "recovered", aid))
                else:
                    self._fail(a["id"], res, dec(a["reserved_usd"]))
                    outcomes.append((a["id"], "failed", None))
            else:
                self.store.settle(a["id"], status="uncertain", settled_usd=a["reserved_usd"],
                                  failure_class="interrupted_uncertain",
                                  detail="worker stopped between reserve and settle; outcome unknown; reservation kept as spent; not re-sent")
                outcomes.append((a["id"], "uncertain", None))
        for a in self.store.attempts(job_id):     # reasoning calls cut off mid-flight: keep the money, record it
            if a["status"] == "reserved" and a["category"] == "reasoning":
                self.store.settle(a["id"], status="uncertain", settled_usd=a["reserved_usd"], failure_class="interrupted_uncertain",
                                  detail="worker stopped during a reasoning call")
                outcomes.append((a["id"], "uncertain", None))
        return outcomes
