#!/usr/bin/env python3
"""Validate the root portable manifest without excluding nested manifests."""
from __future__ import annotations
import hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "PORTABLE_SHA256_MANIFEST.txt"
def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
def main() -> int:
    entries = {}
    for line_number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        if not line:
            raise SystemExit(f"invalid_manifest_line:{line_number}")
        parts = line.split(None, 1)
        if len(parts) != 2 or len(parts[0]) != 64:
            raise SystemExit(f"invalid_manifest_line:{line}")
        sha, rel = parts
        path = Path(rel)
        if path.is_absolute() or ".." in path.parts or "\\" in rel:
            raise SystemExit(f"non_relative_manifest_path:{rel}")
        normalized = path.as_posix()
        if normalized in entries:
            raise SystemExit(f"duplicate_manifest_path:{normalized}")
        entries[normalized] = sha
    actual_paths = {
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file() and p != MANIFEST and ".git" not in p.relative_to(ROOT).parts
    }
    if set(entries) != actual_paths:
        missing = sorted(actual_paths - set(entries)); extra = sorted(set(entries) - actual_paths)
        raise SystemExit(f"manifest_coverage_mismatch:missing={missing}:extra={extra}")
    for rel, expected in sorted(entries.items()):
        actual = digest(ROOT / rel)
        if actual != expected:
            raise SystemExit(f"manifest_hash_mismatch:{rel}:{actual}!={expected}")
    print(f"relative_manifest_check=ok files={len(entries)}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
