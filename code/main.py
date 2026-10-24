#!/usr/bin/env python3
"""
Ghost Data Still Exists — Deletion Audit Agent CLI
HackerRank Orchestrate October 2026

Production runner that executes the multi-modal ForensicAuditAgent
over the 518 evaluation deletion requests in dataset/deletion_requests.csv
and outputs the compliant output.csv at the repository root.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

# Ensure code/ is on python path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_core import ForensicAuditAgent


def parse_case_num(case_id: str) -> int:
    """Extract numeric suffix from case identifier for natural sorting."""
    m = re.search(r"\d+", case_id)
    return int(m.group()) if m else 0


def run_audit(
    repo_root: Optional[Path] = None,
    requests_path: Optional[Path] = None,
    output_path: Optional[Path] = None,
    verbose: bool = False,
) -> None:
    """
    Execute forensic deletion audit on input requests and save output.csv.
    """
    root = repo_root or Path(__file__).resolve().parent.parent
    req_file = requests_path or (root / "dataset" / "deletion_requests.csv")
    out_file = output_path or (root / "output.csv")

    print("=" * 70)
    print(" GHOST DATA STILL EXISTS — FORENSIC DELETION AUDIT AGENT")
    print(" HackerRank Orchestrate October 2026")
    print("=" * 70)
    print(f"[*] Repository root: {root}")
    print(f"[*] Input requests:  {req_file}")
    print(f"[*] Output target:   {out_file}")

    start_time = time.time()
    agent = ForensicAuditAgent(repo_root=root)
    init_elapsed = time.time() - start_time
    print(f"[*] Engine initialized in {init_elapsed:.2f}s with {len(agent.evidence_records)} evidence facts.")

    with open(req_file, newline="", encoding="utf-8") as f:
        requests = list(csv.DictReader(f))

    print(f"[*] Auditing {len(requests)} cases...")

    results = []
    status_counts = {"COMPLETE": 0, "INCOMPLETE": 0, "NOT_APPLICABLE": 0}
    total_steps = 0

    for i, req in enumerate(requests):
        case_id = req["case_id"]
        status, steps = agent.audit_case(req)

        status_counts[status] = status_counts.get(status, 0) + 1
        total_steps += len(steps)

        steps_json = json.dumps(steps, separators=(",", ":"))
        results.append({
            "case_id": case_id,
            "deletion_status": status,
            "steps_json": steps_json,
        })

        if verbose or (i + 1) % 50 == 0 or (i + 1) == len(requests):
            print(f"    [{i+1:>3}/{len(requests)}] {case_id:<10} -> {status:<15} ({len(steps):>2} steps)")

    # Sort numerically by case_id per problem contract
    results.sort(key=lambda x: parse_case_num(x["case_id"]))

    # Write output.csv with exact required columns
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "deletion_status", "steps_json"])
        for r in results:
            writer.writerow([r["case_id"], r["deletion_status"], r["steps_json"]])

    total_elapsed = time.time() - start_time
    print("-" * 70)
    print(f"[+] Audit completed successfully in {total_elapsed:.2f}s ({total_elapsed/len(requests)*1000:.1f}ms/case)")
    print(f"[+] Status distribution: {dict(status_counts)}")
    print(f"[+] Total generated steps: {total_steps} (avg {total_steps/len(requests):.1f} steps/case)")
    print(f"[+] Output written: {out_file} ({len(results)} rows)")
    print("=" * 70)


def evaluate_sample(repo_root: Optional[Path] = None) -> None:
    """Run accuracy benchmark against the 32 reference sample cases."""
    root = repo_root or Path(__file__).resolve().parent.parent
    agent = ForensicAuditAgent(repo_root=root)

    sample_reqs = list(csv.DictReader(open(root / "dataset" / "sample_deletion_requests.csv")))
    sample_truth = {r["case_id"]: r for r in csv.DictReader(open(root / "dataset" / "sample_output.csv"))}

    correct_status = 0
    total = len(sample_reqs)
    total_truth_steps = 0
    total_pred_steps = 0
    matching_steps = 0

    print("=" * 70)
    print(" SAMPLE ACCURACY BENCHMARK (32 CASES)")
    print("=" * 70)

    for req in sample_reqs:
        cid = req["case_id"]
        status, steps = agent.audit_case(req)
        truth = sample_truth[cid]
        t_status = truth["deletion_status"]
        t_steps = json.loads(truth["steps_json"])

        is_match = (status == t_status)
        if is_match:
            correct_status += 1

        total_truth_steps += len(t_steps)
        total_pred_steps += len(steps)

        def step_tuple(s):
            return (s["phase"], s["system_id"], s["resource_id"], s["operation"], s["state"], s.get("evidence_id", ""))

        t_set = set(step_tuple(s) for s in t_steps)
        p_set = set(step_tuple(s) for s in steps)
        matching_steps += len(t_set & p_set)

        flag = "✓ PASS" if is_match else "✗ FAIL"
        print(f"  {flag} {cid:<10} Pred: {status:<15} Truth: {t_status:<15} ({len(steps):>2} steps)")

    print("-" * 70)
    print(f"Case Deletion-Status Accuracy: {correct_status}/{total} ({correct_status/total*100:.1f}%)")
    print(f"Step-Level Precision:         {matching_steps}/{total_pred_steps} ({matching_steps/total_pred_steps*100:.1f}%)")
    print(f"Step-Level Recall:            {matching_steps}/{total_truth_steps} ({matching_steps/total_truth_steps*100:.1f}%)")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(description="Forensic Deletion Audit Agent Runner")
    parser.add_argument("--eval-sample", action="store_true", help="Evaluate accuracy against 32 sample cases")
    parser.add_argument("--requests", type=Path, help="Path to deletion_requests.csv")
    parser.add_argument("--output", type=Path, help="Path to output.csv target")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print verbose step output")
    args = parser.parse_args()

    if args.eval_sample:
        evaluate_sample()
    else:
        run_audit(requests_path=args.requests, output_path=args.output, verbose=args.verbose)


if __name__ == "__main__":
    main()
