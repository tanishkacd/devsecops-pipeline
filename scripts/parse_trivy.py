#!/usr/bin/env python3
"""
Parses a Trivy JSON report and appends a summary entry (counts by severity)
to history/scan-history.json, so the dashboard can chart trends over time.

Usage:
    python3 scripts/parse_trivy.py <trivy-report.json> <history/scan-history.json>
"""

import json
import os
import sys
from datetime import datetime, timezone


def count_severities(trivy_report: dict) -> dict:
    """Count vulnerabilities by severity across all result sections."""
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}

    for result in trivy_report.get("Results", []) or []:
        for vuln in result.get("Vulnerabilities", []) or []:
            severity = vuln.get("Severity", "UNKNOWN")
            if severity in counts:
                counts[severity] += 1
            else:
                counts["UNKNOWN"] += 1

    return counts


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 parse_trivy.py <trivy-report.json> <history-file.json>")
        sys.exit(1)

    trivy_report_path = sys.argv[1]
    history_path = sys.argv[2]

    with open(trivy_report_path, "r") as f:
        trivy_report = json.load(f)

    counts = count_severities(trivy_report)
    total = sum(counts.values())

    entry = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit": os.environ.get("GITHUB_SHA", "local")[:7],
        "total": total,
        **counts,
    }

    # Load existing history (or start fresh)
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        history = []

    history.append(entry)

    # Keep only the most recent 100 entries so the file doesn't grow forever
    history = history[-100:]

    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    print(f"Recorded scan: {entry}")


if __name__ == "__main__":
    main()
