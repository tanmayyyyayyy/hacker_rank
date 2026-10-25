# Quick Start Guide

## 1-Minute Setup
```bash
# Install dependencies (minimal)
pip install -r requirements.txt

# Generate predictions
python3 code/main.py
```

## Verification
```bash
# Check output
head -5 output.csv
wc -l output.csv  # Should be 519 lines (header + 518 rows)

# Validate format
python3 -c "
import csv,json
for r in csv.DictReader(open('output.csv')):
    json.loads(r['steps_json'])
    assert r['deletion_status'] in ['COMPLETE','INCOMPLETE','NOT_APPLICABLE']
print('✓ All valid')
"
```

## Entry Points
- `python3 code/main.py` - Main agent (recommended)
- `python3 run_all.py` - Orchestrator with fallbacks
- `make run` - Makefile target
- `python3 solve_comprehensive.py` - Direct solver

## Troubleshooting
- Output goes to repo root as `output.csv`
- Logs written to `log.txt` (AGENTS.md compliant)
- All dataset files read from `dataset/`
