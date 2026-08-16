#!/usr/bin/env python3
"""Validate complete relative SHA-256 coverage for this package."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "PORTABLE_SHA256_MANIFEST.txt"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    entries: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or len(parts[0]) != 64:
            raise SystemExit(f"invalid_manifest_line:{line}")
        sha, rel = parts
        path = Path(rel)
        if path.is_absolute() or ".." in path.parts or rel in entries:
            raise SystemExit(f"invalid_manifest_path:{rel}")
        entries[rel] = sha
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p.name != MANIFEST.name}
    if set(entries) != actual:
        raise SystemExit(f"manifest_coverage_mismatch:missing={sorted(actual-set(entries))}:extra={sorted(set(entries)-actual)}")
    for rel, expected in sorted(entries.items()):
        actual_sha = digest(ROOT / rel)
        if actual_sha != expected:
            raise SystemExit(f"manifest_hash_mismatch:{rel}")
    print(f"relative_manifest_check=ok files={len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
