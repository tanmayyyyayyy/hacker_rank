#!/usr/bin/env python3
"""
Ghost Data Still Exists — Automated Forensic Verification & Regression Test Suite
HackerRank Orchestrate October 2026

Comprehensive test runner verifying:
- Graph-based transitive identity resolution
- Multilingual deletion intent classification
- In-memory SQLite virtual execution & JSON column parsing
- PDF stream decompression with Adobe ASCII85
- Asynchronous distributed log trace stitching
- Rule 15 account tombstone compliance
- 100% sample benchmark accuracy
- output.csv schema, monotonic step ordering, and contract validation
"""

import csv
import json
import re
import sys
import time
from pathlib import Path

# Add code/ to import path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_core import ForensicAuditAgent


# Terminal ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


class ForensicTestSuite:
    def __init__(self, repo_root: Path):
        self.root = repo_root
        self.agent = ForensicAuditAgent(repo_root=self.root)
        self.passed = 0
        self.failed = 0
        self.total = 0

    def assert_test(self, name: str, condition: bool, details: str = "") -> None:
        self.total += 1
        if condition:
            self.passed += 1
            print(f"  {GREEN}✓ PASS{RESET} {BOLD}{name}{RESET}")
        else:
            self.failed += 1
            print(f"  {RED}✗ FAIL{RESET} {BOLD}{name}{RESET} — {details}")

    def test_identity_resolution(self) -> None:
        print(f"\n{CYAN}[1/8] Testing Graph-Based Identity Resolution Closure...{RESET}")
        # Test current email
        uid_priya, _ = self.agent.resolve_subject("priya.raman@gmail.com")
        self.assert_test("Current email resolves to stable user_id", uid_priya == "user_07", f"Got: {uid_priya}")

        # Test historical email from user_audit_log
        uid_nadia, idents_nadia = self.agent.resolve_subject("nadia.ionescu@yahoo.com")
        self.assert_test("Historical email resolves through audit log", uid_nadia == "user_10", f"Got: {uid_nadia}")
        self.assert_test("Historical email included in identity set", "nadia.ionescu@yahoo.com" in idents_nadia)

    def test_multilingual_intent_classification(self) -> None:
        print(f"\n{CYAN}[2/8] Testing Multilingual Intent & DSAR Classification...{RESET}")
        # Positive requests
        self.assert_test("English deletion intent recognized", self.agent.is_deletion_request("Please delete all my personal data."))
        self.assert_test("Spanish deletion intent recognized", self.agent.is_deletion_request("Por favor eliminar mi cuenta permanentemente."))
        self.assert_test("French deletion intent recognized", self.agent.is_deletion_request("Veuillez supprimer mon compte et effacer mes données."))
        self.assert_test("Japanese deletion intent recognized", self.agent.is_deletion_request("私のアカウントとデータを完全に削除してください。"))

        # Explicit non-deletion DSAR requests (must be False)
        self.assert_test("Marketing opt-out only classified as non-deletion", not self.agent.is_deletion_request("Please unsubscribe me from marketing lists only; do not close my account."))
        self.assert_test("DSAR access copy classified as non-deletion", not self.agent.is_deletion_request("Send me a copy of my order history in portable format. Leave my profile active."))
        self.assert_test("Rectification classified as non-deletion", not self.agent.is_deletion_request("My surname is misspelled. Please correct my information and keep the account."))

    def test_sqlite_virtual_execution(self) -> None:
        print(f"\n{CYAN}[3/8] Testing In-Memory SQLite Virtualization & Replica Parsing...{RESET}")
        # Check that records from databases are indexed
        db_records = [r for r in self.agent.evidence_records if r[1].startswith("evidence_") and "sql" in self.agent.manifest_by_id.get(r[1], {}).get("file_path", "")]
        self.assert_test("SQLite virtual execution extracted records", len(db_records) > 0, f"Found {len(db_records)} records")

        # Check that JSON column in read replica was parsed
        replica_recs = [r for r in self.agent.evidence_records if r[1] == "evidence_05"]
        self.assert_test("Nested JSON payloads parsed from read replica (evidence_05)", len(replica_recs) >= 3, f"Found {len(replica_recs)} records")

    def test_pdf_stream_decompression(self) -> None:
        print(f"\n{CYAN}[4/8] Testing PDF Binary Stream Decompression (Adobe ASCII85)...{RESET}")
        pdf_recs = [r for r in self.agent.evidence_records if r[1] == "evidence_58"]
        self.assert_test("PDF attachment support_001 extracted from delivery correction form", any(r[3] == "support_001" for r in pdf_recs))

    def test_distributed_trace_log_stitching(self) -> None:
        print(f"\n{CYAN}[5/8] Testing Distributed Trace-ID Asynchronous Log Stitching...{RESET}")
        # Check case_12 trace correlation: minjun.kim -> account_9797
        ev01_recs = [r for r in self.agent.evidence_records if r[1] == "evidence_01" and r[5] == "minjun.kim@gmail.com"]
        self.assert_test("Trace-ID links minjun.kim to account_9797 in service_events", any(r[3] == "account_9797" for r in ev01_recs))

    def test_tombstone_compliance_rule_15(self) -> None:
        print(f"\n{CYAN}[6/8] Testing Account Tombstone Rule 15 Compliance...{RESET}")
        tombstone_recs = [r for r in self.agent.evidence_records if r[2] == "identity_service" and "tombstone" in r[3]]
        self.assert_test("Identity service tombstones audited", len(tombstone_recs) > 0)
        # Verify case_32 tombstone_9178 is flagged for exposed PII
        t9178 = [r for r in tombstone_recs if r[3] == "tombstone_9178"]
        self.assert_test("Un-redacted tombstone flagged as REPORT_EXPOSED_PII", any(r[4] == "FINDING_EXPOSED_PII" for r in t9178))

    def test_sample_benchmark_accuracy(self) -> None:
        print(f"\n{CYAN}[7/8] Testing Reference Benchmark Accuracy (32 Sample Cases)...{RESET}")
        sample_reqs = list(csv.DictReader(open(self.root / "dataset" / "sample_deletion_requests.csv")))
        sample_truth = {r["case_id"]: r for r in csv.DictReader(open(self.root / "dataset" / "sample_output.csv"))}
        correct = 0
        for req in sample_reqs:
            cid = req["case_id"]
            st, _ = self.agent.audit_case(req)
            if st == sample_truth[cid]["deletion_status"]:
                correct += 1
        self.assert_test("100% case-level deletion-status accuracy on sample benchmark", correct == len(sample_reqs), f"Accuracy: {correct}/{len(sample_reqs)}")

    def test_output_csv_schema_and_ordering(self) -> None:
        print(f"\n{CYAN}[8/8] Testing output.csv Schema, Monotonic Ordering & Contract...{RESET}")
        output_file = self.root / "output.csv"
        self.assert_test("output.csv exists at repository root", output_file.exists())

        rows = list(csv.DictReader(open(output_file)))
        self.assert_test("output.csv contains exactly 518 evaluation rows", len(rows) == 518, f"Got: {len(rows)}")

        # Check numeric sorting
        case_nums = [int(re.search(r"\d+", r["case_id"]).group()) for r in rows]
        self.assert_test("Cases sorted strictly by numerical case_id", case_nums == sorted(case_nums))

        # Check steps and phases
        valid_phases = ["FINDING", "REMEDIATION", "VERIFICATION"]
        valid_seq = True
        valid_states = True
        empty_na = True

        for r in rows:
            cid = r["case_id"]
            st = r["deletion_status"]
            steps = json.loads(r["steps_json"])

            if st == "NOT_APPLICABLE" and steps != []:
                empty_na = False

            # Check phase ordering
            phases = [s["phase"] for s in steps]
            phase_indices = [valid_phases.index(p) for p in phases if p in valid_phases]
            if phase_indices != sorted(phase_indices):
                valid_seq = False

            # Check consecutive step numbers
            for idx, s in enumerate(steps, 1):
                if s["step_no"] != idx:
                    valid_seq = False

        self.assert_test("NOT_APPLICABLE cases have empty steps_json=[]", empty_na)
        self.assert_test("Consecutive step numbering (1, 2, 3...) with no gaps", valid_seq)
        self.assert_test("Strict topological phase order (FINDING -> REMEDIATION -> VERIFICATION)", valid_seq)

    def run_all(self) -> bool:
        start = time.time()
        print("=" * 70)
        print(f"{BOLD} GHOST DATA STILL EXISTS — AUTOMATED TEST SUITE{RESET}")
        print("=" * 70)

        self.test_identity_resolution()
        self.test_multilingual_intent_classification()
        self.test_sqlite_virtual_execution()
        self.test_pdf_stream_decompression()
        self.test_distributed_trace_log_stitching()
        self.test_tombstone_compliance_rule_15()
        self.test_sample_benchmark_accuracy()
        self.test_output_csv_schema_and_ordering()

        elapsed = time.time() - start
        print("\n" + "=" * 70)
        if self.failed == 0:
            print(f"{GREEN}{BOLD}✓ ALL {self.total} TESTS PASSED in {elapsed:.2f}s! (100% SUCCESS){RESET}")
        else:
            print(f"{RED}{BOLD}✗ {self.failed} OF {self.total} TESTS FAILED in {elapsed:.2f}s.{RESET}")
        print("=" * 70)
        return self.failed == 0


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    runner = ForensicTestSuite(repo_root)
    success = runner.run_all()
    sys.exit(0 if success else 1)
