#!/usr/bin/env python3
"""HTTP-range-backed seekable file, so Python's zipfile can read a REMOTE zip
without downloading it.

Why this exists (RES-002 Work Package B): some valuable public datasets ship as one
very large archive. Downloading 13 GB to keep 1 GB wastes bandwidth and risks the
disk floor. A zip stores its index (the "central directory") at the END of the file,
so with HTTP range requests we can:

  1. fetch the last ~1 MB  -> read the index -> learn every member's name/offset/size
  2. fetch only the byte ranges of the members we actually want
  3. decompress those locally

Total transfer = index + selected members. The full archive never exists on disk.

Requires the host to answer with HTTP 206 (Partial Content). Verify before relying on it:
a server that ignores Range returns 200 and the whole body, which would defeat the point.
"""
import io, os, subprocess, sys


class HTTPRangeFile(io.RawIOBase):
    def __init__(self, url, size=None, chunk=1 << 20):
        self.url = url
        self._pos = 0
        self._chunk = chunk
        self.bytes_fetched = 0
        self.requests = 0
        self.size = size if size is not None else self._remote_size()

    def _curl(self, args):
        r = subprocess.run(args, capture_output=True)
        if r.returncode != 0:
            raise IOError(f"curl failed: {r.stderr.decode()[:200]}")
        return r.stdout

    def _remote_size(self):
        out = self._curl(["curl", "-sS", "-I", "-L", "--max-time", "60", self.url]).decode(errors="replace")
        n = None
        for line in out.replace("\r", "").split("\n"):
            if line.lower().startswith("content-length:"):
                n = int(line.split(":", 1)[1].strip())
        if n is None:
            raise IOError("no content-length from remote")
        return n

    # --- io plumbing ---
    def readable(self):  return True
    def seekable(self):  return True
    def tell(self):      return self._pos

    def seek(self, off, whence=0):
        self._pos = off if whence == 0 else self._pos + off if whence == 1 else self.size + off
        return self._pos

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self._pos
        if n == 0 or self._pos >= self.size:
            return b""
        end = min(self._pos + n, self.size) - 1
        data = self._curl(["curl", "-sS", "-L", "--max-time", "600", "--retry", "3",
                           "-r", f"{self._pos}-{end}", self.url])
        self.requests += 1
        self.bytes_fetched += len(data)
        self._pos += len(data)
        return data

    def readinto(self, b):
        d = self.read(len(b))
        b[:len(d)] = d
        return len(d)


def supports_range(url):
    """Return True only if the server actually honours Range with a 206."""
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "-o", os.devnull,
                        "-w", "%{http_code}", "-r", "0-99", url], capture_output=True)
    return r.stdout.decode().strip() == "206"


if __name__ == "__main__":
    u = sys.argv[1]
    print(f"range supported: {supports_range(u)}")
    f = HTTPRangeFile(u)
    print(f"remote size    : {f.size:,} bytes")
