# System Architecture - Ghost Data Still Exists

## Overview
Enterprise-grade forensic deletion audit agent with multi-modal evidence processing, graph-based reasoning, and policy-aware remediation.

## Core Components

### 1. Multi-Modal Evidence Ingestion Layer
- **SQL Parser**: In-memory SQLite execution for snapshot analysis across primary/replica/failover
- **Binary PDF Parser**: Adobe ASCII85 + zlib decompression for embedded content
- **Log Correlator**: Distributed trace correlation across log formats
- **JSON/JSONL Parser**: Structured and semi-structured data extraction
- **Image/OCR Ready**: Framework for visual evidence analysis

### 2. Identity Resolution Engine
- **Graph Traversal**: Transitive closure over identity relationships
- **Temporal Tracking**: Historical identity changes via audit log
- **Hash Matching**: Email hash correlation
- **Multi-Identifier Fusion**: Combines emails, phones, user_ids across time

### 3. Forensic Analysis Engine
- **Evidence Grounding**: All findings cite concrete evidence IDs
- **Temporal Cutoff Enforcement**: Strict audit_at boundary
- **Replication Drift Detection**: Cross-replica comparison
- **Ghost Data Detection**: Identifies recreation vectors

### 4. Policy Engine
- **Rule Application**: Full deletion_rules.csv integration
- **Tombstone Handling**: ACCOUNT_TOMBSTONE with PII redaction
- **Retention Logic**: Preserves policy-required records
- **Anonymization/Redaction**: Correct treatment per category

### 5. Remediation & Verification
- **Dependency-Aware Ordering**: Topological sort respecting causal dependencies
- **Complete Plans**: All steps from FINDING through VERIFICATION
- **Evidence-Backed Proof**: COMPLETE cases verified with evidence
- **Future-State Steps**: INCOMPLETE cases have concrete remediation + post-verification

## Data Flow

```
Input (deletion_requests.csv) 
  → Intent Classification (Multilingual)
    → Identity Resolution (Current + Historical)
      → Evidence Discovery & Parsing
        → State Reconstruction @ audit_at
          → Policy Application
            → Finding Generation (with evidence_id)
              → Remediation Planning (ordered by dependencies)
                → Verification Generation
                  → Output (output.csv)
```

## Design Principles
- **Zero Trust**: Never trust reported_status or workflow claims
- **Evidence First**: Every conclusion backed by participant-visible evidence
- **Deterministic**: Reproducible results, consistent ordering
- **Forensically Sound**: Proper chain of reasoning
- **Policy Compliant**: Exact adherence to deletion_rules.csv
