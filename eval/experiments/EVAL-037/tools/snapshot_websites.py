#!/usr/bin/env python3
"""EVAL-037 — freeze the two permitted website snapshots.

Run ONCE, during the EVAL-037 setup task, on a network-enabled machine.
Execution lanes never run this. They read the frozen bytes only.

Two subcommands:

  fetch   perform the one-time network fetch and write index.html + headers.txt
  seal    offline: derive page.txt, per-site SNAPSHOT.yaml and the manifest,
          and record sha256 for every artifact. Idempotent, no network.

`seal` is deterministic: given the same index.html it always produces the same
page.txt and the same digests, so any later party can re-run it and confirm the
snapshot was not edited.
"""
import argparse
import hashlib
import html
import json
import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SITES = ROOT / "common" / "websites"

PERMITTED = [
    {"brief": "B01", "host": "rentok.com", "url": "https://rentok.com"},
    {"brief": "B02", "host": "getaight.ai", "url": "https://getaight.ai"},
]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def extract_text(raw_html):
    """Deterministic visible-text extraction. Pure function of the input bytes."""
    s = re.sub(r"(?is)<(script|style|noscript|template|svg)[^>]*>.*?</\1>", " ", raw_html)
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    s = re.sub(r"(?i)<(br|/p|/div|/li|/h[1-6]|/tr|/section)[^>]*>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace(" ", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = "\n".join(line.strip() for line in s.split("\n"))
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip() + "\n"


def cmd_fetch(args):
    for site in PERMITTED:
        d = SITES / site["host"]
        d.mkdir(parents=True, exist_ok=True)
        idx, hdr = d / "index.html", d / "headers.txt"
        if idx.exists() and not args.force:
            print(f"SKIP {site['url']} — already snapshotted (use --force to refetch)")
            continue
        meta = subprocess.run(
            ["curl", "-sSL", "-A", UA, "--max-time", "90", "-D", str(hdr),
             "-o", str(idx), "-w", "%{http_code}\t%{url_effective}\t%{size_download}\t%{content_type}",
             site["url"]],
            capture_output=True, text=True, check=True).stdout.strip()
        code, final, size, ctype = meta.split("\t")
        if code != "200":
            print(f"FAIL {site['url']} — HTTP {code}", file=sys.stderr)
            return 1
        (d / "fetch.json").write_text(json.dumps(
            {"requested_url": site["url"], "final_url": final, "http_status": int(code),
             "bytes": int(size), "content_type": ctype, "user_agent": UA,
             "fetched_by": "eval/experiments/EVAL-037/tools/snapshot_websites.py fetch"},
            indent=2) + "\n")
        print(f"OK   {site['url']} -> {idx} ({size} bytes)")
    return 0


def cmd_seal(args):
    manifest = {"experiment": "EVAL-037",
                "what_this_is": ("Frozen one-time snapshots of the only two websites any EVAL-037 "
                                 "trial may use. Execution lanes read these bytes. No live browsing "
                                 "is permitted during any experimental call."),
                "live_browsing_permitted_during_trials": False,
                "other_websites_permitted": False,
                "text_extraction": ("deterministic; regenerate with `snapshot_websites.py seal` and "
                                    "compare digests"),
                "sites": []}
    for site in PERMITTED:
        d = SITES / site["host"]
        idx = d / "index.html"
        if not idx.exists():
            print(f"MISSING {idx} — run `fetch` first", file=sys.stderr)
            return 1
        raw = idx.read_text(encoding="utf-8", errors="replace")
        (d / "page.txt").write_text(extract_text(raw), encoding="utf-8")
        fetch = json.loads((d / "fetch.json").read_text()) if (d / "fetch.json").exists() else {}
        files = {}
        for name in ("index.html", "page.txt", "headers.txt", "fetch.json"):
            if (d / name).exists():
                files[name] = {"sha256": sha256_file(d / name), "bytes": (d / name).stat().st_size}
        snap = {"experiment": "EVAL-037", "brief": site["brief"], "host": site["host"],
                "requested_url": site["url"], "final_url": fetch.get("final_url", site["url"]),
                "http_status": fetch.get("http_status"), "content_type": fetch.get("content_type"),
                "snapshot_taken": "once, during the EVAL-037 setup/freeze task",
                "immutable": True, "files": files}
        with open(d / "SNAPSHOT.yaml", "w", encoding="utf-8") as fh:
            _dump(snap, fh)
        entry = dict(snap)
        entry["path"] = str((d).relative_to(ROOT))
        manifest["sites"].append(entry)
        print(f"SEALED {site['host']}  index.html={files['index.html']['sha256']}")
    with open(SITES / "WEBSITE-SNAPSHOT-MANIFEST.yaml", "w", encoding="utf-8") as fh:
        _dump(manifest, fh)
    return 0


def _dump(obj, fh, indent=0):
    """Minimal deterministic YAML writer (no PyYAML dependency, insertion order kept)."""
    pad = "  " * indent
    for k, v in obj.items():
        if isinstance(v, dict):
            fh.write(f"{pad}{k}:\n"); _dump(v, fh, indent + 1)
        elif isinstance(v, list):
            fh.write(f"{pad}{k}:\n")
            for item in v:
                if isinstance(item, dict):
                    first = True
                    for ik, iv in item.items():
                        lead = f"{pad}  - " if first else f"{pad}    "
                        first = False
                        if isinstance(iv, dict):
                            fh.write(f"{lead}{ik}:\n"); _dump(iv, fh, indent + 3)
                        else:
                            fh.write(f"{lead}{ik}: {_scalar(iv)}\n")
                else:
                    fh.write(f"{pad}  - {_scalar(item)}\n")
        else:
            fh.write(f"{pad}{k}: {_scalar(v)}\n")


def _scalar(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if s == "" or any(c in s for c in ":#\n'\"") or s[0] in "-?&*![]{}|>%@`" or s.strip() != s:
        return "'" + s.replace("'", "''") + "'"
    return s


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch"); f.add_argument("--force", action="store_true")
    sub.add_parser("seal")
    a = ap.parse_args()
    sys.exit(cmd_fetch(a) if a.cmd == "fetch" else cmd_seal(a))
