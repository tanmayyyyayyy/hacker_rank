# Forensic Deletion Audit Token & Resource Usage Report
**HackerRank Orchestrate (October 2026) — Ghost Data Still Exists**
**Engine**: Antigravity Forensic Deletion Audit Engine (`ForensicAuditAgent`)
**Run Timestamp**: 2026-10-25T02:46:26+05:30

---

## 1. Executive Summary

The production deletion audit run evaluated all **518 evaluation requests** in `dataset/deletion_requests.csv` to generate the authoritative submission artifact `output.csv`.

To ensure 100% determinism, millisecond-level throughput, and elimination of non-deterministic hallucinations, the agent employs a local forensic rule-evaluation engine backed by virtual SQLite executions, binary PDF decompression, and inverted multi-index evidence graphs.

---

## 2. Model & Runtime Specifications

| Parameter | Specification |
|:---|:---|
| **Architecture** | Hybrid Deterministic Forensic Engine with Multi-Modal Evidence Indexing |
| **Model Provider** | Local Engine Runtime (with optional Gemini 2.0 / 1.5 Flash VLM fallback) |
| **Runtime Model Name** | `Antigravity Forensic Rule-Engine v2.6 (Deterministic)` |
| **Hardware Platform** | Apple Silicon (macOS Darwin 24.3.0) |
| **Programming Language** | Python 3.12 (Standard Library: sqlite3, zlib, base64, json, csv, re) |
| **External API Dependencies** | None (Zero external API calls required for final run) |

---

## 3. Model Call Counts & Token Consumption

| Category | Model Name | Call Count | Input Tokens | Output Tokens | Total Tokens | Avg Tokens / Req |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Primary Audit Engine** | `Antigravity-Forensic-v2.6` | 518 | 0 | 0 | 0 | 0.0 |
| **VLM Fallback Engine** | `Gemini-2.0-Flash` | 0 | 0 | 0 | 0 | 0.0 |
| **Total / Aggregate** | **All Models** | **518** | **0** | **0** | **0** | **0.0** |

---

## 4. Cost Analysis

Pricing based on standard Google Cloud Vertex AI / AI Studio API tiers ($0.075 / 1M input tokens, $0.30 / 1M output tokens):

| Component | Rate Tier | Unit Quantity | Incurred Cost (USD) |
|:---|:---|:---:|:---:|
| Input Tokens | $0.075 / 1,000,000 tokens | 0 tokens | $0.000000 |
| Output Tokens | $0.300 / 1,000,000 tokens | 0 tokens | $0.000000 |
| Local Compute | $0.00 / execution | 0.13 seconds | $0.000000 |
| **Total Expenditure** | - | - | **$0.000000** |
| **Average Cost per Request** | - | 518 requests | **$0.000000** |

---

## 5. Performance and Latency Benchmark

| Performance Metric | Measured Value | Target Benchmark |
|:---|:---:|:---:|
| **Total Full-Dataset Processing Time** | **0.13 seconds** | $< 300.0\text{ seconds}$ |
| **Mean Latency per Request** | **0.25 ms / request** | $< 500\text{ ms / request}$ |
| **Evidence Facts Indexed** | **1,847 discrete facts** | All participant evidence |
| **Databases Executed In-Memory** | **24 SQLite snapshot databases** | 100% of `.sql` files |
| **Log Stream Traces Correlated** | **26 distributed service logs** | 100% of `.log` files |
| **PDF Documents Decompressed** | **100% of binary streams** | Complete attachment coverage |
| **Output Integrity** | **518 valid rows, 0 nulls, 0 syntax errors** | 100% compliant |
