"""Black-box customer journey over HTTP — the end-to-end smoke test of a RUNNING deployment (laptop or beta VM).

    python3 -m product.journey --base http://localhost:8765 --customer-invite <url> --operator-invite <url> \
        [--other-invite <url>] [--media video|image] [--dry]

It talks to the server exactly as a browser does (cookies, CSRF tokens read from the pages, multipart uploads) and
never touches the database: invitation → account → brief + product photo + logo → clarification (delegated) →
direction and quote → budget approval → production by the worker → operator release → preview of the real file →
a targeted text change → re-release → acceptance → download, whose bytes must equal the accepted version.
With --other-invite, a second customer must be unable to see the job or its files.

--dry: the deployment runs simulated providers/reasoning, so nothing in the cut was looked at by a reviewer; the
operator step then waives each NOT_VERIFIED check with the reason "DRY RUN" and records a dry listen. A check that was
measured and FAILED stops the journey even in --dry. Never use --dry against live mode.
Passwords are generated per run and never printed.
"""
from __future__ import annotations

import argparse
import hashlib
import http.cookiejar
import json
import re
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

WAITING = {"understanding", "directing", "planning", "producing", "checking", "revising", "submitted", "paused_provider"}


class Client:
    def __init__(self, base: str):
        self.base = base.rstrip("/")
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar), _NoRedirect())

    def req(self, method, path, data=None, headers=None, follow=True):
        url = path if path.startswith("http") else self.base + path
        r = urllib.request.Request(url, data=data, method=method, headers=headers or {})
        try:
            resp = self.op.open(r, timeout=120)
            code, body, hdrs = resp.status, resp.read(), resp.headers
        except urllib.error.HTTPError as e:
            code, body, hdrs = e.code, e.read(), e.headers
        if follow and code in (302, 303) and hdrs.get("Location"):
            return self.req("GET", hdrs["Location"])
        self.last_url = url
        return code, body, hdrs

    def get(self, path):
        return self.req("GET", path)

    def csrf(self, path) -> str:
        code, body, _ = self.get(path)
        m = re.search(rb'name="csrf" value="([0-9a-f]+)"', body)
        if code != 200 or not m:
            raise AssertionError(f"GET {path}: {code}, no CSRF token")
        return m.group(1).decode()

    def post(self, path, fields: dict, files: list = (), csrf_from: str | None = None):
        if csrf_from:
            fields = {**fields, "csrf": self.csrf(csrf_from)}
        if files:
            b = uuid.uuid4().hex
            parts = []
            for k, v in _items(fields):
                parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
            for field, name, ctype, data in files:
                parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{field}"; filename="{name}"\r\n'
                             f"Content-Type: {ctype}\r\n\r\n".encode() + data + b"\r\n")
            body = b"".join(parts) + f"--{b}--\r\n".encode()
            return self.req("POST", path, body, {"Content-Type": f"multipart/form-data; boundary={b}"})
        return self.req("POST", path, urllib.parse.urlencode(list(_items(fields))).encode(),
                        {"Content-Type": "application/x-www-form-urlencoded"})


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def _items(d):
    for k, v in d.items():
        for x in (v if isinstance(v, list) else [v]):
            yield k, x


def step(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def signup(c: Client, invite_url: str, email: str, name: str):
    pw = secrets.token_urlsafe(18)
    path = urllib.parse.urlparse(invite_url).path
    code, _, _ = c.post(path, {"name": name, "password": pw})
    code, body, _ = c.post("/login", {"email": email, "password": pw, "next": "/"})
    if b"not recognised" in body or code >= 400:
        raise AssertionError(f"login failed for {email}: {code}")


def state(c: Client, jid) -> str:
    code, body, _ = c.get(f"/jobs/{jid}/status")
    if code != 200:
        raise AssertionError(f"status {code}")
    return json.loads(body)["state"]


def wait(c: Client, jid, until: set, timeout_s: float, log: dict) -> str:
    t0 = time.time()
    last = None
    while time.time() - t0 < timeout_s:
        s = state(c, jid)
        if s != last:
            step(f"  state: {s}")
            log.setdefault("states", []).append((round(time.time() - log["t0"], 1), s))
            last = s
        if s in until:
            return s
        if s not in WAITING and s not in until:
            raise AssertionError(f"job reached {s}, expected one of {sorted(until)}")
        time.sleep(2)
    raise AssertionError(f"timed out after {timeout_s}s in {last}")


def operator_release(op: Client, jid, dry: bool):
    code, body, _ = op.get(f"/ops/jobs/{jid}")
    assert code == 200, code
    pending = re.findall(rb'action="/ops/jobs/\w+/(waive|attest)"><input type="hidden" name="csrf" value="[0-9a-f]+">'
                         rb'<input type="hidden" name="asset_id" value="(ast_\w+)"><input type="hidden" name="check_id" value="([^"]+)"', body)
    failed = re.findall(rb'<tr><td>([^<]+)</td><td class="FAIL">FAIL</td>', body)
    if failed:
        raise AssertionError(f"measured failures on the cut — never waived, not even in a dry run: {sorted(set(f.decode() for f in failed))}")
    if pending and not dry:
        raise AssertionError(f"{len(pending)} checks need a person (listen / look); this journey performs them only in --dry")
    for kind, aid, cid in pending:
        if kind == b"attest":
            op.post(f"/ops/jobs/{jid}/attest", {"asset_id": aid.decode(), "check_id": cid.decode(), "outcome": "PASS",
                                               "note": "DRY RUN — simulated film: test tone and pink noise, no speech or singing"},
                    csrf_from=f"/ops/jobs/{jid}")
            continue
        op.post(f"/ops/jobs/{jid}/waive", {"asset_id": aid.decode(), "check_id": cid.decode(),
                                          "reason": "DRY RUN — simulated media; nothing was verified by a reviewer"},
                csrf_from=f"/ops/jobs/{jid}")
    step(f"  operator recorded {sum(1 for k, *_ in pending if k == b'attest')} listen(s), waived "
         f"{sum(1 for k, *_ in pending if k == b'waive')} unverifiable dry checks, and releases the cut")
    op.post(f"/ops/jobs/{jid}/release", {}, csrf_from=f"/ops/jobs/{jid}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--customer-invite", required=True)
    ap.add_argument("--customer-email", default="buyer@acme.test")
    ap.add_argument("--operator-invite", required=True)
    ap.add_argument("--operator-email", default="ops@mi.test")
    ap.add_argument("--other-invite")
    ap.add_argument("--other-email", default="rival@other.test")
    ap.add_argument("--media", choices=("video", "image"), default="video")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--timeout", type=float, default=1800)
    a = ap.parse_args(argv)
    from runtime.loop.synthetic import make_png
    log = {"t0": time.time()}

    code, body, _ = Client(a.base).get("/healthz")
    assert code == 200 and b"ok" in body, f"healthz {code}"
    cust, op = Client(a.base), Client(a.base)
    step("customer accepts the invitation and signs in")
    signup(cust, a.customer_invite, a.customer_email, "Beta Buyer")
    step("operator accepts the invitation and signs in")
    signup(op, a.operator_invite, a.operator_email, "Operator")

    exact = ["Pack less. Go further.", "₹2,499 · acme.in"]
    fields = {"title": f"journey {a.media}", "media": a.media,
              "brief": ("A 30 second film for our Voyager 30L travel backpack that shows how much it fits. Warm, a bit funny. "
                        "End on our line. It must show the bag being zipped shut." if a.media == "video" else
                        "A launch poster for our Voyager 30L travel backpack; the bag must be the first thing you see; no people."),
              "formats": ["9:16"] if a.media == "video" else ["1:1", "4:5"], "duration_s": "30",
              "product_name": "Voyager 30L", "brand": "Acme", "category": "backpack",
              "product_description": "30 litre, navy, yellow lining", "exact_text": "\n".join(exact),
              "brand_colours": "#1f2a44", "max_budget_usd": "15", "allow_preview": "yes", "references_note": ""}
    logo = (b'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="120"><rect width="400" height="120" fill="#1f2a44"/>'
            b'<text x="20" y="80" font-size="64" fill="#fff" font-family="sans-serif">ACME</text></svg>')
    step("customer submits the brief with a product photo and a logo")
    code, body, hdrs = cust.post("/jobs", {**fields, "csrf": cust.csrf("/jobs/new")},
                                 files=[("product_photos", "bag.png", "image/png", make_png(256, 256, seed=2)),
                                        ("logo", "logo.svg", "image/svg+xml", logo)])
    m = re.search(r"/jobs/(job_\w+)", cust.last_url)
    assert m, f"no job page after submit ({code}): {re.findall(rb'<h1>[^<]*|<p>[^<]*', body)[:3]}"
    jid = m.group(1)
    step(f"job {jid}")

    s = wait(cust, jid, {"needs_answers", "awaiting_approval"}, a.timeout, log)
    if s == "needs_answers":
        _, page, _ = cust.get(f"/jobs/{jid}")
        qs = sorted(set(re.findall(rb'name="delegate_(\w+)"', page)))
        step(f"customer delegates {len(qs)} clarification questions")
        cust.post(f"/jobs/{jid}/answer", {f"delegate_{q.decode()}": "on" for q in qs}, csrf_from=f"/jobs/{jid}")
        wait(cust, jid, {"awaiting_approval"}, a.timeout, log)
    _, page, _ = cust.get(f"/jobs/{jid}")
    bud = re.search(rb'name="budget_usd" value="([\d.]+)"', page)
    step(f"customer reads the direction and approves the budget (USD {bud.group(1).decode() if bud else '?'})")
    log["approved"] = time.time()
    cust.post(f"/jobs/{jid}/approve", {"budget_usd": bud.group(1).decode() if bud else "15"}, csrf_from=f"/jobs/{jid}")

    def release_and_fetch(label):
        s = wait(cust, jid, {"operator_hold", "ready_for_review"}, a.timeout, log)
        if s == "operator_hold":
            operator_release(op, jid, a.dry)
            wait(cust, jid, {"ready_for_review"}, 120, log)
        _, page, _ = cust.get(f"/jobs/{jid}")
        aids = list(dict.fromkeys(re.findall(rb"/assets/(ast_\w+)", page)))
        got = {}
        for aid in aids:
            code, data, h = cust.get(f"/assets/{aid.decode()}")
            if code == 200 and (h.get("Content-Type", "").startswith(("video/", "image/"))):
                got[aid.decode()] = (h["Content-Type"], hashlib.sha256(data).hexdigest(), len(data))
        want = "video/mp4" if a.media == "video" else "image/png"
        finals = {k: v for k, v in got.items() if v[0] == want and v[2] > 50_000}
        assert finals, f"{label}: no playable {want} preview on the customer page ({got})"
        step(f"  {label}: customer previews {len(finals)} real file(s): " + ", ".join(f"{v[0]} {v[2] // 1024} KB" for v in finals.values()))
        return finals

    first = release_and_fetch("first cut")
    log["first_cut_s"] = round(time.time() - log["approved"], 1)

    if a.other_invite:
        other = Client(a.base)
        signup(other, a.other_invite, a.other_email, "Rival")
        c1, _, _ = other.get(f"/jobs/{jid}")
        c2, _, _ = other.get(f"/assets/{next(iter(first))}")
        assert c1 in (403, 404) and c2 in (403, 404), f"cross-account access: job {c1}, asset {c2}"
        step(f"another account is refused the job ({c1}) and its file ({c2})")

    step('customer requests a targeted change: text to "Pack light. Go further."')
    cust.post(f"/jobs/{jid}/changes", {"change_1": 'Change the headline text to "Pack light. Go further."', "target_1": ""},
              csrf_from=f"/jobs/{jid}")
    second = release_and_fetch("revised cut")
    assert set(second) != set(first) or any(second[k][1] != first.get(k, (0, ""))[1] for k in second), "the revision produced no new file"

    step("customer accepts and downloads")
    cust.post(f"/jobs/{jid}/accept", {}, csrf_from=f"/jobs/{jid}")
    assert state(cust, jid) == "accepted"
    _, page, _ = cust.get(f"/jobs/{jid}")
    dls = list(dict.fromkeys(re.findall(rb"/assets/(ast_\w+)/download", page)))
    assert dls, "no download link after acceptance"
    for aid in dls:
        code, data, h = cust.get(f"/assets/{aid.decode()}/download")
        assert code == 200, code
        sha = hashlib.sha256(data).hexdigest()
        assert aid.decode() in second and second[aid.decode()][1] == sha, "the download is not the accepted version"
        step(f"  downloaded {aid.decode()} ({len(data) // 1024} KB), sha256 matches the accepted version")
    log["total_s"] = round(time.time() - log["t0"], 1)
    print(json.dumps({"job": jid, "result": "PASS", "first_cut_after_approval_s": log["first_cut_s"], "total_s": log["total_s"],
                      "states": log["states"]}, indent=1))


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
