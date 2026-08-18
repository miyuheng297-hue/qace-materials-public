#!/usr/bin/env python3
"""Scan the public package for prohibited payloads, paths, and secrets."""
from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SUFFIXES = {".md", ".csv", ".json", ".py", ".txt", ".png", ".pdf", ".cff"}
ALLOWED_EXTENSIONLESS = {".gitattributes", ".gitignore"}
FORBIDDEN_SUFFIXES = {".jsonl", ".log", ".zip", ".tar", ".gz", ".db", ".sqlite", ".docx", ".eps", ".svg"}
FORBIDDEN_NAMES = {".env", "credentials", "secrets", "checkpoint", "predictions", "responses", "raw_http", "cache", "logs"}
FORBIDDEN_KEYS = {
    "question", "question_text", "answer", "gold_answer", "answer_aliases", "supporting_facts",
    "supporting_titles", "title", "paragraph", "paragraph_text", "context", "prediction", "response",
    "raw_response", "sample_id", "paragraph_id", "selected_evidence", "selected_paragraphs",
}
FORBIDDEN_HEADERS = FORBIDDEN_KEYS | {"text", "document", "sentence", "candidate_id", "record_id"}
EXPECTED_FIGURES = {f"Fig{i}.{suffix}" for i in range(1, 5) for suffix in ("png", "pdf")}


def patterns() -> list[tuple[str, re.Pattern[str]]]:
    return [
        ("absolute_server_path", re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]|/(?:root|home|Users|etc|tmp)/)")),
        ("ip_address", re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])")),
        ("credential_value", re.compile(r"(?i)(?:api[_-]?key|password|passwd|secret|credential|access[_-]?token)\s*[:=]\s*['\"][^'\"]+")),
    ]


def audit() -> list[str]:
    findings: list[str] = []
    figure_names = {p.name for p in (ROOT / "figures").iterdir() if p.is_file()}
    missing_figures = sorted(EXPECTED_FIGURES - figure_names)
    unexpected_figures = sorted(name for name in figure_names if name.startswith("Fig") and name not in EXPECTED_FIGURES)
    findings.extend(f"missing_figure:{name}" for name in missing_figures)
    findings.extend(f"unexpected_figure:{name}" for name in unexpected_figures)
    # A release audit may be run from a checked-out Git worktree.  Repository
    # internals are not release payloads and must not be interpreted as files
    # to publish or scan for secrets.
    package_files = [
        p for p in ROOT.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(ROOT).parts
    ]
    for path in sorted(package_files):
        rel = path.relative_to(ROOT).as_posix()
        if path.name == "PORTABLE_SHA256_MANIFEST.txt":
            continue
        if path == Path(__file__).resolve():
            continue
        suffix = path.suffix.lower()
        if suffix not in ALLOWED_SUFFIXES and path.name not in ALLOWED_EXTENSIONLESS:
            findings.append(f"extension_not_allowed:{rel}")
        if suffix in FORBIDDEN_SUFFIXES:
            findings.append(f"forbidden_extension:{rel}")
        if {part.lower() for part in path.relative_to(ROOT).parts} & FORBIDDEN_NAMES:
            findings.append(f"forbidden_name:{rel}")
        if suffix in {".png", ".pdf"}:
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in patterns():
            if pattern.search(content):
                findings.append(f"{label}:{rel}")
        if suffix == ".json":
            keys = {m.group(1).lower() for m in re.finditer(r'"([^"\\]+)"\s*:', content)}
            bad = keys & FORBIDDEN_KEYS
            if bad:
                findings.append(f"forbidden_json_keys:{rel}:{','.join(sorted(bad))}")
        if suffix == ".csv":
            try:
                header = next(csv.reader(content.splitlines()), [])
            except csv.Error:
                header = []
            bad = {value.strip().lower() for value in header} & FORBIDDEN_HEADERS
            if bad:
                findings.append(f"forbidden_csv_headers:{rel}:{','.join(sorted(bad))}")
    return findings


def main() -> int:
    findings = audit()
    if findings:
        print("\n".join(findings))
        return 1
    package_file_count = sum(
        1 for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(ROOT).parts
    )
    print(f"sensitive_content_scan=ok files={package_file_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
