#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
import csv
from collections import Counter

def main():
    print("=" * 70)
    print(" GHOST DATA STILL EXISTS - FORENSIC AUDIT INTERFACE ")
    print("=" * 70)
    print()
    root = Path(__file__).parent
    out = root / 'output.csv'
    if out.exists():
        with open(out) as f:
            rows = list(csv.DictReader(f))
        print(f"📊 Total Cases: {len(rows)}")
        c = Counter(r['deletion_status'] for r in rows)
        print(f"✓ COMPLETE: {c.get('COMPLETE',0)}")
        print(f"⚠ INCOMPLETE: {c.get('INCOMPLETE',0)}")
        print(f"⊘ NOT_APPLICABLE: {c.get('NOT_APPLICABLE',0)}")
        print()
        print(f"📁 Output: {out}")
        print(f"📋 Log: {root}/log.txt")
    else:
        print("No output.csv found. Run: python3 code/main.py")
    print("=" * 70)

if __name__ == '__main__':
    main()
