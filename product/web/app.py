"""The customer and operator web application (WSGI, stdlib + Jinja2).

Every customer request is authenticated and scoped to the caller's account (Service.job / asset_for raise
for anything else); every state-changing request carries a CSRF token bound to the session; media is served
only through an authorised asset route. No provider names or internals on customer pages.

    python3 -m product.web.app --host 127.0.0.1 --port 8080
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import logging
import mimetypes
import re
import secrets
import traceback
from email.parser import BytesParser
from email.policy import default as email_default
from http import cookies
from pathlib import Path
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs, quote
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

from jinja2 import Environment, FileSystemLoader, select_autoescape

from product import config, learning, states, verify
from product.service import Invalid, Service
from product.store import Store, dec

log = logging.getLogger("mi.web")
HERE = Path(__file__).parent
COOKIE = "mi_session"


class Request:
    def __init__(self, environ, max_bytes):
        self.env = environ
        self.method = environ["REQUEST_METHOD"]
        self.path = environ.get("PATH_INFO", "/")
        self.query = {k: v[0] for k, v in parse_qs(environ.get("QUERY_STRING", "")).items()}
        c = cookies.SimpleCookie(environ.get("HTTP_COOKIE", ""))
        self.session = c[COOKIE].value if COOKIE in c else None
        self.form, self.files, self.lists = {}, [], {}
        if self.method == "POST":
            n = int(environ.get("CONTENT_LENGTH") or 0)
            if n > max_bytes * 6:
                raise Invalid("upload too large")
            body = environ["wsgi.input"].read(n) if n else b""
            ctype = environ.get("CONTENT_TYPE", "")
            if ctype.startswith("multipart/form-data"):
                msg = BytesParser(policy=email_default).parsebytes(b"Content-Type: " + ctype.encode() + b"\r\n\r\n" + body)
                for part in msg.iter_parts():
                    name = part.get_param("name", header="content-disposition")
                    fn = part.get_filename()
                    data = part.get_payload(decode=True) or b""
                    if fn:
                        if data:
                            self.files.append({"field": name, "filename": fn, "data": data, "content_type": part.get_content_type()})
                    else:
                        v = data.decode("utf-8", "replace")
                        self.form.setdefault(name, v)
                        self.lists.setdefault(name, []).append(v)
            else:
                for k, v in parse_qs(body.decode("utf-8", "replace"), keep_blank_values=True).items():
                    self.form[k] = v[0]
                    self.lists[k] = v

    def getlist(self, k):
        return self.lists.get(k, [])


class Response(Exception):
    def __init__(self, status="200 OK", body=b"", headers=None):
        self.status, self.body, self.headers = status, body, headers or []


def redirect(to, extra_headers=None):
    return Response("303 See Other", b"", [("Location", to)] + (extra_headers or []))


class App:
    def __init__(self, settings=None):
        self.s = settings or config.load()
        self.store = Store(self.s.db_path)
        self.svc = Service(self.s, self.store)
        self.secret = (self.s.secret("MI_SECRET_KEY") or self._local_secret()).encode()
        self.jinja = Environment(loader=FileSystemLoader(HERE / "templates"), autoescape=select_autoescape(["html"]))
        self.jinja.globals.update(states=states, label=states.label, rail=states.RAIL, rail_position=states.rail_position,
                                  json=json, simulated=(self.s.provider_mode == "simulated" or self.s.reasoning_mode == "simulated"))
        self.jinja.filters["usd"] = lambda v: f"USD {dec(v):.2f}" if v not in (None, "") else "—"
        self.jinja.filters["loads"] = lambda v: json.loads(v) if v else {}
        self.routes = [
            ("GET", r"/healthz", self.healthz), ("GET", r"/login", self.login_form), ("POST", r"/login", self.login),
            ("POST", r"/logout", self.logout), ("GET", r"/invite/(?P<tok>[\w-]+)", self.invite_form),
            ("POST", r"/invite/(?P<tok>[\w-]+)", self.invite), ("GET", r"/", self.home), ("GET", r"/jobs/new", self.new_job),
            ("POST", r"/jobs", self.create_job), ("GET", r"/jobs/(?P<jid>job_\w+)", self.job_page),
            ("GET", r"/jobs/(?P<jid>job_\w+)/status", self.job_status),
            ("POST", r"/jobs/(?P<jid>job_\w+)/(?P<action>answer|approve|direction-change|changes|accept|reject|budget|upload)", self.job_action),
            ("GET", r"/assets/(?P<aid>ast_\w+)(?P<dl>/download)?", self.asset),
            ("GET", r"/ops", self.ops_home), ("GET", r"/ops/jobs/(?P<jid>job_\w+)", self.ops_job),
            ("POST", r"/ops/jobs/(?P<jid>job_\w+)/(?P<action>pause|resume|waive|release|retry)", self.ops_action),
            ("POST", r"/ops/accounts", self.ops_account), ("POST", r"/ops/invites", self.ops_invite),
        ]

    def _local_secret(self):
        p = self.s.data_dir / ".secret_key"
        if not p.exists():
            p.write_text(secrets.token_hex(32))
            p.chmod(0o600)
        return p.read_text().strip()

    # ── plumbing ───────────────────────────────────────────────────────────────────────────────
    def __call__(self, environ, start_response):
        try:
            req = Request(environ, self.s.max_upload_bytes)
            for method, pat, fn in self.routes:
                m = re.fullmatch(pat, req.path)
                if m and method == req.method:
                    if method == "POST" and fn not in (self.login, self.invite):
                        self._csrf(req)
                    raise fn(req, **m.groupdict()) or Response("204 No Content")
            raise Response("404 Not Found", b"not found")
        except Response as r:
            status, body, headers = r.status, r.body, r.headers
        except PermissionError:
            status, body, headers = "404 Not Found", b"not found", []
        except Invalid as e:
            status, body, headers = "400 Bad Request", self.render("error.html", None, message=str(e)), []
        except Exception:  # noqa: BLE001
            log.error("unhandled: %s", config.scrub(traceback.format_exc()))
            status, body, headers = "500 Internal Server Error", b"something went wrong; the team has been notified", []
        if isinstance(body, str):
            body = body.encode()
        base = [("X-Content-Type-Options", "nosniff"), ("X-Frame-Options", "DENY"), ("Referrer-Policy", "same-origin"),
                ("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; media-src 'self'; style-src 'self' 'unsafe-inline'; "
                                            "script-src 'none'; frame-ancestors 'none'; form-action 'self'")]
        if not any(h[0] == "Content-Type" for h in headers):
            headers.append(("Content-Type", "text/html; charset=utf-8"))
        start_response(status, base + headers + [("Content-Length", str(len(body)))])
        return [body]

    def _csrf(self, req):
        want = hmac.new(self.secret, (req.session or "").encode(), hashlib.sha256).hexdigest()
        if not req.session or not hmac.compare_digest(req.form.get("csrf", ""), want):
            raise Response("403 Forbidden", b"form expired; reload the page and try again")

    def csrf_for(self, req):
        return hmac.new(self.secret, (req.session or "").encode(), hashlib.sha256).hexdigest()

    def user(self, req, role=None):
        u = self.svc.session_user(req.session)
        if u is None:
            raise redirect("/login?next=" + quote(req.path))
        if role and u["role"] != role:
            raise PermissionError
        return u

    def render(self, tpl, req, **ctx):
        u = self.svc.session_user(req.session) if req else None
        return self.jinja.get_template(tpl).render(user=u, csrf=self.csrf_for(req) if req else "", **ctx)

    def page(self, tpl, req, **ctx):
        return Response("200 OK", self.render(tpl, req, **ctx))

    # ── access ─────────────────────────────────────────────────────────────────────────────────
    def healthz(self, req):
        self.store.q1("SELECT 1")
        return Response("200 OK", b'{"ok":true}', [("Content-Type", "application/json")])

    def login_form(self, req):
        return self.page("login.html", req, next=req.query.get("next", "/"), error=None)

    def login(self, req):
        tok = self.svc.login(req.form.get("email", ""), req.form.get("password", ""))
        if not tok:
            return Response("401 Unauthorized", self.render("login.html", req, next="/", error="Email or password not recognised."))
        nxt = req.form.get("next", "/")
        nxt = nxt if nxt.startswith("/") and not nxt.startswith("//") else "/"
        secure = "; Secure" if self.s.base_url.startswith("https") else ""
        return redirect(nxt, [("Set-Cookie", f"{COOKIE}={tok}; HttpOnly; SameSite=Lax; Path=/; Max-Age=1209600{secure}")])

    def logout(self, req):
        if req.session:
            self.svc.logout(req.session)
        return redirect("/login", [("Set-Cookie", f"{COOKIE}=; Max-Age=0; Path=/")])

    def invite_form(self, req, tok):
        return self.page("invite.html", req, tok=tok, error=None)

    def invite(self, req, tok):
        try:
            self.svc.redeem_invite(tok, name=req.form.get("name", ""), password=req.form.get("password", ""))
        except Invalid as e:
            return Response("400 Bad Request", self.render("invite.html", req, tok=tok, error=str(e)))
        return redirect("/login")

    # ── customer ───────────────────────────────────────────────────────────────────────────────
    def home(self, req):
        u = self.user(req)
        if u["role"] == "operator":
            raise redirect("/ops")
        return self.page("home.html", req, jobs=self.store.jobs_for_account(u["account_id"]), account=self.store.account(u["account_id"]))

    def new_job(self, req):
        u = self.user(req, "customer")
        return self.page("new_job.html", req, account=self.store.account(u["account_id"]))

    def create_job(self, req):
        u = self.user(req, "customer")
        f = req.form
        uploads = [{"role": {"product_photos": "product", "logo": "logo", "references": "reference"}.get(x["field"], "reference"),
                    "filename": x["filename"], "data": x["data"], "content_type": x["content_type"]} for x in req.files]
        jid = self.svc.submit(u, title=f.get("title", ""), media=f.get("media", ""), text=f.get("brief", ""),
                              formats=req.getlist("formats"), duration_s=f.get("duration_s"),
                              exact_strings=[s for s in f.get("exact_text", "").splitlines()],
                              product={"name": f.get("product_name"), "brand": f.get("brand"), "category": f.get("category"),
                                       "description": f.get("product_description")},
                              brand_colours=[c.strip() for c in f.get("brand_colours", "").split(",")],
                              max_budget_usd=f.get("max_budget_usd"), uploads=uploads,
                              allow_preview_spend=f.get("allow_preview") == "yes", references_note=f.get("references_note", ""))
        return redirect(f"/jobs/{jid}")

    def _job_view(self, jid, u):
        j = self.svc.job(u, jid)
        st = self.store
        finals = [n["selected_asset_id"] for n in st.nodes(jid) if n["kind"] in ("compose_still", "assemble") and n["selected_asset_id"]]
        gw = st.artifact(jid, "gateway")
        report = None
        if finals and j["state"] in ("ready_for_review", "accepted", "revising", "rejected"):
            report = [verify.gateway(st, jid, a, (gw or {}).get("required", {})) for a in finals]
        deliverables = [a for a in st.assets(jid) if a["role"] == "deliverable"]
        return {"job": j, "brief": st.original_brief(jid), "intent": st.artifact(jid, "intent"), "direction": st.artifact(jid, "direction"),
                "review": st.artifact(jid, "review"), "quote": st.artifact(jid, "quote"), "answers": st.artifact(jid, "answers"),
                "preview": [a for a in st.assets(jid, role="preview")], "finals": [st.asset(a) for a in finals], "report": report,
                "deliverables": deliverables, "uploads": st.assets(jid, source="customer"), "ledger": st.ledger_summary(jid),
                "feedback": st.feedback(jid), "deliveries": st.deliveries(jid), "revision": st.artifact(jid, "revision_plan"),
                "account": st.account(j["account_id"]), "nodes": st.nodes(jid)}

    def job_page(self, req, jid):
        u = self.user(req)
        return self.page("job.html", req, **self._job_view(jid, u))

    def job_status(self, req, jid):
        u = self.user(req)
        j = self.svc.job(u, jid)
        body = json.dumps({"state": j["state"], "label": states.label(j["state"]), "updated": j["updated"]})
        return Response("200 OK", body, [("Content-Type", "application/json")])

    def job_action(self, req, jid, action):
        u = self.user(req, "customer")
        j = self.svc.job(u, jid)
        o = self.svc.orch
        f = req.form
        who = u["email"]
        if action == "answer":
            ans = {k[2:]: v for k, v in f.items() if k.startswith("q_") and v.strip()}
            for k in [k[9:] for k in f if k.startswith("delegate_")]:
                ans[k] = "decide for me (use your default)"
            o.answer(jid, ans, who)
        elif action == "approve":
            o.approve(jid, by=who, budget_usd=f.get("budget_usd") or self.store.artifact(jid, "quote")["recommended_budget_usd"],
                      note=f.get("note", ""))
        elif action == "direction-change":
            o.request_direction_change(jid, f.get("text", "")[:2000], who)
        elif action == "changes":
            items = []
            for i in range(1, 6):
                t = f.get(f"change_{i}", "").strip()
                if t:
                    items.append({"target": f.get(f"target_{i}") or None, "text": t[:2000]})
            if not items:
                raise Invalid("describe at least one change")
            o.request_changes(jid, who, items)
        elif action == "accept":
            o.accept(jid, who)
        elif action == "reject":
            o.reject(jid, who, f.get("reason", "")[:2000] or "rejected")
        elif action == "budget":
            self.svc.raise_budget(u, jid, f.get("budget_usd"))
        elif action == "upload":
            for x in req.files:
                self.svc.add_upload(u, jid, role=f.get("role", "reference"), filename=x["filename"], data=x["data"])
        return redirect(f"/jobs/{jid}")

    def asset(self, req, aid, dl=None):
        u = self.user(req)
        a = self.svc.asset_for(u, aid)
        if u["role"] == "customer" and a["source"] == "generated" and a["role"] != "preview":
            raise PermissionError         # customers see previews, their uploads and released cuts — not intermediate draws
        if u["role"] == "customer" and a["role"] == "deliverable" and self.store.job(a["job_id"])["state"] not in (
                "ready_for_review", "accepted", "revising", "rejected"):
            raise PermissionError         # nothing is shown to the customer before the gateway / operator releases it
        data = Path(a["path"]).read_bytes()
        headers = [("Content-Type", a["content_type"] or mimetypes.guess_type(a["path"])[0] or "application/octet-stream"),
                   ("Cache-Control", "private, max-age=300")]
        if dl:
            if u["role"] == "customer" and not any(d["asset_id"] == aid for d in self.store.deliveries(a["job_id"])):
                raise PermissionError     # downloads only of the accepted, delivered version
            headers.append(("Content-Disposition", f'attachment; filename="{Path(a["path"]).name}"'))
        if a["content_type"] == "image/svg+xml":
            headers.append(("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'"))
        return Response("200 OK", data, headers)

    # ── operator ───────────────────────────────────────────────────────────────────────────────
    def ops_home(self, req):
        self.user(req, "operator")
        accounts = self.store.q("SELECT * FROM accounts ORDER BY created")
        return self.page("ops_home.html", req, jobs=self.store.all_jobs(), accounts=accounts,
                         invite=req.query.get("invite"))

    def ops_job(self, req, jid):
        u = self.user(req, "operator")
        v = self._job_view(jid, u)
        st = self.store
        finals = [a["id"] for a in v["finals"]]
        gw = st.artifact(jid, "gateway") or {}
        v.update(events=st.events(jid), attempts=st.attempts(jid), llm=st.llm_calls(jid), assets=st.assets(jid),
                 checks={a: st.checks(a) for a in finals},
                 gateway=[verify.gateway(st, jid, a, gw.get("required", {})) for a in finals],
                 canon=st.artifact(jid, "canon_trace"), dreview=st.artifact(jid, "direction_review"),
                 metrics=learning.metrics(st, jid), controls=verify.controls())
        return self.page("ops_job.html", req, **v)

    def ops_action(self, req, jid, action):
        u = self.user(req, "operator")
        j = self.store.job(jid)
        who = f"operator:{u['email']}"
        f = req.form
        if action == "pause":
            self.store.transition(jid, j["state"], "paused_operator", actor=who, data={"reason": f.get("reason", "")}, resume_state=j["state"],
                                  pause_reason=f.get("reason", "paused by operator"))
        elif action in ("resume", "retry"):
            target = f.get("to") or j["resume_state"]
            self.store.transition(jid, j["state"], target, actor=who, data={"reason": f.get("reason", "")}, pause_reason=None)
        elif action == "waive":
            if len(f.get("reason", "").strip()) < 10:
                raise Invalid("a waiver needs a reason (at least a sentence)")
            self.store.waive(jid, f["asset_id"], f["check_id"], who, f["reason"].strip())
        elif action == "release":
            self.svc.orch.release_hold(jid, who)
        return redirect(f"/ops/jobs/{jid}")

    def ops_account(self, req):
        self.user(req, "operator")
        self.store.create_account(req.form["name"], ceiling_usd=req.form.get("ceiling_usd") or "25", auto_approve=req.form.get("auto_approve") == "yes")
        return redirect("/ops")

    def ops_invite(self, req):
        u = self.user(req, "operator")
        tok = self.svc.create_invite(email=req.form["email"], role=req.form.get("role", "customer"),
                                     account_id=req.form.get("account_id") or None, by=u["email"])
        return redirect("/ops?invite=" + quote(f"{self.s.base_url}/invite/{tok}"))


class _ThreadingServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


class _QuietHandler(WSGIRequestHandler):
    def log_message(self, fmt, *args):
        log.info("%s %s", self.address_string(), fmt % args)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    app = App()
    srv = make_server(a.host, a.port, app, server_class=_ThreadingServer, handler_class=_QuietHandler)
    log.info("serving on http://%s:%s (data %s, providers=%s, reasoning=%s)", a.host, a.port, app.s.data_dir,
             app.s.provider_mode, app.s.reasoning_mode)
    srv.serve_forever()


if __name__ == "__main__":
    main()
