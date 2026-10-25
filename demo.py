#!/usr/bin/env python3
"""
Ghost Data Still Exists - Demo
Showcases forensic capabilities
"""
import json
from pathlib import Path

def show_sample():
    import csv
    samples = list(csv.DictReader(open('dataset/sample_output.csv')))
    print("=== Sample Cases Demo ===")
    for s in samples[:3]:
        print(f"\n{s['case_id']}: {s['deletion_status']}")
        steps = json.loads(s['steps_json'])
        for st in steps:
            print(f"  [{st['phase']}] {st['system_id']}.{st['resource_id']} → {st['operation']} ({st['evidence_id'] or 'future'})")

if __name__ == '__main__':
    show_sample()
