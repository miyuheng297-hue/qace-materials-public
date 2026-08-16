#!/usr/bin/env python3
"""Audit the candidate for benchmark text, responses, paths, and secrets."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SUFFIXES = {".md", ".csv", ".json", ".py", ".txt", ".png"}
FORBIDDEN_SUFFIXES = {".jsonl", ".log", ".zip", ".tar", ".gz", ".db", ".sqlite", ".docx", ".pdf", ".eps"}
FORBIDDEN_NAMES = {".env", "credentials", "secrets", "checkpoint", "predictions", "responses", "raw_http"}
FORBIDDEN_KEYS = {
    "question", "question_text", "answer", "gold_answer", "answer_aliases", "supporting_facts",
    "supporting_titles", "title", "paragraph", "paragraph_text", "context", "prediction", "response",
    "raw_response", "sample_id", "paragraph_id", "selected_evidence", "selected_paragraphs",
}
FORBIDDEN_HEADERS = FORBIDDEN_KEYS | {"text", "document", "sentence", "candidate_id", "record_id"}


def patterns() -> list[tuple[str, re.Pattern[str]]]:
    absolute_root = "/" + "root" + "/"
    absolute_home = "/" + "home" + "/"
    web = "h" + "ttps?://"
    ipv4 = r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])"
    secret = r"(?i)(?:api[_-]?key|password|passwd|secret|credential|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"
    benchmark_id = r"(?i)(?:[0-9]+hop__|\b[0-9a-f]{24}\b)"
    return [
        ("absolute_server_path", re.compile(re.escape(absolute_root) + "|" + re.escape(absolute_home))),
        ("network_url", re.compile(web)),
        ("ip_address", re.compile(ipv4)),
        ("credential_assignment", re.compile(secret)),
        ("benchmark_shaped_identifier", re.compile(benchmark_id)),
    ]


def audit() -> list[str]:
    findings: list[str] = []
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        rel = path.relative_to(ROOT).as_posix()
        suffix = path.suffix.lower()
        if suffix not in ALLOWED_SUFFIXES:
            findings.append(f"extension_not_allowed:{rel}")
        if suffix in FORBIDDEN_SUFFIXES:
            findings.append(f"forbidden_extension:{rel}")
        lowered_parts = {part.lower() for part in path.parts}
        if lowered_parts & FORBIDDEN_NAMES:
            findings.append(f"forbidden_name:{rel}")
        if path.name == "PORTABLE_SHA256_MANIFEST.txt":
            continue
        if suffix == ".png":
            if path.name not in {"figure1_v106_docx_submission_equivalent.png", "figure2_v106_docx_submission_equivalent.png", "figure3_v106_docx_submission_equivalent.png"} or path.parent.name != "figures":
                findings.append(f"unexpected_figure_asset:{rel}")
            continue
        content = path.read_text(encoding="utf-8")
        scan_content = content.replace('http://www.w3.org/2000/svg', 'SVG_NAMESPACE')
        for label, pattern in patterns():
            if pattern.search(scan_content):
                findings.append(f"{label}:{rel}")
        if suffix == ".json":
            key_pattern = re.compile(r'"([^"\\]+)"\s*:')
            keys = {match.group(1).lower() for match in key_pattern.finditer(content)}
            bad = keys & FORBIDDEN_KEYS
            if bad:
                findings.append(f"forbidden_json_keys:{rel}:{','.join(sorted(bad))}")
        if suffix == ".csv":
            with path.open(newline="", encoding="utf-8") as handle:
                header = next(csv.reader(handle), [])
            bad = {value.strip().lower() for value in header} & FORBIDDEN_HEADERS
            if bad:
                findings.append(f"forbidden_csv_headers:{rel}:{','.join(sorted(bad))}")
    return findings


def main() -> int:
    findings = audit()
    if findings:
        print("\n".join(findings))
        return 1
    file_count = sum(1 for path in ROOT.rglob("*") if path.is_file())
    print(f"sensitive_content_scan=ok files={file_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
