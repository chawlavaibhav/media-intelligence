import io
import re
import unittest
import uuid
from http.cookies import SimpleCookie
from urllib.parse import urlencode

from product.tests.support import FILM_BRIEF, Env
from product.web.app import App
from runtime.loop.synthetic import make_png


class Client:
    def __init__(self, app):
        self.app, self.cookie = app, None

    def req(self, method, path, form=None, files=None):
        body, ctype = b"", ""
        if files is not None:
            b = uuid.uuid4().hex
            parts = []
            for k, v in (form or {}).items():
                for vv in (v if isinstance(v, list) else [v]):
                    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{vv}\r\n'.encode())
            for field, name, data, ct in files:
                parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{field}"; filename="{name}"\r\nContent-Type: {ct}\r\n\r\n'.encode()
                             + data + b"\r\n")
            body = b"".join(parts) + f"--{b}--\r\n".encode()
            ctype = f"multipart/form-data; boundary={b}"
        elif form is not None:
            body = urlencode(form, doseq=True).encode()
            ctype = "application/x-www-form-urlencoded"
        path, _, qs = path.partition("?")
        env = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": qs, "CONTENT_LENGTH": str(len(body)),
               "CONTENT_TYPE": ctype, "wsgi.input": io.BytesIO(body), "HTTP_COOKIE": f"mi_session={self.cookie}" if self.cookie else ""}
        out = {}

        def sr(status, headers):
            out["status"], out["headers"] = status, headers
        out["body"] = b"".join(self.app(env, sr))
        for k, v in out["headers"]:
            if k == "Set-Cookie":
                c = SimpleCookie(v)
                self.cookie = c["mi_session"].value or None
        return out

    def csrf(self, path):
        m = re.search(rb'name="csrf" value="([0-9a-f]+)"', self.req("GET", path)["body"])
        return m.group(1).decode()

    def login(self, email):
        r = self.req("POST", "/login", {"email": email, "password": "correct horse battery", "next": "/"})
        assert r["status"].startswith("303"), r["status"]


class WebJourney(unittest.TestCase):
    def setUp(self):
        self.e = Env()
        self.app = App(self.e.s)
        self.c = Client(self.app)
        self.c.login("buyer@acme.test")

    def tearDown(self):
        self.e.close()

    def _create(self):
        tok = self.c.csrf("/jobs/new")
        r = self.c.req("POST", "/jobs", {"csrf": tok, "brief": FILM_BRIEF, "media": "video", "formats": ["9:16"], "duration_s": "20",
                                         "product_name": "Voyager 30L", "brand": "Acme", "category": "backpack",
                                         "exact_text": "Pack less. Go further.", "brand_colours": "#1f2a44", "max_budget_usd": "15",
                                         "allow_preview": "yes"},
                       files=[("product_photos", "bag.png", make_png(64, 64, seed=2), "image/png"),
                              ("logo", "logo.png", make_png(32, 16, seed=5), "image/png")])
        self.assertTrue(r["status"].startswith("303"), r["body"][:400])
        return dict(r["headers"])["Location"].split("/")[-1]

    def test_customer_can_submit_approve_and_see_every_stage_page(self):
        jid = self._create()
        self.assertEqual(len(self.e.store.assets(jid, source="customer")), 2)
        self.assertIn(b"Understanding your brief", self.c.req("GET", f"/jobs/{jid}")["body"])
        self.e.drain()
        page = self.c.req("GET", f"/jobs/{jid}")["body"]
        self.assertIn(b"Creative direction", page)
        self.assertIn(b"Approve direction", page)
        self.assertNotIn(b"veo", page.lower())                         # no provider internals on customer pages
        self.assertNotIn(b"nano-banana", page.lower())
        prev = re.search(rb'/assets/(ast_\w+)"', page).group(1).decode()
        self.assertTrue(self.c.req("GET", f"/assets/{prev}")["status"].startswith("200"))
        tok = self.c.csrf(f"/jobs/{jid}")
        self.c.req("POST", f"/jobs/{jid}/approve", {"csrf": tok, "budget_usd": "15"})
        self.e.drain()
        self.assertEqual(self.e.state(jid), "operator_hold")
        final = self.e.orch._final_assets(jid)[0]
        self.assertTrue(self.c.req("GET", f"/assets/{final}")["status"].startswith("404"))      # not before release
        self.e.waive_all(jid)
        self.e.orch.release_hold(jid, "operator:test")
        page = self.c.req("GET", f"/jobs/{jid}")["body"]
        self.assertIn(b"Accept and download", page)
        self.assertTrue(self.c.req("GET", f"/assets/{final}")["status"].startswith("200"))
        self.assertTrue(self.c.req("GET", f"/assets/{final}/download")["status"].startswith("404"))  # not before acceptance
        tok = self.c.csrf(f"/jobs/{jid}")
        self.c.req("POST", f"/jobs/{jid}/accept", {"csrf": tok})
        self.assertEqual(self.e.state(jid), "accepted")
        dl = self.c.req("GET", f"/assets/{final}/download")
        self.assertTrue(dl["status"].startswith("200"))
        self.assertIn("attachment", dict(dl["headers"])["Content-Disposition"])

    def test_another_account_cannot_see_the_job_or_its_files_and_posts_need_csrf(self):
        jid = self._create()
        up = self.e.store.assets(jid, source="customer")[0]["id"]
        other = self.e.store.create_account("Other Co", ceiling_usd="20")
        self.e.customer("spy@other.test", other)
        c2 = Client(self.app)
        c2.login("spy@other.test")
        self.assertTrue(c2.req("GET", f"/jobs/{jid}")["status"].startswith("404"))
        self.assertTrue(c2.req("GET", f"/assets/{up}")["status"].startswith("404"))
        tok2 = c2.csrf("/jobs/new")
        self.assertTrue(c2.req("POST", f"/jobs/{jid}/accept", {"csrf": tok2})["status"].startswith("404"))
        self.assertTrue(self.c.req("POST", f"/jobs/{jid}/accept", {"csrf": "forged"})["status"].startswith("403"))
        self.assertTrue(c2.req("GET", "/ops")["status"].startswith("404"))
        anon = Client(self.app)
        self.assertTrue(anon.req("GET", f"/jobs/{jid}")["status"].startswith("303"))

    def test_unsupported_upload_types_are_refused(self):
        tok = self.c.csrf("/jobs/new")
        r = self.c.req("POST", "/jobs", {"csrf": tok, "brief": "a poster", "media": "image", "max_budget_usd": "5", "allow_preview": "yes"},
                       files=[("product_photos", "x.png", b"MZ\x90\x00 not an image", "image/png")])
        self.assertTrue(r["status"].startswith("400"))

    def test_operator_pages_render_and_the_operator_can_waive_and_release(self):
        jid = self._create()
        self.e.drain()
        self.e.orch.approve(jid, by="buyer@acme.test", budget_usd="15")
        self.e.drain()
        self.e.operator()
        op = Client(self.app)
        op.login("founder@mi.test")
        self.assertIn(b"Presentation gateway", op.req("GET", f"/ops/jobs/{jid}")["body"])
        self.assertIn(jid.encode(), op.req("GET", "/ops")["body"])
        g = self.e.store.artifact(jid, "gateway")
        tok = op.csrf(f"/ops/jobs/{jid}")
        for r in g["results"]:
            for b in r["blocking"]:
                op.req("POST", f"/ops/jobs/{jid}/waive", {"csrf": tok, "asset_id": r["asset_id"], "check_id": b["check_id"],
                                                          "reason": "dry run — simulated media, nothing to verify"})
        op.req("POST", f"/ops/jobs/{jid}/release", {"csrf": tok})
        # the listen cannot be waived: the film is still held until a person records what they heard
        self.assertEqual(self.e.state(jid), "operator_hold")
        self.assertIn(b"This cannot be waived", op.req("GET", f"/ops/jobs/{jid}")["body"])
        for r in g["results"]:
            op.req("POST", f"/ops/jobs/{jid}/attest", {"csrf": tok, "asset_id": r["asset_id"], "check_id": "audio_heard_by_person",
                                                       "note": "dry run: test tone and pink noise, no speech", "outcome": "PASS"})
        op.req("POST", f"/ops/jobs/{jid}/release", {"csrf": tok})
        self.assertEqual(self.e.state(jid), "ready_for_review")
        self.assertTrue(self.app.jinja)  # templates compiled


if __name__ == "__main__":
    unittest.main()
