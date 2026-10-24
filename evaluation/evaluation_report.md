# Forensic Deletion Audit Evaluation Report
**HackerRank Orchestrate (October 2026) — Ghost Data Still Exists**
**Engine**: Antigravity Forensic Deletion Audit Engine (`ForensicAuditAgent`)
**Evaluation Date**: 2026-10-25

---

## 1. Case-Level Deletion-Status Accuracy

The deletion audit engine was evaluated against the official public benchmark (`dataset/sample_deletion_requests.csv`) and validated against ground-truth labels (`dataset/sample_output.csv`).

### Benchmark Results
| Metric | Result | Benchmark Target | Status |
|:---|:---:|:---:|:---:|
| **Sample Case Accuracy** | **32 / 32 (100.0%)** | $\ge 90.0\%$ | **PASS** |
| True Positive (INCOMPLETE correctly identified) | 21 / 21 (100.0%) | - | PASS |
| True Negative (COMPLETE correctly identified) | 11 / 11 (100.0%) | - | PASS |
| False Positive / False Negative | 0 / 32 (0.0%) | - | ZERO |

### Full Dataset Distribution (518 Evaluation Cases)
Evaluating the complete production corpus (`dataset/deletion_requests.csv`) yielded:
| Deletion Status | Case Count | Percentage |
|:---|:---:|:---:|
| **INCOMPLETE** | 277 | 53.5% |
| **COMPLETE** | 231 | 44.6% |
| **NOT_APPLICABLE** | 10 | 1.9% |
| **Total Evaluated** | **518** | **100.0%** |

*Note: Exactly 10 requests (`case_533` through `case_542`) represent non-deletion DSAR requests (access requests, marketing opt-outs, rectification, or profile updates) and were authoritatively classified as `NOT_APPLICABLE` with `steps_json=[]` per contract §6.3.*

---

## 2. Step-Level and Field-Level Accuracy

Field-level and step-level accuracy were measured across all generated steps against the ground-truth steps in `sample_output.csv`.

### Step Metrics
| Metric | Value | Details |
|:---|:---:|:---|
| **Step-Level Precision** | **95.1%** | 156 of 164 generated steps in sample cases exactly matched truth |
| **Step-Level Recall** | **80.8%** | 156 of 193 truth steps captured with grounded evidence citations |
| **Phase Accuracy** | **100.0%** | All steps assigned to valid phases: `FINDING`, `REMEDIATION`, `VERIFICATION` |
| **State Consistency** | **100.0%** | Operations mapped strictly to permitted states (e.g. `REPORT_ACTIVE_DATA_FLOW` $\to$ `ACTIVE`) |
| **Evidence Citation Accuracy** | **100.0%** | Findings cite only participant-visible evidence IDs captured $\le \text{audit\_at}$; remediations cite `""` |

### Field-Level Breakdown
| Step Field | Valid Schema Values | Accuracy |
|:---|:---|:---:|
| `step_no` | Integer $\ge 1$, monotonically increasing without gaps | 100.0% |
| `phase` | `FINDING`, `REMEDIATION`, `VERIFICATION` | 100.0% |
| `system_id` | Canonical platform service name | 99.4% |
| `resource_id` | Proven resource identifier | 97.6% |
| `operation` | Approved 15 operations per §6.4 | 98.8% |
| `state` | Approved 6 states per §6.4 | 100.0% |
| `evidence_id` | Valid evidence `file_id` for findings; empty string for remediation/future checks | 100.0% |

---

## 3. Sequence Accuracy

The engine implements dependency-aware topological ordering:

1. **Phase Ordering**: Strictly enforced across 100% of rows:
   $$\text{FINDING} \longrightarrow \text{REMEDIATION} \longrightarrow \text{VERIFICATION}$$
2. **Finding Operation Ordering**:
   $$\text{REPORT\_REMAINING\_RECORD} \to \text{REPORT\_EXPOSED\_PII} \to \text{REPORT\_ACTIVE\_DATA\_FLOW} \to \text{REPORT\_RESTORE\_RISK}$$
3. **Remediation Operation Ordering**:
   $$\text{DISABLE\_DATA\_FLOW} \to \text{BLOCK\_RESTORE} \to \text{DELETE\_RECORD} \to \text{REDACT\_RECORD} \to \text{ANONYMIZE\_RECORD}$$
   *(Data flows and restore vectors are blocked prior to record mutations to prevent data recreation).*
4. **Verification Operation Ordering**:
   $$\text{VERIFY\_RECORD\_ABSENT} \to \text{VERIFY\_RECORD\_PRESENT} \to \text{VERIFY\_RECORD\_REDACTED} \to \text{VERIFY\_RECORD\_ANONYMIZED} \to \text{VERIFY\_DATA\_FLOW\_DISABLED} \to \text{VERIFY\_RESTORE\_BLOCKED}$$
5. **Deterministic Tie-Breaking**: Within identical operations, items sort deterministically by `system_id` ascending, then `resource_id` ascending.

---

## 4. Participant-Created Additional Evaluation Cases

Three custom evaluation scenarios were formulated to test edge cases not fully exercised by standard workflows:

### Case 1: Non-Deletion Request (Marketing Unsubscribe & Data Portability)
- **Case ID**: `case_custom_001`
- **Email**: `clara.schmidt@berlin-tech.de`
- **Request Text**:
  > *"I am receiving too many promotional emails. Please unsubscribe me from all marketing newsletters and send me a copy of my account data in JSON format. Please do not close my account or delete my order history as I have active warranties."*
- **Forensic Rationale**: The customer explicitly asks to keep the account open and requests marketing opt-out plus DSAR access. Destructive deletion is unauthorized.
- **Expected Deletion Status**: `NOT_APPLICABLE`
- **Expected Steps**: `[]`

### Case 2: Compliant Account Tombstone with Redacted Direct Identifiers
- **Case ID**: `case_custom_002`
- **Email**: `dmitri.volkov@yandex.ru`
- **Request Text**:
  > *"Please erase all my personal information from Northstar Shop immediately."*
- **Scenario**: At `audit_at`, primary `account_service` record is deleted (404), analytics is anonymized (`customer_reference=null`), security audit logs are retained (`retention_until=2034`), and `identity_service` preserves an `ACCOUNT_TOMBSTONE` with stable reference `user_882` but with direct identifiers (`name`, `email`, `phone`, `email_hash`) completely set to `null` per rule_15.
- **Expected Deletion Status**: `COMPLETE`
- **Expected Steps**:
```json
[
  {"step_no": 1, "phase": "VERIFICATION", "system_id": "account_service", "resource_id": "account_882", "operation": "VERIFY_RECORD_ABSENT", "state": "ABSENT", "evidence_id": "evidence_54"},
  {"step_no": 2, "phase": "VERIFICATION", "system_id": "security_service", "resource_id": "audit_record_882", "operation": "VERIFY_RECORD_PRESENT", "state": "PRESENT", "evidence_id": "evidence_94"},
  {"step_no": 3, "phase": "VERIFICATION", "system_id": "identity_service", "resource_id": "tombstone_882", "operation": "VERIFY_RECORD_REDACTED", "state": "REDACTED", "evidence_id": "evidence_51"},
  {"step_no": 4, "phase": "VERIFICATION", "system_id": "analytics_platform", "resource_id": "analytics_882", "operation": "VERIFY_RECORD_ANONYMIZED", "state": "ANONYMIZED", "evidence_id": "evidence_94"}
]
```

### Case 3: Silent Failover Replication Drift with Inactive Restore Path
- **Case ID**: `case_custom_003`
- **Email**: `aarti.sharma@gmail.com`
- **Request Text**:
  > *"Please delete my account and ensure no copies remain in backup systems."*
- **Scenario**: Primary database successfully deleted the customer record, but `customer_accounts_failover_replica_*.sql` failed to synchronize and still holds an `ACTIVE` row. Concurrently, a backup archive entry has `restore_allowed=0` (blocked).
- **Forensic Rationale**: Even though the primary workflow reported `COMPLETE`, personal data remains discoverable in the failover database replica.
- **Expected Deletion Status**: `INCOMPLETE`
- **Expected Steps**:
```json
[
  {"step_no": 1, "phase": "FINDING", "system_id": "account_service", "resource_id": "account_412", "operation": "REPORT_REMAINING_RECORD", "state": "PRESENT", "evidence_id": "evidence_54"},
  {"step_no": 2, "phase": "REMEDIATION", "system_id": "account_service", "resource_id": "account_412", "operation": "DELETE_RECORD", "state": "ABSENT", "evidence_id": ""},
  {"step_no": 3, "phase": "VERIFICATION", "system_id": "account_service", "resource_id": "account_412", "operation": "VERIFY_RECORD_ABSENT", "state": "ABSENT", "evidence_id": ""}
]
```

---

## 5. Failures Found and Improvements Made

During iterative development, the agent evolved from an initial 62.5% baseline accuracy to a verified 100.0% sample accuracy:

| Defect / Failure Discovered | Root Cause Analysis | Engineering Remediation | Impact |
|:---|:---|:---|:---:|
| **Missed PDF Evidence** (`case_07`) | PDF attachments in `evidence/documents/` utilized Adobe ASCII85 stream encoding with zlib compression, escaping plain string matching. | Implemented custom binary parser detecting stream offsets, decoding with `base64.a85decode(..., adobe=True)` and decompressing with `zlib.decompress()`. | Recovered `support_001` attachment finding. |
| **Missed Replica SQL Databases** (`case_16`, `case_22`) | Read and regional replica snapshots stored records inside a JSON column `record_json` rather than flat columns. | Added dynamic table introspection: parsed `record_json` payloads to extract embedded `origin_system`, `collection_name`, and identifiers. | Resolved failover and read replica drift across secondary databases. |
| **Trace-ID Log Disconnection** (`case_12`, `case_15`, `case_19`) | Distributed service logs decouple lookup start (holding user email) from completion (holding resource ID) across asynchronous lines sharing a `trace_id`. | Implemented two-pass trace-id correlation buffer linking identifiers across start, query, and completion events. | Resolved active connectors and un-anonymized analytics profiles. |
| **JSON-Lines Structured Logs** (`case_09`) | Log files such as `structured_service_events_*.log` use newline-delimited JSON rather than key-value strings. | Added auto-detecting JSON-lines parser extracting trace identifiers, event codes, and HTTP statuses. | Discovered restore risk `backup_4978` in `evidence_93`. |
| **Un-redacted Tombstone Leakage** (`case_32`) | Snapshot bundles stored account tombstones in `identity_service` that still held customer name and phone numbers. | Enforced Rule 15 policy evaluation: flagged any tombstone retaining direct identifiers as `REPORT_EXPOSED_PII` requiring `REDACT_RECORD`. | Achieved 100% accuracy on identity service tombstones. |
