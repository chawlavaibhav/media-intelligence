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
from product import customer as customer_words
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
                                  json=json, ceiling_enforced=self.s.account_ceiling_enforced, simulated=(self.s.provider_mode == "simulated" or self.s.reasoning_mode == "simulated"))
        self.jinja.filters["plain"] = customer_words.plain
        self.jinja.filters["usd"] = lambda v: f"USD {dec(v):.2f}" if v not in (None, "") else "—"
        self.jinja.filters["loads"] = lambda v: json.loads(v) if v else {}
        self.routes = [
            ("GET", r"/healthz", self.healthz), ("GET", r"/login", self.login_form), ("POST", r"/login", self.login),
            ("POST", r"/logout", self.logout), ("GET", r"/invite/(?P<tok>[\w-]+)", self.invite_form),
            ("POST", r"/invite/(?P<tok>[\w-]+)", self.invite), ("GET", r"/", self.home), ("GET", r"/jobs/new", self.new_job),
            ("POST", r"/jobs", self.create_job), ("GET", r"/jobs/(?P<jid>job_\w+)", self.job_page),
            ("GET", r"/jobs/(?P<jid>job_\w+)/status", self.job_status),
            ("POST", r"/jobs/(?P<jid>job_\w+)/(?P<action>answer|approve|direction-change|changes|accept|reject|budget|upload|input|master|abandon|decide|taste|taste-change)", self.job_action),
            ("GET", r"/shelf", self.shelf_page), ("POST", r"/shelf/(?P<sid>shf_\w+)", self.shelf_action),
            ("GET", r"/assets/(?P<aid>ast_\w+)(?P<dl>/download)?", self.asset),
            ("GET", r"/ops", self.ops_home), ("GET", r"/ops/jobs/(?P<jid>job_\w+)", self.ops_job),
            ("POST", r"/ops/jobs/(?P<jid>job_\w+)/(?P<action>pause|resume|waive|release|retry|attest|override|override_recipe|override_final|close|approve_master)", self.ops_action),
            ("GET", r"/ops/lessons", self.ops_lessons), ("POST", r"/ops/lessons/(?P<lid>lsn_\w+)", self.ops_lesson_action),
            ("GET", r"/ops/digest", self.ops_digest), ("POST", r"/ops/lessons/(?P<lid>lsn_\w+)/undo", self.ops_lesson_undo),
            ("GET", r"/ops/rulebook", self.ops_rulebook), ("GET", r"/ops/library", self.ops_library),
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
        if role == "operator" and u["role"] in ("operator", "founder"):
            return u                  # staff pages: founder and operators view; only the founder can decide (authority.py)
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
        if u["role"] in ("operator", "founder"):
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
        gw = st.artifact(jid, "gateway_report")
        report = None
        if finals and j["state"] in ("ready_for_review", "accepted", "revising", "rejected"):
            from product.stations.tasters import required
            req = required(self.svc.orch, jid)
            report = [verify.gateway(st, jid, a, req) for a in finals]
        deliverables = [a for a in st.assets(jid) if a["role"] == "deliverable"]
        recipe = st.artifact(jid, "recipe")
        direction = dict(recipe, beats=[dict(s, first_frame=s["first_frame"]) for s in recipe.get("shots", [])]) if recipe else None
        master = st.node(jid, "master")
        return {"job": j, "brief": st.original_brief(jid), "intent": st.artifact(jid, "understanding"), "direction": direction,
                "feasibility": st.artifact(jid, "feasibility"), "review": st.artifact(jid, "final_review"), "quote": st.artifact(jid, "quote"),
                "answers": st.artifact(jid, "answers"), "gateway_saved": gw,
                "master": st.asset(master["selected_asset_id"]) if master and master["selected_asset_id"] else None,
                "preview": [a for a in st.assets(jid, role="preview")][-1:], "finals": [st.asset(a) for a in finals], "report": report,
                "deliverables": deliverables, "uploads": st.assets(jid, source="customer"), "ledger": st.ledger_summary(jid),
                "feedback": st.feedback(jid), "deliveries": st.deliveries(jid), "revision": st.artifact(jid, "revision_plan"),
                "account": st.account(j["account_id"]), "nodes": [n for n in st.nodes(jid) if n["status"] != "retired"],
                "plan_note": st.artifact(jid, "plan_note"), "plan_objections": _current_objections(st, jid),
                "customer_notes": (st.artifact(jid, "customer_notes") or {}).get("notes", []),
                "customer_decision": st.artifact(jid, "customer_decision"),
                "progress": customer_words.progress(st, jid),
                "checked": customer_words.checked_list(report) if report else [],
                "taste": [st.asset(st.node(jid, x)["selected_asset_id"]) for x in _taste_nodes(self.svc.orch, jid)
                          if st.node(jid, x) and st.node(jid, x)["selected_asset_id"]] if j["state"] == "awaiting_taste" else []}

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
                      note=f.get("note", ""), accept_objections=f.get("accept_objections") == "yes")
        elif action == "taste":
            o.approve_taste(jid, by=who)
        elif action == "taste-change":
            o.change_taste(jid, by=who, text=f.get("text", "")[:2000])
        elif action == "decide":
            o.decide(jid, by=who, choice=f.get("choice", ""), note=f.get("note", "")[:1000], budget_usd=f.get("budget_usd") or None)
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
        elif action == "input":
            for x in req.files:
                self.svc.add_upload(u, jid, role="product", filename=x["filename"], data=x["data"], label=f.get("label") or None)
            feas = self.store.artifact(jid, "feasibility") or {}
            accepted = [{"instead_of": a["for_action"], "use": a["alternative"]} for i, a in enumerate(feas.get("alternatives", []))
                        if f.get(f"alt_{i}") == "yes"]
            o.provide_input(jid, by=who, accepted_alternatives=accepted, facts=[f.get("facts", "")], note=f.get("note", ""))
        elif action == "master":
            o.approve_master(jid, by=who)
        elif action == "abandon":
            o.abandon(jid, who, f.get("reason", "")[:2000] or "closed by the customer")
        return redirect(f"/jobs/{jid}")

    def shelf_page(self, req):
        u = self.user(req, "customer")
        return self.page("shelf.html", req, items=self.svc.orch.shelf.items(u["account_id"]))

    def shelf_action(self, req, sid):
        u = self.user(req, "customer")
        self.svc.orch.shelf.decide(u["account_id"], sid, approve=req.form.get("decision") == "approve", by=u["email"])
        return redirect("/shelf")

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
        o = self.svc.orch
        finals = [a["id"] for a in v["finals"]]
        from product import cost
        from product.stations.tasters import required
        req_checks = required(o, jid) if st.artifact(jid, "understanding") and st.artifact(jid, "recipe") else {}
        forms = {k: st.artifact(jid, k) for k in ("order_slip", "understanding", "feasibility", "recipe", "recipe_check", "production_log",
                                                  "final_review", "lessons", "change_request")}
        trays = {w: st.artifact(jid, f"tray:{w}") for w in ("pantry_checker", "chef", "recipe_checker")}
        v.update(events=st.events(jid), attempts=st.attempts(jid), llm=st.llm_calls(jid), assets=st.assets(jid),
                 gateway=[verify.gateway(st, jid, a, req_checks) for a in finals], forms=forms, trays=trays,
                 overrides=st.overrides(jid), founder_decision=st.artifact(jid, "founder_decision"),
                 cost=cost.reasoning_report(o, jid, st.artifact(jid, "recipe")) if st.artifact(jid, "understanding") else None,
                 metrics=learning.metrics(st, jid), is_founder=u["role"] == "founder", lessons=o.lessons.all(jid))
        v.update(attestable={r["check_id"]: verify.attestable(r["check_id"]) for g in v["gateway"] for r in g["table"]
                             if verify.attestable(r["check_id"])}, non_waivable=verify.NON_WAIVABLE)
        return self.page("ops_job.html", req, **v)

    def ops_action(self, req, jid, action):
        u = self.user(req, "operator")
        j = self.store.job(jid)
        o = self.svc.orch
        f = req.form
        who = f"{u['role']}:{u['email']}"
        try:
            if action == "pause":           # anyone on the team may stop work; deciding what happens next is the founder's
                self.store.transition(jid, j["state"], "paused_operator", actor=who, data={"reason": f.get("reason", "")},
                                      resume_state=j["state"], pause_reason=f.get("reason", "paused by our team"))
            elif action in ("resume", "retry"):
                o.founder_resume(jid, session=req.session, to=f.get("to") or None, reason=f.get("reason", ""))
            elif action == "waive":
                o.waive_check(jid, session=req.session, asset_id=f["asset_id"], check_id=f["check_id"], reason=f.get("reason", ""))
            elif action == "attest":
                o.confirm_check(jid, session=req.session, asset_id=f["asset_id"], check_id=f["check_id"], note=f.get("note", ""),
                                outcome=f.get("outcome", "PASS"))
            elif action == "release":
                o.release(jid, session=req.session)
            elif action in ("override", "override_recipe"):
                o.override_recipe(jid, session=req.session, reason=f.get("reason", ""))
            elif action == "override_final":
                o.override_final_review(jid, session=req.session, reason=f.get("reason", ""))
            elif action == "approve_master":
                o.approve_master(jid, by=who, founder_session=req.session)
            elif action == "close":
                o.abandon(jid, who, f.get("reason", "closed by the founder"), founder_session=req.session)
        except PermissionError as e:
            return Response("403 Forbidden", self.render("error.html", req, message=str(e)))
        except ValueError as e:
            raise Invalid(str(e))
        return redirect(f"/ops/jobs/{jid}")

    def ops_lessons(self, req):
        u = self.user(req, "operator")
        return self.page("ops_lessons.html", req, lessons=self.svc.orch.lessons.all(), is_founder=u["role"] == "founder", json=json)

    def ops_digest(self, req):
        """The founder's weekly digest (amendment 1 §4): what the kitchen learned by itself, from which job, on what evidence,
        before → after — with Undo per item; plus the money/override/safety lessons that wait for the founder."""
        u = self.user(req, "operator")
        rows = self.svc.orch.lessons.digest(7)
        groups = {"applied": [], "founder_only": [], "waiting_support": [], "rolled_back": [], "undone": [], "other": []}
        for r in rows:
            groups.get(r["status"], groups["other"]).append(r)
        return self.page("ops_digest.html", req, groups=groups, is_founder=u["role"] == "founder", json=json)

    def ops_lesson_undo(self, req, lid):
        self.user(req, "operator")
        o = self.svc.orch
        row = o.lessons.lesson(lid)
        from product import authority
        try:
            proof = authority.founder_proof(self.store, req.session, job_id=row["job_id"], action="undo a lesson")
            o.lessons.undo(lid, founder=proof, note=req.form.get("note", ""))
        except PermissionError as e:
            return Response("403 Forbidden", self.render("error.html", req, message=str(e)))
        except (ValueError, KeyError) as e:
            raise Invalid(str(e))
        return redirect("/ops/digest")

    def ops_lesson_action(self, req, lid):
        self.user(req, "operator")
        f = req.form
        o = self.svc.orch
        row = o.lessons.lesson(lid)
        from product import authority
        try:
            proof = authority.founder_proof(self.store, req.session, job_id=row["job_id"], action="decide a lesson")
            edited = json.loads(f["edited"]) if f.get("decision") == "edit" and f.get("edited") else None
            o.lessons.decide(lid, founder=proof, decision=f.get("decision", ""), note=f.get("note", ""), edited_diff=edited)
        except PermissionError as e:
            return Response("403 Forbidden", self.render("error.html", req, message=str(e)))
        except (ValueError, KeyError) as e:
            raise Invalid(str(e))
        return redirect("/ops/lessons")

    def ops_rulebook(self, req):
        self.user(req, "operator")
        from product import flow, rulebook
        rb = self.svc.orch.rulebook
        cards = [(w, rb.card(w), rb.history(w)) for w in rulebook.AI_WORKERS + rulebook.CODE_WORKERS]
        return self.page("ops_rulebook.html", req, cards=cards, forms=rulebook.forms(), send_backs=flow.SEND_BACKS, models=self.s.models,
                         qualified=tuple(j for j in ("recipe_checker", "small_taster", "big_taster") if self.svc.orch.qualified(j)))

    def ops_library(self, req):
        self.user(req, "operator")
        o = self.svc.orch
        return self.page("ops_library.html", req, equipment=o.equipment.rows(), recipes=o.recipes.all(None, staff=True),
                         failures=o.failures.all(None, staff=True))

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


def _current_objections(st, jid):
    """The reviewer's objections, only while they are about the plan the customer is looking at."""
    obj = st.artifact(jid, "plan_objections")
    return obj if obj and obj["recipe_version"] == len(st.artifact_versions(jid, "recipe")) else None


def _taste_nodes(k, jid):
    from product.stations.head_cook import taste_nodes
    return taste_nodes(k, jid)
