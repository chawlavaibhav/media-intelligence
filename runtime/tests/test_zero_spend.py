"""Nothing in this lane reaches a network, a provider, or the Lab's stores.

Not a promise in a comment: the socket layer is replaced with something that explodes, and a
full brief-to-spec compile is run through it.
"""
from __future__ import annotations

import socket
import unittest
from pathlib import Path

from runtime import paths
from runtime.tests import support

FIXED = "2026-09-10T12:00:00Z"


class ExplodingSocket:
    def __init__(self, *args, **kwargs):
        raise AssertionError("the spec lane opened a socket")


class NoNetworkTest(unittest.TestCase):
    def test_a_full_compile_opens_no_socket(self):
        real_socket, real_create, real_getaddrinfo = socket.socket, socket.create_connection, socket.getaddrinfo

        def explode(*args, **kwargs):
            raise AssertionError("the spec lane touched the network")

        socket.socket = ExplodingSocket
        socket.create_connection = explode
        socket.getaddrinfo = explode
        try:
            for name in ("mustard-oil-tin", "showroom-photo-edit", "lipstick-packshot"):
                spec = support.compiler().compile(support.submit(name), compiled_utc=FIXED).spec
                self.assertTrue(spec["spec_id"])
        finally:
            socket.socket, socket.create_connection, socket.getaddrinfo = real_socket, real_create, real_getaddrinfo


class NoLabWritesTest(unittest.TestCase):
    def test_a_compile_writes_nothing_under_eval_canon_or_coordination(self):
        watched = [Path(paths.ROOT) / d for d in ("eval", "canon", "coordination")]
        before = {d: _snapshot(d) for d in watched}
        for name in ("mustard-oil-tin", "showroom-photo-edit", "lipstick-packshot"):
            support.compiler().compile(support.submit(name), compiled_utc=FIXED)
        for directory in watched:
            self.assertEqual(before[directory], _snapshot(directory), f"the lane wrote under {directory.name}/")

    def test_no_runtime_module_writes_outside_the_runtime_tree(self):
        """Every open(..., 'w') in the package is inside a store or a fixture path."""
        import re

        offenders = []
        for path in Path(paths.RUNTIME).rglob("*.py"):
            if "tests" in path.parts:
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                if re.search(r"""open\([^)]*["']w""", line) and "eval" in line:
                    offenders.append(f"{path.name}: {line.strip()}")
        self.assertEqual(offenders, [])


def _snapshot(directory: Path):
    if not directory.exists():
        return None
    return sorted((str(p.relative_to(directory)), p.stat().st_mtime_ns, p.stat().st_size)
                  for p in directory.rglob("*") if p.is_file())


if __name__ == "__main__":
    unittest.main()
