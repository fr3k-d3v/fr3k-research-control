"""Atomic local checkpoint storage. Not a project source of truth.

Caller must choose an access-controlled directory; no secrets are logged.
"""
from pathlib import Path
import os
import tempfile
from checkpoint import Checkpoint, encode, decode

def save(path: str | Path, checkpoint: Checkpoint) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    data = encode(checkpoint).encode("utf-8")
    name = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".ctx64k-",
                                         delete=False) as f:
            name = f.name
            os.fchmod(f.fileno(), 0o600)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, target)
        dirfd = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(dirfd)
        finally:
            os.close(dirfd)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)

def load(path: str | Path) -> Checkpoint:
    return decode(Path(path).read_text(encoding="utf-8"))
