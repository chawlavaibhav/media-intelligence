#!/usr/bin/env python3
"""EVAL-037 — the read-only website tool.

Exposed IDENTICALLY in NO_CANON and FULL_CANON, for B01 and B02 only. It is not a
Canon tool and carries no Canon semantics; website access is a property of the brief,
not of the condition, so it must not differ between conditions.

  B01 -> https://rentok.com   (frozen snapshot)
  B02 -> https://getaight.ai  (frozen snapshot)
  B03-B06 -> no website tool is exposed at all

The tool serves the FROZEN page.txt bytes. There is no live browsing and no other
domain is reachable: the permitted host is fixed per trial at construction time and
any other request is refused rather than fetched.

The tested model decides whether to call it. Not calling it is a legitimate outcome
and is recorded as such.
"""
import hashlib
import pathlib

import yaml

# brief -> the ONE site that brief permits
BRIEF_SITE = {
    "B01": {"host": "rentok.com", "url": "https://rentok.com"},
    "B02": {"host": "getaight.ai", "url": "https://getaight.ai"},
}


class WebsiteAccessError(RuntimeError):
    """Raised on any attempt to reach a host this brief does not permit."""


def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


class Website:
    """Serves one brief's frozen snapshot. Constructed only for B01/B02."""

    def __init__(self, pkg_root, brief_id):
        site = BRIEF_SITE.get(brief_id)
        if site is None:
            raise WebsiteAccessError(
                f"brief {brief_id} permits no website; the tool must not be exposed")
        self.pkg = pathlib.Path(pkg_root)
        self.brief_id = brief_id
        self.host = site["host"]
        self.source_url = site["url"]
        self.dir = self.pkg / "common" / "websites" / self.host
        self.text_path = self.dir / "page.txt"
        self.html_path = self.dir / "index.html"
        meta = yaml.safe_load((self.dir / "SNAPSHOT.yaml").read_text(encoding="utf-8"))
        self.recorded = {k: v["sha256"] for k, v in meta["files"].items()}
        self.final_url = meta.get("final_url", self.source_url)

    def website_read(self, url=None):
        """Return the frozen snapshot text for this brief's permitted website.

        `url` is optional. If given it must name the permitted host; anything else is
        refused. There is no fetch path in this code — only a read of frozen bytes.
        """
        if url:
            u = str(url).strip().lower()
            if self.host not in u:
                raise WebsiteAccessError(
                    f"{url!r} is not permitted for {self.brief_id}. The only permitted "
                    f"website is {self.source_url}. No other domain is reachable and "
                    f"there is no live browsing.")
        text = self.text_path.read_text(encoding="utf-8")
        text_digest = sha256_file(self.text_path)
        html_digest = sha256_file(self.html_path)
        # Fail closed: serve nothing if the frozen bytes drifted from the sealed record.
        if (text_digest != self.recorded["page.txt"]
                or html_digest != self.recorded["index.html"]):
            raise WebsiteAccessError(
                f"snapshot digest drift for {self.host}; refusing to serve altered bytes")
        return {
            "brief_id": self.brief_id,
            "source_url": self.source_url,
            "final_url": self.final_url,
            "host": self.host,
            "snapshot": "frozen; taken once during the EVAL-037 setup task",
            "live_browsing": False,
            "snapshot_path": str(self.text_path.relative_to(self.pkg)),
            "snapshot_sha256": text_digest,            # the bytes actually returned
            "source_html_sha256": html_digest,         # the raw page they came from
            "content_chars": len(text),
            "content": text,
        }


TOOL_SCHEMA = {
    "name": "website_read",
    "description": ("Read the frozen snapshot of the one website this brief permits. "
                    "Returns the page text plus its snapshot fingerprint and source URL. "
                    "This is a frozen copy, not a live fetch, and no other website is "
                    "reachable."),
    "input_schema": {"type": "object", "properties": {
        "url": {"type": "string",
                "description": "Optional. Must be the permitted website; omit to read it."}},
        "required": []},
}

TOOL_NAME = "website_read"


def schema_for(brief_id):
    """The tool schema for a brief, or None when that brief permits no website."""
    if brief_id not in BRIEF_SITE:
        return None
    s = dict(TOOL_SCHEMA)
    s["description"] = (
        f"Read the frozen snapshot of {BRIEF_SITE[brief_id]['url']}, the only website "
        "this brief permits. Returns the page text plus its snapshot fingerprint and "
        "source URL. This is a frozen copy, not a live fetch.")
    return s


def dispatch(site, name, args):
    if name != TOOL_NAME:
        raise ValueError(f"tool {name!r} is not the website tool")
    if site is None:
        raise WebsiteAccessError("no website tool is exposed for this brief")
    return site.website_read(**(args or {}))
