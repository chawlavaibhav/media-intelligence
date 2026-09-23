"""The product's application service: the operations the web app (and tests) perform. Every customer
operation is scoped to the caller's account; uploads are validated; the original brief is frozen at
submission and never rewritten."""
from __future__ import annotations

import hashlib
import json
import re
import secrets
from decimal import Decimal, InvalidOperation
from pathlib import Path

from product.config import Settings
from product.orchestrator import PREVIEW_ALLOWANCE_USD, Orchestrator
from product.store import Store, dec, money, new_id, utc_now

ALLOWED_UPLOADS = {
    "image/png": (b"\x89PNG\r\n\x1a\n",), "image/jpeg": (b"\xff\xd8\xff",), "image/webp": (b"RIFF",),
    "image/svg+xml": (b"<svg", b"<?xml"), "application/pdf": (b"%PDF",),
}
ROLES = ("product", "logo", "reference")
FORMATS = ("1:1", "4:5", "9:16", "16:9")


class Invalid(ValueError):
    pass


def sniff(data: bytes, declared: str) -> str:
    head = data[:64].lstrip()
    for ctype, magics in ALLOWED_UPLOADS.items():
        if any(head.startswith(m) for m in magics):
            if ctype == "image/webp" and data[8:12] != b"WEBP":
                continue
            return ctype
    raise Invalid(f"unsupported file type ({declared or 'unknown'}); upload PNG, JPEG, WEBP, SVG or PDF")


def hash_pw(pw: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    h = hashlib.scrypt(pw.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    return f"scrypt${salt.hex()}${h.hex()}"


def check_pw(pw: str, stored: str | None) -> bool:
    if not stored or not stored.startswith("scrypt$"):
        return False
    _, salt, h = stored.split("$")
    return secrets.compare_digest(hash_pw(pw, bytes.fromhex(salt)).split("$")[2], h)


def token_hash(tok: str) -> str:
    return hashlib.sha256(tok.encode()).hexdigest()


class Service:
    def __init__(self, settings: Settings, store: Store, orch: Orchestrator | None = None):
        self.s, self.store = settings, store
        self.orch = orch or Orchestrator(settings, store)

    # ── accounts and access ──────────────────────────────────────────────────────────────────
    def founder_exists(self) -> bool:
        return self.store.q1("SELECT 1 FROM users WHERE role='founder'") is not None

    def create_invite(self, *, email: str, role: str, account_id: str | None, by: str) -> str:
        if role not in ("customer", "operator", "founder"):
            raise Invalid("role")
        if role == "founder" and self.founder_exists():
            raise Invalid("a founder account already exists; there is exactly one founder")
        tok = secrets.token_urlsafe(24)
        with self.store.tx() as c:
            c.execute("INSERT INTO invites VALUES (?,?,?,?,?,NULL)", (token_hash(tok), account_id, email.strip().lower(), role, utc_now()))
        return tok

    def redeem_invite(self, token: str, *, name: str, password: str) -> str:
        if len(password) < 10:
            raise Invalid("choose a password of at least 10 characters")
        row = self.store.q1("SELECT * FROM invites WHERE token_hash=?", (token_hash(token),))
        if not row or row["used_at"]:
            raise Invalid("this invitation is not valid (unknown or already used)")
        uid = new_id("usr")
        with self.store.tx() as c:
            if c.execute("SELECT 1 FROM users WHERE email=?", (row["email"],)).fetchone():
                raise Invalid("an account already exists for this email")
            if row["role"] == "founder" and c.execute("SELECT 1 FROM users WHERE role='founder'").fetchone():
                raise Invalid("a founder account already exists; there is exactly one founder")
            c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?)", (uid, row["account_id"], row["email"], name.strip()[:80],
                                                                   row["role"], hash_pw(password), utc_now()))
            c.execute("UPDATE invites SET used_at=? WHERE token_hash=?", (utc_now(), token_hash(token)))
        return uid

    def login(self, email: str, password: str) -> str | None:
        u = self.store.user_by_email(email)
        if not u or not check_pw(password, u["pw_hash"]):
            return None
        tok = secrets.token_urlsafe(32)
        import time
        with self.store.tx() as c:
            c.execute("INSERT INTO sessions VALUES (?,?,?,?)", (token_hash(tok), u["id"], utc_now(), time.time() + 14 * 86400))
        return tok

    def session_user(self, tok: str | None):
        if not tok:
            return None
        import time
        row = self.store.q1("SELECT * FROM sessions WHERE token_hash=?", (token_hash(tok),))
        if not row or row["expires"] < time.time():
            return None
        return self.store.user(row["user_id"])

    def logout(self, tok: str):
        with self.store.tx() as c:
            c.execute("DELETE FROM sessions WHERE token_hash=?", (token_hash(tok),))

    # ── jobs ────────────────────────────────────────────────────────────────────────────────
    def submit(self, user, *, title: str, media: str, text: str, formats: list, duration_s, exact_strings: list,
               product: dict, brand_colours: list, max_budget_usd, uploads: list, allow_preview_spend: bool,
               references_note: str = "", forbidden_words: list = ()) -> str:
        if user["role"] != "customer" or not user["account_id"]:
            raise Invalid("only a customer account can submit jobs")
        if media not in ("image", "video"):
            raise Invalid("choose image or video")
        if not text.strip():
            raise Invalid("tell us what you want — a sentence is enough")
        formats = [f for f in formats if f in FORMATS] or (["9:16"] if media == "video" else ["1:1"])
        if media == "video":
            formats = [f for f in formats if f in ("9:16", "16:9")][:1] or ["9:16"]
            try:
                duration_s = float(duration_s or 15)
            except ValueError:
                raise Invalid("duration must be a number of seconds")
            if not 6 <= duration_s <= 30:
                raise Invalid("films in this beta run 6–30 seconds")
        else:
            duration_s = None
        try:
            cap = dec(max_budget_usd or 0)
        except InvalidOperation:
            raise Invalid("budget must be a number")
        acct = self.store.account(user["account_id"])
        if cap <= 0 or cap > dec(acct["ceiling_usd"]):
            raise Invalid(f"set a maximum production budget between USD 1 and your account limit (USD {acct['ceiling_usd']})")
        if not allow_preview_spend:
            raise Invalid("please allow the small planning allowance so we can prepare the creative direction")
        colours = [c for c in brand_colours if re.fullmatch(r"#[0-9a-fA-F]{6}", c or "")]
        brief = {"text": text.strip()[:6000], "media": media, "formats": formats, "duration_s": duration_s,
                 "exact_strings": [s for s in (x.strip() for x in exact_strings) if s][:8],
                 "product": {k: (product.get(k) or "").strip()[:300] for k in ("name", "brand", "category", "description")},
                 "brand_colours": colours, "max_budget_usd": money(cap), "references_note": references_note[:1000],
                 "forbidden_words": [w for w in forbidden_words if w][:20], "submitted_by": user["email"], "submitted_utc": utc_now()}
        allowance = min(PREVIEW_ALLOWANCE_USD, cap)
        jid = self.store.create_job(account_id=user["account_id"], user_id=user["id"], title=title.strip()[:120] or text[:60],
                                    media=media, brief=brief, budget_usd=allowance)
        self.store.set_job(jid, budget_authorised_by=f"{user['email']} (planning allowance at submission)", budget_authorised_at=utc_now())
        for up in uploads:
            self.add_upload(user, jid, **up)
        return jid

    def add_upload(self, user, job_id, *, role: str, filename: str, data: bytes, content_type: str = ""):
        job = self.job(user, job_id)
        if role not in ROLES:
            raise Invalid("unknown upload role")
        if not data or len(data) > self.s.max_upload_bytes:
            raise Invalid(f"files must be under {self.s.max_upload_bytes // (1024 * 1024)} MB")
        ctype = sniff(data, content_type)
        if ctype == "image/svg+xml" and re.search(rb"<script|javascript:|onload=", data, re.I):
            raise Invalid("SVG files with scripts are not accepted")
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", Path(filename).name)[:80] or "upload"
        d = self.s.media_dir / job["id"] / "uploads"
        d.mkdir(parents=True, exist_ok=True)
        p = d / f"{secrets.token_hex(4)}-{safe}"
        p.write_bytes(data)
        return self.store.add_asset(job["id"], path=p, kind="upload", source="customer", content_type=ctype, role=role,
                                    status="supplied", meta={"filename": safe, "uploaded_by": user["email"]})

    def job(self, user, job_id):
        if user["role"] in ("operator", "founder"):
            j = self.store.job(job_id)
        else:
            j = self.store.job_for_account(job_id, user["account_id"])
        if j is None:
            raise PermissionError("not found")
        return j

    def asset_for(self, user, asset_id):
        a = self.store.asset(asset_id)
        if a is None:
            raise PermissionError("not found")
        self.job(user, a["job_id"])        # raises for another account's asset
        return a

    def raise_budget(self, user, job_id, new_budget):
        j = self.job(user, job_id)
        acct = self.store.account(j["account_id"])
        b = dec(new_budget)
        if b > dec(acct["ceiling_usd"]):
            raise Invalid(f"above the account limit USD {acct['ceiling_usd']}")
        if b <= dec(j["budget_usd"]):
            raise Invalid("the new budget must be higher than the current one")
        self.store.set_job(job_id, budget_usd=money(b), budget_authorised_by=user["email"], budget_authorised_at=utc_now())
        self.store.event(job_id, user["email"], "budget_raised", {"to": money(b)})
        if j["state"] == "paused_budget":
            self.store.transition(job_id, "paused_budget", j["resume_state"], actor=user["email"], pause_reason=None)
