#!/usr/bin/env python3
"""Bake-off v1 runner: arms A, B, C (+ A_MAI side check) exactly as TEST-FLOWS.md.

    bash -c 'source ~/.mi-keys && <venv>/bin/python run.py --step practice|stills|films [--sim] [--briefs T1,T2] [--run-dir D]'

Prompts come from render_prompts.build() (the approved text). Claude calls go through the `claude` CLI on the founder's
subscription (founder override, 26 Sep). Media: Nano Banana 2 / MAI-Image-2.6 / Veo 3.1 (Fast|standard) / Lyria, Google
Gemini API + Azure only. Finishing reuses the studio compositor (product/compose.py, pinned worktree).

Ledger: every call is reserved before it is sent and settled after (failures included) in <run>/ledger.jsonl. A step
stops when its cap would be exceeded (exit 3). Media is written under <run>/ (outside git); the run's text records are
copied into git at the end.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import render_prompts  # noqa: E402

MEDIA_ROOT = Path.home() / "Vaibhav_Personal_Projects" / "bakeoff-media"
STUDIO = MEDIA_ROOT / "studio"                 # git worktree of origin/claude/kitchen-v3 @ 11bfc5f (finishing code)
CLAUDE_CWD = MEDIA_ROOT / "claude-cwd"
MOKOBARA_REF = "origin/work/agency-job-mokobara-odyssey-001"

STEP_BRIEFS = {"practice": ["T1", "T2", "T3", "T4"],
               "stills": ["E01", "E02", "E03", "E04", "E05", "E06", "E07"],
               "films": ["E08", "E09", "E10", "E11", "E12"]}
STEP_ARMS = {"practice": ["B", "C"], "stills": ["A", "B", "C"], "films": ["A", "B", "C"]}
MAI_BRIEFS = {"E01", "E02", "E03", "E04", "E05"}
CAPS = {"practice": 14.0, "stills": 23.0, "films": 128.0}        # founder 26 Sep: total US$165
TOTAL_CAP = 165.0

WRITER_MODEL = "claude-sonnet-5"
PRICE = {"nb2": 0.067, "mai": 0.05, "veo-fast": 0.15, "veo-std": 0.40, "lyria": 0.06, "ocr": 0.0015,
         "luna_in": 0.25e-6, "luna_out": 2.0e-6, "claude": 0.0}
VEO = {"fast": "veo-3.1-fast-generate-preview", "std": "veo-3.1-generate-preview"}
VEO_DUR = (4, 6, 8)
GEMINI = "https://generativelanguage.googleapis.com/v1beta"
MAI_HOST = "https://aight-bakeoff-mai-eus.services.ai.azure.com"
LLM_LOCK = threading.Lock()          # one `claude` process at a time (8 GB Mac)
MAI_LOCK = threading.Lock()          # MAI deployment: 1 request / 60 s
_MAI_LAST = [0.0]


class CapReached(Exception):
    pass


def video_model(bid: str, cls: str) -> str:
    """Founder 26 Sep: story films on Veo 3.1 standard, except practice T3 on Fast."""
    return "std" if cls == "F1_story_film" and bid != "T3" else "fast"


# ─────────────────────────────── ledger ───────────────────────────────
class Ledger:
    def __init__(self, path: Path, step: str):
        self.path, self.step, self.lock = path, step, threading.Lock()
        self.rows = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def _spent(self, step=None):
        tot = {}
        for r in self.rows:
            if r["kind"] == "reserve":
                tot[r["id"]] = r
            elif r["kind"] == "settle" and r["id"] in tot:
                tot[r["id"]] = {**tot[r["id"]], "amount": r["amount"]}
        return sum(r["amount"] for r in tot.values() if step is None or r["step"] == step)

    def reserve(self, *, brief, arm, what, route, amount, sim):
        with self.lock:
            amount = 0.0 if sim else amount
            if self._spent(self.step) + amount > CAPS[self.step] + 1e-9:
                raise CapReached(f"step {self.step} cap US${CAPS[self.step]} would be exceeded by {route} {what} "
                                 f"(spent {self._spent(self.step):.2f} + {amount:.2f})")
            if self._spent() + amount > TOTAL_CAP + 1e-9:
                raise CapReached(f"total cap US${TOTAL_CAP} would be exceeded (spent {self._spent():.2f} + {amount:.2f})")
            rid = uuid.uuid4().hex[:12]
            self._write({"kind": "reserve", "id": rid, "t": time.time(), "step": self.step, "brief": brief, "arm": arm,
                         "what": what, "route": route, "amount": round(amount, 6), "sim": sim})
            return rid

    def settle(self, rid, *, status, amount, detail="", seconds=0.0):
        with self.lock:
            self._write({"kind": "settle", "id": rid, "t": time.time(), "status": status, "amount": round(amount, 6),
                         "detail": str(detail)[:500], "seconds": round(seconds, 2)})

    def _write(self, row):
        self.rows.append(row)
        with self.path.open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    def arm_cost(self, brief, arm):
        res = {r["id"]: r for r in self.rows if r["kind"] == "reserve" and r["brief"] == brief and r["arm"] == arm}
        cost, secs = 0.0, 0.0
        for r in self.rows:
            if r["kind"] == "settle" and r["id"] in res:
                cost += r["amount"]
                secs += r.get("seconds", 0)
        return round(cost, 4), round(secs, 1)


# ─────────────────────────────── providers ───────────────────────────────
def _http(method, url, headers, body=None, timeout=300, raw=False):
    data = body if isinstance(body, bytes) or body is None else json.dumps(body).encode()
    h = dict(headers)
    if body is not None and not isinstance(body, bytes):
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            b = r.read()
            return r.status, (b if raw else json.loads(b.decode()))
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", "replace")[:800]
        return e.code, {"$error": txt}
    except Exception as e:  # noqa: BLE001
        return None, {"$error": f"{type(e).__name__}: {e}"[:400]}


def extract_json(text: str):
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    cand = m.group(1) if m else text[text.find("{"): text.rfind("}") + 1]
    return json.loads(cand)


class Live:
    sim = False

    def __init__(self):
        self.gkey = os.environ.get("GOOGLE_API_KEY")
        self.vkey = os.environ.get("GOOGLE_CLOUD_VISION_API_KEY")
        self._azure = None
        self._mai = None

    # Claude via the subscription CLI
    def claude(self, prompt: str, files: list[Path] | None = None, workdir: Path | None = None) -> tuple[str, dict]:
        wd = workdir or CLAUDE_CWD
        wd.mkdir(parents=True, exist_ok=True)
        tools = ["--tools", "Read", "--allowedTools", "Read"] if files else ["--tools", ""]
        cmd = ["claude", "-p", "--model", WRITER_MODEL, "--system-prompt", "You are a helpful assistant.",
               *tools, "--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence",
               "--output-format", "json"]
        env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY",)}
        with LLM_LOCK:
            p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=wd, env=env, timeout=900)
        try:
            d = json.loads(p.stdout)
        except ValueError:
            raise RuntimeError(f"claude CLI: unparseable output rc={p.returncode} {p.stdout[:200]} {p.stderr[:200]}")
        if d.get("is_error"):
            raise RuntimeError(f"claude CLI error: {str(d.get('result'))[:300]}")
        return d.get("result") or "", {"usage": d.get("usage"), "models": list((d.get("modelUsage") or {}).keys())}

    def luna(self, prompt: str) -> tuple[str, float]:
        if self._azure is None:
            env = {}
            for line in (Path.home() / ".mi-studio-keys").read_text().splitlines():
                m = re.match(r"(?:export )?([A-Z_]+)=(.*)", line.strip())
                if m:
                    env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
            self._azure = env
        ep = self._azure["AZURE_OPENAI_ENDPOINT"].rstrip("/")
        st, d = _http("POST", f"{ep}/openai/deployments/gpt-5.6-luna/chat/completions?api-version=2025-04-01-preview",
                      {"api-key": self._azure["AZURE_OPENAI_API_KEY"]},
                      {"messages": [{"role": "user", "content": prompt}], "max_completion_tokens": 4000,
                       "response_format": {"type": "json_object"}}, timeout=180)
        if st != 200:
            raise RuntimeError(f"luna HTTP {st}: {str(d)[:300]}")
        u = d.get("usage") or {}
        return d["choices"][0]["message"]["content"], u.get("prompt_tokens", 0) * PRICE["luna_in"] + u.get("completion_tokens", 0) * PRICE["luna_out"]

    def nb2(self, prompt, aspect, refs):
        parts = [{"text": prompt}] + [{"inlineData": {"mimeType": m, "data": base64.b64encode(b).decode()}} for m, b in refs]
        body = {"contents": [{"role": "user", "parts": parts}],
                "generationConfig": {"responseModalities": ["IMAGE"], "candidateCount": 1, "imageConfig": {"aspectRatio": aspect}}}
        st, d = _http("POST", f"{GEMINI}/models/gemini-3.1-flash-image:generateContent", {"x-goog-api-key": self.gkey}, body)
        if st != 200:
            raise RuntimeError(f"nb2 HTTP {st}: {str(d)[:300]}")
        for c in d.get("candidates") or []:
            for p in (c.get("content") or {}).get("parts") or []:
                if (p.get("inlineData") or {}).get("data"):
                    return base64.b64decode(p["inlineData"]["data"])
        raise RuntimeError(f"nb2 no image: finish={[c.get('finishReason') for c in d.get('candidates') or []]} fb={d.get('promptFeedback')}")

    def _mai_key(self):
        if self._mai is None:
            self._mai = subprocess.run(["az", "cognitiveservices", "account", "keys", "list", "--subscription",
                                        "b832f4a1-79be-4fb2-ae93-6ba6efd209d2", "-g", "aight-studio", "-n",
                                        "aight-bakeoff-mai-eus", "--query", "key1", "-o", "tsv"],
                                       capture_output=True, text=True, check=True).stdout.strip()
        return self._mai

    def mai(self, prompt, aspect, refs):
        size = {"1:1": (1024, 1024), "4:5": (896, 1120), "9:16": (768, 1344), "16:9": (1344, 768)}.get(aspect, (1024, 1024))
        with MAI_LOCK:
            wait = 61 - (time.time() - _MAI_LAST[0])
            if wait > 0:
                time.sleep(wait)
            try:
                if not refs:
                    st, d = _http("POST", f"{MAI_HOST}/mai/v1/images/generations", {"api-key": self._mai_key()},
                                  {"model": "MAI-Image-2.6", "prompt": prompt, "width": size[0], "height": size[1]}, timeout=300)
                else:
                    b = uuid.uuid4().hex
                    parts = [f'--{b}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'.encode()
                             for n, v in (("model", "MAI-Image-2.6"), ("prompt", prompt))]
                    for i, (m, data) in enumerate(refs):
                        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="image"; filename="ref{i}.{m.split("/")[-1]}"\r\n'
                                     f'Content-Type: {m}\r\n\r\n'.encode() + data + b"\r\n")
                    st, d = _http("POST", f"{MAI_HOST}/mai/v1/images/edits",
                                  {"api-key": self._mai_key(), "Content-Type": f"multipart/form-data; boundary={b}"},
                                  b"".join(parts) + f"--{b}--\r\n".encode(), timeout=300)
            finally:
                _MAI_LAST[0] = time.time()
        if st != 200:
            raise RuntimeError(f"mai HTTP {st}: {str(d)[:300]}")
        return base64.b64decode(d["data"][0]["b64_json"])

    def veo(self, model, prompt, duration, aspect, image=None, refs=None):
        inst = {"prompt": prompt}
        params = {"aspectRatio": aspect, "durationSeconds": int(duration), "resolution": "720p",
                  "personGeneration": "allow_adult" if image else "allow_all"}
        if image:
            inst["image"] = {"bytesBase64Encoded": base64.b64encode(image[1]).decode(), "mimeType": image[0]}
        if refs:
            inst["referenceImages"] = [{"image": {"bytesBase64Encoded": base64.b64encode(b).decode(), "mimeType": m},
                                        "referenceType": "asset"} for m, b in refs[:3]]
        st, d = _http("POST", f"{GEMINI}/models/{VEO[model]}:predictLongRunning", {"x-goog-api-key": self.gkey},
                      {"instances": [inst], "parameters": params})
        if st == 400 and "personGeneration" in str(d) and params["personGeneration"] == "allow_all":   # refused before generation, US$0
            params["personGeneration"] = "allow_adult"
            st, d = _http("POST", f"{GEMINI}/models/{VEO[model]}:predictLongRunning", {"x-goog-api-key": self.gkey},
                          {"instances": [inst], "parameters": params})
        if st == 400 and refs:          # refused before generation (US$0): send without reference images, logged by caller
            return None, f"refs refused: {str(d)[:300]}"
        if st != 200 or not d.get("name"):
            raise RuntimeError(f"veo submit HTTP {st}: {str(d)[:300]}")
        return d["name"], ""

    def veo_poll(self, op, max_wait=900):
        deadline = time.time() + max_wait
        while time.time() < deadline:
            st, d = _http("GET", f"{GEMINI}/{op}", {"x-goog-api-key": self.gkey}, timeout=120)
            if st == 200 and d.get("done"):
                if d.get("error"):
                    raise RuntimeError(f"veo op error: {d['error']}")
                gv = (d.get("response") or {}).get("generateVideoResponse") or {}
                s = gv.get("generatedSamples") or []
                uri = ((s[0] if s else {}).get("video") or {}).get("uri")
                if not uri:
                    raise RuntimeError(f"veo no video: filtered={gv.get('raiMediaFilteredCount')} {gv.get('raiMediaFilteredReasons')}")
                st2, data = _http("GET", uri, {"x-goog-api-key": self.gkey}, timeout=300, raw=True)
                if st2 != 200:
                    raise RuntimeError(f"veo download HTTP {st2}")
                return data
            time.sleep(8)
        raise RuntimeError("veo poll timeout")

    def lyria(self, prompt):
        text = prompt + " Instrumental only: no vocals, no singing, no spoken words."
        st, d = _http("POST", f"{GEMINI}/interactions", {"x-goog-api-key": self.gkey}, {"model": "lyria-3-clip-preview", "input": text})
        if st != 200:
            raise RuntimeError(f"lyria HTTP {st}: {str(d)[:300]}")
        for s in d.get("steps") or []:
            for c in s.get("content") or []:
                if c.get("type") == "audio" and c.get("data"):
                    return base64.b64decode(c["data"])
        raise RuntimeError("lyria: no audio")

    def ocr(self, img: bytes) -> str:
        st, d = _http("POST", f"https://vision.googleapis.com/v1/images:annotate?key={self.vkey}", {},
                      {"requests": [{"image": {"content": base64.b64encode(img).decode()}, "features": [{"type": "TEXT_DETECTION"}]}]})
        if st != 200:
            raise RuntimeError(f"ocr HTTP {st}")
        return ((d.get("responses") or [{}])[0].get("fullTextAnnotation") or {}).get("text", "")


class Sim(Live):
    """Simulated providers: same interface, US$0, deterministic stub content."""
    sim = True

    def __init__(self):
        super().__init__()
        self.n = 0

    def claude(self, prompt, files=None, workdir=None):
        self.n += 1
        if "Pick the take" in prompt:
            labels = re.findall(r"\b([A-Z]\d*-s\d+-t\d+|[A-Z]\d*-d\d+)\b", prompt)
            return json.dumps({"picks": {"choice": labels[0] if labels else "d1"}, "reasons": {"choice": "sim"}}), {}
        if "Return JSON: {\"prompts\"" in prompt:
            film = "one prompt per scene" in prompt and "15 s" in prompt
            n = 2 if film else 1
            return json.dumps({"prompts": [{"scene": i + 1, "prompt": f"sim scene {i+1} prompt, a warm cinematic shot",
                                            "duration_s": 8} for i in range(n)], "riskiest_scene": n, "notes": "sim"}), {}
        if "These items need fixing" in prompt:
            d = json.loads(prompt[prompt.index("DRAFT:") + 6:])
            for s in d["scenes"]:
                s["prompt"] = " ".join(["calm", "morning", "light"] * 12)
                s["first_frame_still_prompt"] = s["prompt"]
            return json.dumps(d), {}
        base = {"ideas": [{"truth": "t", "moment": "m", "key_frame": "k"}] * 3, "chosen": 0, "why": "sim",
                "treatment": "sim treatment",
                "scenes": [{"n": i + 1, "prompt": "no text anywhere, " + " ".join(["soft", "light", "detail"] * 10), "duration_s": 8,
                            "references": ["photo1"], "spoken": "ek chhota sa pal" if i == 0 else "",
                            "on_screen_copy": ["Sim super"] if i == 0 else [],
                            "first_frame_still_prompt": " ".join(["warm", "frame", "still"] * 12)} for i in range(2)],
                "riskiest_scene": 2, "finish": {"copy_placement": "bottom", "end_card": "logo + copy", "music": "warm sitar bed"}}
        if "Answer each question YES or NO" in prompt:
            base["checklist"] = [{"id": "C01", "answer": "YES", "evidence": "sim", "action": "none"}]
        return json.dumps(base), {}

    def luna(self, prompt):
        req = prompt.split("REQUEST (verbatim):", 1)[1]
        quotes = re.findall(r"(?:exactly:|text:|headline:)\s*([^.\n]+?)(?:\s{2}|$|\.)", req)
        cls = next((c for c in ("S1_product_ad", "S2_edit", "M1_animate", "M2_product_film", "F1_story_film") if c in prompt), "S1_product_ad")
        return json.dumps({"class": cls, "format": {"aspect": "9:16", "duration_s": 15}, "exact_copy": [q.strip() for q in quotes][:3],
                           "language": "en", "facts": [], "questions": [], "refuse_or_rescope": None}), 0.0

    def nb2(self, prompt, aspect, refs):
        from PIL import Image, ImageDraw
        w, h = {"1:1": (1024, 1024), "4:5": (896, 1120), "9:16": (720, 1280), "16:9": (1280, 720)}.get(aspect, (1024, 1024))
        self.n += 1
        im = Image.new("RGB", (w, h), ((self.n * 47) % 255, 120, 160))
        ImageDraw.Draw(im).rectangle([w // 4, h // 3, 3 * w // 4, 2 * h // 3], fill=(230, 200, 150))
        import io
        buf = io.BytesIO()
        im.save(buf, "PNG")
        return buf.getvalue()

    mai = nb2

    def veo(self, model, prompt, duration, aspect, image=None, refs=None):
        return f"sim-op|{duration}|{aspect}|{uuid.uuid4().hex[:6]}", ""

    def veo_poll(self, op, max_wait=900):
        _, dur, aspect, _ = op.split("|")
        w, h = (720, 1280) if aspect == "9:16" else (1280, 720)
        out = MEDIA_ROOT / "tmp" / f"{uuid.uuid4().hex}.mp4"
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc2=s={w}x{h}:r=24:d={dur}", "-f", "lavfi",
                        "-i", f"sine=f=330:d={dur}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out)], check=True)
        b = out.read_bytes()
        out.unlink()
        return b

    def lyria(self, prompt):
        out = MEDIA_ROOT / "tmp" / f"{uuid.uuid4().hex}.mp3"
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=220:d=30", str(out)], check=True)
        b = out.read_bytes()
        out.unlink()
        return b

    def ocr(self, img):
        return ""


# ─────────────────────────────── helpers ───────────────────────────────
def ff(*args, level="error"):
    return subprocess.run(["ffmpeg", "-hide_banner", "-v", level, "-y", *map(str, args)], capture_output=True, text=True)


def probe(p: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height", "-of", "json", str(p)],
                       capture_output=True, text=True)
    return json.loads(r.stdout or "{}")


def mime(p: Path) -> str:
    return {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(p.suffix.lower(), "image/jpeg")


def img_ext(b: bytes) -> str:
    return ".png" if b[:4] == b"\x89PNG" else ".jpg"


def veo_dur(s) -> int:
    try:
        s = float(s)
    except (TypeError, ValueError):
        s = 8
    return next((d for d in VEO_DUR if s <= d), 8)


def aspect_from_text(t: str, default: str) -> str:
    m = re.search(r"\b(1:1|4:5|9:16|16:9)\b", t)
    return m.group(1) if m else default


def words(s: str) -> int:
    return len(re.findall(r"\S+", s or ""))


class Assets:
    def __init__(self, run: Path, briefs_doc: dict):
        self.dir = run / "assets"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.photo_dir = briefs_doc["photo_dir"]

    def get(self, brief: dict) -> list[Path]:
        out = []
        for name in brief.get("assets") or []:
            dst = self.dir / name
            if not dst.exists():
                if brief.get("asset_dir"):
                    shutil.copy(Path(os.path.expanduser(brief["asset_dir"])) / name, dst)
                else:
                    cands = [name, name.replace("The_Transit_Backpack_30L_Private_Island_3", "The-Transit-Backpack-30L_Private-Island-3")]
                    for c in cands:
                        r = subprocess.run(["git", "show", f"{MOKOBARA_REF}:{self.photo_dir}{c}"], cwd=REPO, capture_output=True)
                        if r.returncode == 0:
                            dst.write_bytes(r.stdout)
                            break
                    else:
                        raise FileNotFoundError(name)
            out.append(dst)
        return out


# ─────────────────────────────── one arm on one brief ───────────────────────────────
class ArmRun:
    def __init__(self, ctx, bid, arm, prompts, photos, understanding=None):
        self.ctx, self.bid, self.arm, self.P = ctx, bid, arm, prompts
        self.cls = prompts["cls"]
        self.brief = prompts["brief"]
        self.photos = photos
        self.logo = next((p for p in photos if "logo" in p.name.lower()), None)
        self.product_photos = [p for p in photos if p is not self.logo]
        self.dir = ctx.run / self.bid / self.arm
        self.dir.mkdir(parents=True, exist_ok=True)
        self.U = understanding
        self.trace = {"brief": bid, "arm": arm, "class": self.cls, "events": []}

    # ledgered calls
    def call(self, route, what, amount, fn, *a, **k):
        rid = self.ctx.ledger.reserve(brief=self.bid, arm=self.arm, what=what, route=route, amount=amount, sim=self.ctx.p.sim)
        t = time.time()
        try:
            out = fn(*a, **k)
        except CapReached:
            raise
        except Exception as e:  # noqa: BLE001
            # a failed media call may still be billed; settle at the reserved amount for Veo/images (conservative)
            self.ctx.ledger.settle(rid, status="failed", amount=0.0 if route.startswith(("claude", "luna", "ocr")) or self.ctx.p.sim else amount,
                                   detail=str(e), seconds=time.time() - t)
            self.ev("call_failed", route=route, what=what, error=str(e)[:400])
            raise
        amt = amount
        if route == "luna" and isinstance(out, tuple):
            out, amt = out
        self.ctx.ledger.settle(rid, status="ok", amount=0.0 if self.ctx.p.sim else amt, seconds=time.time() - t)
        return out

    def ev(self, kind, **kw):
        self.trace["events"].append({"t": round(time.time(), 1), "kind": kind, **kw})

    def save(self, name, data: bytes) -> Path:
        p = self.dir / name
        p.write_bytes(data)
        return p

    def write_llm(self, name, prompt, text):
        (self.dir / f"{name}.prompt.txt").write_text(prompt)
        (self.dir / f"{name}.reply.txt").write_text(text)

    def claude_json(self, name, prompt, files=None, workdir=None):
        for attempt in (1, 2):
            text, meta = self.call("claude", name, PRICE["claude"], self.ctx.p.claude, prompt, files, workdir)
            self.write_llm(f"{name}" + ("" if attempt == 1 else "-retry"), prompt, text)
            try:
                return extract_json(text)
            except (ValueError, json.JSONDecodeError) as e:
                self.ev("json_parse_failed", step=name, attempt=attempt, error=str(e)[:200])
                if attempt == 2:
                    raise

    # generation primitives
    def refs_bytes(self, paths):
        return [(mime(p), p.read_bytes()) for p in paths]

    def image(self, prompt, aspect, refs, tag, model="nb2"):
        fn = self.ctx.p.mai if model == "mai" else self.ctx.p.nb2
        b = self.call(model, tag, PRICE[model], fn, prompt, aspect, self.refs_bytes(refs))
        return self.save(f"{tag}{img_ext(b)}", b)

    def video(self, model, prompt, duration, aspect, tag, image: Path | None = None, refs=None):
        route = f"veo-{model}"
        cost = PRICE[route] * duration
        refb = self.refs_bytes(refs) if refs else None
        img = (mime(image), image.read_bytes()) if image else None
        op, note = self.call(route + "-submit", tag, 0.0, self.ctx.p.veo, model, prompt, duration, aspect, img, refb)
        if op is None:
            self.ev("veo_refs_refused_sent_without", tag=tag, note=note)
            op, _ = self.call(route + "-submit", tag + "-norefs", 0.0, self.ctx.p.veo, model, prompt, duration, aspect, img, None)
        b = self.call(route, tag, cost, self.ctx.p.veo_poll, op)
        return self.save(f"{tag}.mp4", b)

    # contact sheet + pick (A3 / B6)
    def pick(self, candidates: dict[str, Path], name="pick"):
        """candidates: label -> image or video. Returns the chosen label."""
        if len(candidates) == 1:
            return next(iter(candidates))
        from PIL import Image, ImageDraw, ImageFont
        tiles = []
        for label, p in candidates.items():
            frames = []
            if p.suffix == ".mp4":
                dur = float(probe(p).get("format", {}).get("duration", 8))
                for i, frac in enumerate((0.1, 0.5, 0.9)):
                    fp = self.dir / f"_f_{label}_{i}.jpg"
                    ff("-ss", f"{dur*frac:.2f}", "-i", p, "-frames:v", "1", "-vf", "scale=-2:360", fp)
                    frames.append(Image.open(fp).convert("RGB"))
            else:
                im = Image.open(p).convert("RGB")
                im.thumbnail((480, 480))
                frames.append(im)
            w = sum(f.width for f in frames) + 8 * (len(frames) - 1)
            h = max(f.height for f in frames) + 44
            t = Image.new("RGB", (w, h), "white")
            x = 0
            for f in frames:
                t.paste(f, (x, 44))
                x += f.width + 8
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
            except OSError:
                font = ImageFont.load_default()
            ImageDraw.Draw(t).text((6, 6), label, fill="black", font=font)
            tiles.append(t)
        W = max(t.width for t in tiles)
        H = sum(t.height for t in tiles) + 16 * (len(tiles) - 1)
        sheet = Image.new("RGB", (W, H), (235, 235, 235))
        y = 0
        for t in tiles:
            sheet.paste(t, (0, y))
            y += t.height + 16
        wd = self.dir / f"_{name}"
        wd.mkdir(exist_ok=True)
        sheet.save(wd / "contact_sheet.jpg", quality=88)
        prompt = (self.P["A3"] + f"\n\nThe contact sheet is the file contact_sheet.jpg in the current folder (open it with the Read tool). "
                  f"Labelled takes: {', '.join(candidates)}. Each video take is shown as 3 frames (start, middle, end). "
                  f"Return the chosen label(s) as the values in \"picks\".")
        d = self.claude_json(name, prompt, files=[wd / "contact_sheet.jpg"], workdir=wd)
        vals = [str(v) for v in (d.get("picks") or {}).values()] if isinstance(d.get("picks"), dict) else [str(x) for x in d.get("picks") or []]
        for v in vals:
            for label in candidates:
                if label == v.strip() or label in v:
                    self.ev("picked", name=name, label=label, raw=vals)
                    return label
        self.ev("pick_unmatched_took_first", name=name, raw=vals)
        return next(iter(candidates))

    # ── checks (B5) ──
    def allowed_text(self):
        if not hasattr(self, "_allowed"):
            txt = ""
            for p in self.product_photos:
                try:
                    txt += " " + self.call("ocr", f"ocr-ref-{p.name}", PRICE["ocr"], self.ctx.p.ocr, p.read_bytes())
                except Exception:  # noqa: BLE001
                    pass
            self._allowed = set(re.findall(r"[a-z0-9]{3,}", txt.lower()))
        return self._allowed

    def text_problems(self, img: bytes, spoken=""):
        seen = self.call("ocr", "ocr", PRICE["ocr"], self.ctx.p.ocr, img)
        toks = re.findall(r"[a-z0-9]{3,}", seen.lower())
        exact = [c for c in (self.U or {}).get("exact_copy") or [] if c and c.lower() in seen.lower()]
        allowed = self.allowed_text() | set(re.findall(r"[a-z0-9]{3,}", (spoken or "").lower()))
        stray = [t for t in toks if t not in allowed]
        probs = []
        if exact:
            probs.append(f"exact copy drawn by the model: {exact}")
        if sum(len(t) for t in stray) >= 6:
            probs.append(f"stray text: {' '.join(stray[:12])}")
        return probs, seen

    def check_still(self, p: Path):
        probs, seen = self.text_problems(p.read_bytes())
        self.ev("check_still", file=p.name, problems=probs, ocr=seen[:200])
        return probs

    def check_clip(self, p: Path, want_dur: int, aspect: str, spoken=""):
        probs = []
        pr = probe(p)
        dur = float(pr.get("format", {}).get("duration", 0))
        vs = [s for s in pr.get("streams", []) if s.get("codec_type") == "video"]
        if not vs:
            return ["no video stream"]
        w, h = vs[0]["width"], vs[0]["height"]
        if abs(dur - want_dur) > 0.6:
            probs.append(f"duration {dur:.1f}s != {want_dur}s")
        if (aspect == "9:16") != (h > w):
            probs.append(f"aspect {w}x{h} != {aspect}")
        bd = ff("-i", p, "-vf", "blackdetect=d=0.5:pix_th=0.08", "-an", "-f", "null", "-", level="info").stderr
        if "black_start" in bd:
            probs.append("black frames ≥0.5 s")
        fz = ff("-i", p, "-vf", "freezedetect=n=0.003:d=2", "-an", "-f", "null", "-", level="info").stderr
        frozen = sum(float(x) for x in re.findall(r"freeze_duration: ([0-9.]+)", fz))
        starts = [float(x) for x in re.findall(r"freeze_start: ([0-9.]+)", fz)]
        if len(starts) > len(re.findall(r"freeze_end: ", fz)):          # a freeze that runs to the end of the clip
            frozen += max(0.0, dur - starts[-1])
        if frozen > dur * 0.5:
            probs.append(f"little motion: frozen {frozen:.1f}s of {dur:.1f}s")
        ln = ff("-i", p, "-af", "ebur128", "-vn", "-f", "null", "-", level="info").stderr
        m = re.findall(r"I:\s+(-?[0-9.]+) LUFS", ln)
        loud = float(m[-1]) if m else None
        for frac in (0.2, 0.5, 0.85):
            fp = self.dir / f"_ocr_{p.stem}_{frac}.jpg"
            ff("-ss", f"{dur*frac:.2f}", "-i", p, "-frames:v", "1", fp)
            if fp.exists():
                tp, _ = self.text_problems(fp.read_bytes(), spoken)
                probs += [f"t={dur*frac:.1f}s {x}" for x in tp]
        self.ev("check_clip", file=p.name, problems=probs, loudness_lufs=loud)
        return probs

    # ── lint (B3): flags only, back to the writer once ──
    def lint(self, d: dict) -> list[str]:
        flags = []
        exact = [c for c in (self.U or {}).get("exact_copy") or [] if c]
        # brand names = web addresses / handles and their name part (mokobara.com → mokobara); capitalised ordinary words
        # in an offer line ("Family Thali") are NOT brand names (practice T1, 26 Sep: "thali" was flagged in a thali photo)
        brand_words = set()
        for c in exact:
            for w in re.findall(r"@?[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+|@[A-Za-z0-9_.]+", c):
                brand_words |= {w.lower().lstrip("@"), w.lower().lstrip("@").split(".")[0]}
        neg = re.compile(r"\b(no|without|don't|do not|never|avoid)\b\s+\w+", re.I)
        for s in d.get("scenes") or []:
            n = s.get("n", "?")
            pr = s.get("prompt") or ""
            texts = [("prompt", pr)] + ([("first_frame_still_prompt", s["first_frame_still_prompt"])] if s.get("first_frame_still_prompt") else [])
            for field, t in texts:
                wc = words(t)
                if self.cls == "S1_product_ad" or field == "first_frame_still_prompt":
                    if not 30 <= wc <= 80:
                        flags.append(f"scene {n} {field}: still prompt has {wc} words (needs 30–80)")
                elif self.cls == "M1_animate":
                    if wc > 40:
                        flags.append(f"scene {n} {field}: animate prompt has {wc} words (max 40; motion and camera only)")
                elif self.cls in ("M2_product_film", "F1_story_film") and wc > 120:
                    flags.append(f"scene {n} {field}: video prompt has {wc} words (max 120)")
                low = t.lower()
                hits = [c for c in exact if c.lower() in low] + [b for b in brand_words if re.search(rf"\b{re.escape(b)}\b", low)]
                if hits:
                    flags.append(f"scene {n} {field}: contains exact copy / brand name {sorted(set(hits))} — copy is added by code")
                m = neg.findall(t)
                if m:
                    flags.append(f"scene {n} {field}: negative phrasing ('{neg.search(t).group(0)}') — rephrase positively")
            sp = s.get("spoken") or ""
            if sp:
                limit = 2.5 * (float(s.get("duration_s") or 8) - 0.4)
                if words(sp) > limit:
                    flags.append(f"scene {n}: spoken line has {words(sp)} words; max {limit:.0f} for {s.get('duration_s')} s")
        return flags

    # ── arm A ──
    def run_A(self, model="nb2"):
        if model == "mai":
            a1 = json.loads((self.ctx.run / self.bid / "A" / "A1.json").read_text())
        else:
            a1 = self.claude_json("A1", self.P["A1"])
            (self.dir / "A1.json").write_text(json.dumps(a1, indent=1, ensure_ascii=False))
        prompts = a1.get("prompts") or []
        verb = self.brief.get("verbatim", "")
        if self.cls in ("S1_product_ad", "S2_edit"):
            aspect = aspect_from_text(verb, "1:1")
            refs = self.photos
            cands = {}
            for i in range(4):
                try:
                    cands[f"d{i+1}"] = self.image(prompts[0]["prompt"], aspect, refs, f"draw{i+1}", model=model)
                except CapReached:
                    raise
                except Exception:  # noqa: BLE001
                    continue
            if not cands:
                raise RuntimeError("no draw succeeded")
            return cands[self.pick(cands)], "image"
        if self.cls == "M1_animate":
            dur = veo_dur(prompts[0].get("duration_s", 8))
            cands = {}
            for i in range(2):
                try:
                    cands[f"t{i+1}"] = self.video("fast", prompts[0]["prompt"], dur, "9:16", f"take{i+1}", image=self.photos[0])
                except CapReached:
                    raise
                except Exception:  # noqa: BLE001
                    continue
            if not cands:
                raise RuntimeError("no take succeeded")
            return cands[self.pick(cands)], "video"
        # films: text-to-video per scene (photos as Veo reference images), + 1 retake of the riskiest scene
        vm = video_model(self.bid, self.cls)
        refs = self.product_photos or None
        risky = int(a1.get("riskiest_scene") or len(prompts))
        jobs = [(i, s, "t1") for i, s in enumerate(prompts)] + [(risky - 1, prompts[min(max(risky - 1, 0), len(prompts) - 1)], "t2")]
        clips = self._parallel_videos(vm, [(f"S{i+1}-{t}", s["prompt"], veo_dur(s.get("duration_s", 8)), "9:16", None,
                                            refs if vm == "std" else None) for i, s, t in jobs])
        chosen = []
        for i, s in enumerate(prompts):
            c = {f"A-s{i+1}-{t}": clips[f"S{i+1}-{t}"] for t in ("t1", "t2") if clips.get(f"S{i+1}-{t}")}
            if c:
                chosen.append(c[self.pick(c, name=f"pick-s{i+1}")])
        out = self.dir / "film.mp4"
        concat(chosen, out, self.dir)
        return out, "video"

    def _parallel_videos(self, vm, specs):
        """specs: (tag, prompt, dur, aspect, image, refs) → {tag: path or None}."""
        res = {}

        def one(sp):
            tag, prompt, dur, aspect, image, refs = sp
            try:
                res[tag] = self.video(vm, prompt, dur, aspect, tag, image=image, refs=refs)
            except CapReached:
                raise
            except Exception:  # noqa: BLE001
                res[tag] = None
        with ThreadPoolExecutor(max_workers=3) as ex:
            for f in [ex.submit(one, s) for s in specs]:
                f.result()
        return res

    # ── arms B and C ──
    def run_BC(self):
        canon = self.arm == "C"
        d = self.claude_json("C2" if canon else "B2", self.P["C2" if canon else "B2"])
        if canon:
            d2 = self.claude_json("C2b", self.P["C2b"] + "\n\nDRAFT:\n" + json.dumps(d, ensure_ascii=False)
                                  + "\n\nCUSTOMER REQUEST (verbatim):\n" + self.brief.get("verbatim", ""))
            if d2.get("scenes"):
                d = d2
        (self.dir / "writer.json").write_text(json.dumps(d, indent=1, ensure_ascii=False))
        flags = self.lint(d)
        self.ev("lint", flags=flags)
        if flags:
            fix = self.P["lint"].replace("{list}", "; ".join(flags)) + "\n\nDRAFT:" + json.dumps(d, ensure_ascii=False)
            try:
                d3 = self.claude_json("B3-fix", fix)
                if d3.get("scenes"):
                    d = d3
            except (ValueError, json.JSONDecodeError):
                self.ev("lint_fix_unparseable_kept_draft")
            self.ev("lint_after_fix", flags=self.lint(d))
            (self.dir / "writer-final.json").write_text(json.dumps(d, indent=1, ensure_ascii=False))
        scenes = d.get("scenes") or []
        fmt = (self.U or {}).get("format") or {}
        refs_for = lambda s: [p for p in self.product_photos
                              if not s.get("references") or any(str(r) in p.name or re.fullmatch(rf"photo{self.product_photos.index(p)+1}", str(r))
                                                                  for r in s.get("references"))] or self.product_photos
        if self.cls in ("S1_product_ad", "S2_edit"):
            aspect = fmt.get("aspect") if fmt.get("aspect") in ("1:1", "4:5", "9:16", "16:9") else "1:1"
            s = scenes[0]
            refs = self.photos if self.cls == "S2_edit" else refs_for(s)
            cands = {}
            for i in range(4):
                try:
                    p = self.image(s["prompt"], aspect, refs, f"draw{i+1}")
                except CapReached:
                    raise
                except Exception:  # noqa: BLE001
                    continue
                if not self.check_still(p):
                    cands[f"d{i+1}"] = p
                else:
                    self._failed = getattr(self, "_failed", {}) | {f"d{i+1}": p}
            if not cands:
                cands = getattr(self, "_failed", {})
                self.ev("all_draws_failed_checks_pick_from_all")
            if not cands:
                raise RuntimeError("no draw succeeded")
            plate = cands[self.pick(cands)]
            return self.finish_still(plate, aspect, d), "image"
        if self.cls == "M1_animate":
            s = scenes[0]
            dur = veo_dur(s.get("duration_s") or fmt.get("duration_s") or 8)
            aspect = fmt.get("aspect") if fmt.get("aspect") in ("9:16", "16:9") else "9:16"
            cands, failed = {}, {}
            for i in range(2):
                try:
                    p = self.video("fast", s["prompt"], dur, aspect, f"take{i+1}", image=self.photos[0])
                except CapReached:
                    raise
                except Exception:  # noqa: BLE001
                    continue
                (failed if self.check_clip(p, dur, aspect) else cands)[f"t{i+1}"] = p
            cands = cands or failed
            if not cands:
                raise RuntimeError("no take succeeded")
            return cands[self.pick(cands)], "video"
        # films: first-frame still → Veo i2v per scene; 1 take per scene + 1 retake (a failed scene first, else the riskiest)
        vm = video_model(self.bid, self.cls)
        aspect = fmt.get("aspect") if fmt.get("aspect") in ("9:16", "16:9") else "9:16"
        firsts = {}
        for i, s in enumerate(scenes):
            fp = s.get("first_frame_still_prompt") or s.get("prompt")
            try:
                firsts[i] = self.image(fp, aspect, refs_for(s) if self.product_photos else [], f"S{i+1}-first")
            except CapReached:
                raise
            except Exception:  # noqa: BLE001
                firsts[i] = None
        specs = [(f"S{i+1}-t1", s["prompt"], veo_dur(s.get("duration_s", 8)), aspect, firsts[i], None) for i, s in enumerate(scenes)]
        clips = self._parallel_videos(vm, specs)
        fails = {}
        for i, s in enumerate(scenes):
            p = clips.get(f"S{i+1}-t1")
            fails[i] = ["generation failed"] if p is None else self.check_clip(p, veo_dur(s.get("duration_s", 8)), aspect, s.get("spoken", ""))
        bad = [i for i in fails if fails[i]]
        retake = bad[0] if bad else min(max(int(d.get("riskiest_scene") or len(scenes)) - 1, 0), len(scenes) - 1)
        self.ev("retake_slot", scene=retake + 1, reason="failed checks" if bad else "riskiest")
        s = scenes[retake]
        clips.update(self._parallel_videos(vm, [(f"S{retake+1}-t2", s["prompt"], veo_dur(s.get("duration_s", 8)), aspect, firsts[retake], None)]))
        if clips.get(f"S{retake+1}-t2"):
            self.check_clip(clips[f"S{retake+1}-t2"], veo_dur(s.get("duration_s", 8)), aspect, s.get("spoken", ""))
        chosen = []
        for i, s in enumerate(scenes):
            c = {f"{self.arm}-s{i+1}-{t}": clips[f"S{i+1}-{t}"] for t in ("t1", "t2") if clips.get(f"S{i+1}-{t}")}
            if len(c) > 1 and fails[i]:
                c = {k: v for k, v in c.items() if not k.endswith("t1")}
            if c:
                chosen.append((i, c[self.pick(c, name=f"pick-s{i+1}")]))
        return self.finish_film(chosen, scenes, d, aspect), "video"

    # ── finishing (B7), code only ──
    def direction(self, d, zone_default="bottom"):
        exact = [c for c in (self.U or {}).get("exact_copy") or [] if c and not re.search(r"\blogo\b", c, re.I)]
        place = ((d.get("finish") or {}).get("copy_placement") or "").lower()
        zone = next((z for z in ("top", "bottom", "left", "right") if z in place), zone_default)
        return {"copy_deck": [{"id": f"c{i+1}", "text": t, "role": "headline" if i == 0 else "copy"} for i, t in enumerate(exact)],
                "composition": {"text_zone": zone}, "end_card": {"background_hex": "#101010"}}

    def studio(self):
        if str(STUDIO) not in sys.path:
            sys.path.insert(0, str(STUDIO))
        from product import compose, media  # noqa: F401
        return compose, media

    def finish_still(self, plate, aspect, d):
        dr = self.direction(d)
        if not dr["copy_deck"] and not self.logo:
            self.ev("finish_still", note="no exact copy and no logo: plate shown as generated")
            return plate
        compose, media = self.studio()
        out = self.dir / f"final-{aspect.replace(':', 'x')}.png"
        try:
            _, checks, layout = compose.still_ad(plate=plate, out=out, aspect=aspect, direction=dr, logo=self.logo,
                                                 workdir=self.dir, product_box_norm=None)
            self.ev("finish_still", checks=[(c["check_id"], c["status"]) for c in checks], text=layout.get("rendered_text"))
            return out
        except Exception as e:  # noqa: BLE001
            self.ev("finish_still_retry_wrapped", error=f"{type(e).__name__}: {e}"[:300])
        # a line too wide for the canvas: the same words, same order, wrapped at word breaks (≤26 characters a line)
        deck = []
        for c in dr["copy_deck"]:
            cur = ""
            for w in c["text"].split():
                if cur and len(cur) + 1 + len(w) > 26:
                    deck.append(cur)
                    cur = w
                else:
                    cur = f"{cur} {w}".strip()
            deck.append(cur)
        dr["copy_deck"] = [{"id": f"c{i+1}", "text": t, "role": "headline" if i == 0 else "copy"} for i, t in enumerate(deck)]
        try:
            _, checks, layout = compose.still_ad(plate=plate, out=out, aspect=aspect, direction=dr, logo=self.logo,
                                                 workdir=self.dir, product_box_norm=None)
            self.ev("finish_still", wrapped=True, checks=[(c["check_id"], c["status"]) for c in checks], text=layout.get("rendered_text"))
            return out
        except Exception as e:  # noqa: BLE001
            self.ev("finish_still_failed_plate_shown", error=f"{type(e).__name__}: {e}"[:400])
            return plate

    def finish_film(self, chosen, scenes, d, aspect):
        compose, media = self.studio()
        W, H = (1080, 1920) if aspect == "9:16" else (1920, 1080)
        parts = []
        for i, clip in chosen:
            s = scenes[i]
            copy = (s.get("on_screen_copy") or [])
            if copy and isinstance(copy[0], str) and copy[0].strip():
                try:
                    ov = self.dir / f"super-s{i+1}.png"
                    dur = float(probe(clip)["format"]["duration"])
                    _, ch = compose.super_overlay(out=ov, size=(W, H), text=copy[0].strip(), clip=clip, clip_in=0.0, use=dur, clip_size=(W, H))
                    out = self.dir / f"s{i+1}-super.mp4"
                    r = ff("-i", clip, "-i", ov, "-filter_complex", f"[0:v]scale={W}:{H}[v];[v][1:v]overlay=0:0:enable='gte(t,{max(0.0, dur-3.5):.2f})'",
                           "-c:a", "copy", "-c:v", "libx264", "-pix_fmt", "yuv420p", out)
                    if r.returncode == 0:
                        clip = out
                        self.ev("super", scene=i + 1, text=copy[0], checks=[(c["check_id"], c["status"]) for c in ch])
                except Exception as e:  # noqa: BLE001
                    self.ev("super_failed", scene=i + 1, error=str(e)[:300])
            parts.append(clip)
            sp = s.get("spoken") or ""
            if sp:
                limit = 2.5 * (veo_dur(s.get("duration_s", 8)) - 0.4)
                self.ev("voice_timing", scene=i + 1, words=words(sp), max_words=round(limit, 1), ok=words(sp) <= limit)
        dr = self.direction(d)
        if dr["copy_deck"] or self.logo:
            try:
                card = self.dir / "end_card.png"
                _, ch, _ = compose.end_card(out=card, size=(W, H), direction=dr, logo=self.logo, workdir=self.dir)
                cv = self.dir / "end_card.mp4"
                ff("-loop", "1", "-t", "2.5", "-i", card, "-f", "lavfi", "-t", "2.5", "-i", "anullsrc=r=48000:cl=stereo",
                   "-vf", f"scale={W}:{H},format=yuv420p", "-r", "24", "-c:v", "libx264", "-c:a", "aac", "-shortest", cv)
                parts.append(cv)
                self.ev("end_card", checks=[(c["check_id"], c["status"]) for c in ch])
            except Exception as e:  # noqa: BLE001
                self.ev("end_card_failed", error=f"{type(e).__name__}: {e}"[:300])
        film = self.dir / "film-cut.mp4"
        concat(parts, film, self.dir, size=(W, H))
        music = ((d.get("finish") or {}).get("music") or "").strip()
        if music and not re.match(r"^(no|none|n/?a|false)\b", music, re.I):
            try:
                mb = self.call("lyria", "music", PRICE["lyria"], self.ctx.p.lyria, music)
                mp = self.save("music.mp3", mb)
                out = self.dir / "film.mp4"
                r = ff("-i", film, "-i", mp, "-filter_complex",
                       "[1:a]volume=0.18,afade=t=out:st=0:d=0.1[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[a]",
                       "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", out)
                if r.returncode == 0:
                    self.ev("music_bed", mood=music)
                    return out
                self.ev("music_mix_failed", err=r.stderr[-300:])
            except CapReached:
                raise
            except Exception as e:  # noqa: BLE001
                self.ev("music_failed", error=str(e)[:300])
        return film


def concat(paths, out: Path, wd: Path, size=None):
    """Normalise every part to one size/fps/audio format, then join in order. No other editing."""
    if not paths:
        raise RuntimeError("nothing to concatenate")
    if size is None:
        pr = probe(paths[0])
        v = next(s for s in pr["streams"] if s["codec_type"] == "video")
        size = (v["width"], v["height"])
    W, H = size
    norm = []
    for i, p in enumerate(paths):
        n = wd / f"_norm_{i}.mp4"
        has_a = any(s.get("codec_type") == "audio" for s in probe(p).get("streams", []))
        args = ["-i", p] + ([] if has_a else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"])
        ff(*args, "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p",
           "-map", "0:v", "-map", "0:a" if has_a else "1:a", "-shortest", "-c:v", "libx264", "-c:a", "aac", "-ar", "48000", "-ac", "2", n)
        norm.append(n)
    lst = wd / "_concat.txt"
    lst.write_text("".join(f"file '{n}'\n" for n in norm))
    r = ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-300:])


# ─────────────────────────────── driver ───────────────────────────────
class Ctx:
    pass


def freeze_hashes() -> dict:
    files = [HERE / f for f in ("run.py", "render_prompts.py", "canon_context.py", "TEST-FLOWS.md", "BRIEFS.yaml")]
    files += sorted((HERE / "prompts").glob("*.md")) + sorted((HERE / "librarian-picks").glob("*.json"))
    files += [STUDIO / "product" / "compose.py", STUDIO / "product" / "media.py"]
    return {str(f.relative_to(REPO) if REPO in f.parents else f): hashlib.sha256(f.read_bytes()).hexdigest() for f in files}


def run_brief(ctx, bid):
    prompts0 = render_prompts.build(bid, None, json.loads((HERE / "librarian-picks" / f"picks-{bid}.json").read_text()))
    brief = prompts0["brief"]
    photos = ctx.assets.get(brief)
    results = {}
    U = None
    arms = STEP_ARMS[ctx.step]
    t_start = time.time()
    if "B" in arms or "C" in arms:
        ar = ArmRun(ctx, bid, "B", prompts0, photos)
        txt = ar.call("luna", "B1", 0.01, ctx.p.luna, prompts0["B1"])
        ar.write_llm("B1", prompts0["B1"], txt)
        U = extract_json(txt)
        (ctx.run / bid / "B1.json").write_text(json.dumps(U, indent=1, ensure_ascii=False))
    P = render_prompts.build(bid, json.dumps(U, ensure_ascii=False) if U else None,
                             json.loads((HERE / "librarian-picks" / f"picks-{bid}.json").read_text()))

    def arm_job(arm):
        ar = ArmRun(ctx, bid, arm if arm != "A_MAI" else "A_MAI", P, photos, U)
        t = time.time()
        try:
            if arm == "A":
                out, kind = ar.run_A()
            elif arm == "A_MAI":
                out, kind = ar.run_A(model="mai")
            else:
                out, kind = ar.run_BC()
            final = ctx.run / bid / f"{arm}-final{out.suffix}"
            shutil.copy(out, final)
            ar.ev("final", file=str(final.relative_to(ctx.run)))
            status = "ok"
        except CapReached:
            raise
        except Exception as e:  # noqa: BLE001
            ar.ev("arm_failed", error=f"{type(e).__name__}: {e}", tb=traceback.format_exc()[-1500:])
            final, kind, status = None, None, "failed"
        (ar.dir / "trace.json").write_text(json.dumps(ar.trace, indent=1, ensure_ascii=False))
        cost, secs = ctx.ledger.arm_cost(bid, arm)
        results[arm] = {"brief_id": bid, "arm": arm, "file": str(final.relative_to(ctx.run)) if final else None, "kind": kind,
                        "status": status, "cost_usd": cost, "seconds": secs, "wall_seconds": round(time.time() - t, 1)}

    with ThreadPoolExecutor(max_workers=len(arms)) as ex:
        futs = [ex.submit(arm_job, a) for a in arms]
        for f in futs:
            f.result()
    if "A" in arms and bid in MAI_BRIEFS and (ctx.run / bid / "A" / "A1.json").exists():
        arm_job("A_MAI")
    # B1 cost is shared by B and C; it is booked under B
    print(f"[{bid}] done in {time.time()-t_start:.0f}s: " + ", ".join(f"{a}={r['status']} ${r['cost_usd']}" for a, r in results.items()), flush=True)
    return list(results.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", required=True, choices=list(STEP_BRIEFS))
    ap.add_argument("--sim", action="store_true")
    ap.add_argument("--briefs")
    ap.add_argument("--run-dir")
    a = ap.parse_args()
    ctx = Ctx()
    ctx.step = a.step
    ctx.p = Sim() if a.sim else Live()
    ctx.run = Path(a.run_dir) if a.run_dir else MEDIA_ROOT / ("run-sim" if a.sim else "run-2026-09-26")
    ctx.run.mkdir(parents=True, exist_ok=True)
    ctx.ledger = Ledger(ctx.run / "ledger.jsonl", a.step)
    doc = yaml.safe_load((HERE / "BRIEFS.yaml").read_text())
    ctx.assets = Assets(ctx.run, doc)
    if not a.sim and a.step in ("stills", "films"):
        fz = ctx.run / "freeze.json"
        now = freeze_hashes()
        if fz.exists():
            old = json.loads(fz.read_text())
            diff = [k for k in set(old) | set(now) if old.get(k) != now.get(k)]
            if diff:
                print(f"FREEZE VIOLATION: changed since exam start: {diff}", flush=True)
                return 4
        else:
            fz.write_text(json.dumps(now, indent=1))
    briefs = a.briefs.split(",") if a.briefs else STEP_BRIEFS[a.step]
    outf = ctx.run / ("outputs.json" if a.step != "practice" else "practice-outputs.json")
    outs = json.loads(outf.read_text()) if outf.exists() else []
    done = {(o["brief_id"], o["arm"]) for o in outs if o.get("status") == "ok"}
    for bid in briefs:
        if all((bid, arm) in done for arm in STEP_ARMS[a.step]):
            print(f"[{bid}] already done, skipped", flush=True)
            continue
        try:
            res = run_brief(ctx, bid)
        except CapReached as e:
            print(f"CAP REACHED: {e}", flush=True)
            (ctx.run / "CAP-REACHED.txt").write_text(str(e))
            return 3
        outs = [o for o in outs if o["brief_id"] != bid] + res
        outf.write_text(json.dumps(outs, indent=1))
    spent = ctx.ledger._spent(a.step)
    print(f"STEP {a.step} finished. step spend US${spent:.2f} / cap {CAPS[a.step]}; total US${ctx.ledger._spent():.2f} / {TOTAL_CAP}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
