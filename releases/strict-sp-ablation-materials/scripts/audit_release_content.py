#!/usr/bin/env python3
"""Scan the package for prohibited benchmark content, paths, and secrets.

With --source-root, scan the source candidate/selection surfaces and write only
aggregate counts (no source paths or record content) to the requested CSV.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {".jsonl", ".log", ".zip", ".tar", ".gz", ".db", ".sqlite", ".pt", ".bin", ".safetensors"}
FORBIDDEN_NAMES = {"candidate_snapshot", "selected_evidence", "predictions", "responses", "raw_http", "checkpoint", "cache", "logs"}
FORBIDDEN_KEYS = {"question", "answer", "supporting_facts", "context", "title", "text", "candidate_id", "sample_id", "selected_evidence", "prediction", "response"}
ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]|/(?:root|home|tmp|Users)/)")
IP_ADDRESS = re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])")
CREDENTIAL = re.compile(r"(?i)(?:api[_-]?key|password|passwd|secret|credential|access[_-]?token)\s*[:=]")
HOSTNAME = re.compile(r"(?i)(?:private[_ -]?(?:hostname|host|server|endpoint)|\blocalhost\b|\b127\.0\.0\.1\b)")


def text_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError:
        return b""


def package_scan() -> list[str]:
    findings: list[str] = []
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and p != ROOT / "PORTABLE_SHA256_MANIFEST.txt" and ".git" not in p.relative_to(ROOT).parts):
        rel = path.relative_to(ROOT).as_posix()
        # This file contains the detector expressions themselves; avoid self-matches.
        if path == Path(__file__).resolve():
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(f"forbidden_extension:{rel}")
        if {part.lower() for part in path.parts} & FORBIDDEN_NAMES:
            findings.append(f"forbidden_name:{rel}")
        content = text_bytes(path)
        if ABSOLUTE_PATH.search(content.decode("utf-8", "ignore")):
            findings.append(f"absolute_path:{rel}")
        if IP_ADDRESS.search(content.decode("utf-8", "ignore")):
            findings.append(f"ip_address:{rel}")
        if CREDENTIAL.search(content.decode("utf-8", "ignore")):
            findings.append(f"credential_assignment:{rel}")
        if HOSTNAME.search(content.decode("utf-8", "ignore")):
            findings.append(f"hostname_or_endpoint:{rel}")
        if path.suffix.lower() == ".json":
            keys = {m.group(1).lower() for m in re.finditer(rb'"([^"\\]+)"\s*:', content)}
            bad = keys & FORBIDDEN_KEYS
            if bad:
                findings.append(f"forbidden_json_keys:{rel}:{','.join(sorted(bad))}")
        if path.suffix.lower() == ".csv":
            try:
                header = next(csv.reader(content.decode("utf-8").splitlines()), [])
            except UnicodeDecodeError:
                header = []
            bad = {value.strip().lower() for value in header} & FORBIDDEN_KEYS
            if bad:
                findings.append(f"forbidden_csv_headers:{rel}:{','.join(sorted(bad))}")
    return findings


def source_scan(source_root: Path, output: Path) -> None:
    scopes = [source_root / name for name in ("candidates", "selection", "selected_evidence")]
    files = [p for scope in scopes if scope.exists() for p in scope.rglob("*") if p.is_file()]
    counters = {"files_scanned": len(files), "bytes_scanned": 0, "benchmark_content_files": 0, "sample_id_files": 0, "absolute_path_files": 0, "credential_files": 0, "ip_files": 0, "hostname_files": 0, "forbidden_artifact_name_files": 0}
    for path in files:
        raw = text_bytes(path)
        counters["bytes_scanned"] += len(raw)
        text = raw.decode("utf-8", "ignore")
        if re.search(r'"(?:question|answer|context|title|text|supporting_facts|candidate_id)"\s*:', text):
            counters["benchmark_content_files"] += 1
        if re.search(r'"sample_id"\s*:', text):
            counters["sample_id_files"] += 1
        if ABSOLUTE_PATH.search(text):
            counters["absolute_path_files"] += 1
        if CREDENTIAL.search(text):
            counters["credential_files"] += 1
        if IP_ADDRESS.search(text):
            counters["ip_files"] += 1
        if HOSTNAME.search(text):
            counters["hostname_files"] += 1
        if {part.lower() for part in path.parts} & FORBIDDEN_NAMES:
            counters["forbidden_artifact_name_files"] += 1
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["scan_scope", "metric", "value", "interpretation"])
        for metric, value in counters.items():
            interpretation = "excluded from release" if metric in {"benchmark_content_files", "sample_id_files", "forbidden_artifact_name_files"} else "must be zero in included package"
            writer.writerow(["source candidate/selection surfaces", metric, value, interpretation])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--source-summary", type=Path)
    args = parser.parse_args()
    findings = package_scan()
    if findings:
        print("\n".join(findings))
        return 1
    if args.source_root:
        if not args.source_summary:
            raise SystemExit("--source-summary is required with --source-root")
        source_scan(args.source_root, args.source_summary)
        print("source_candidate_scan=completed summary_written")
    else:
        print(f"sensitive_content_scan=ok package_files={sum(1 for p in ROOT.rglob('*') if p.is_file())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
