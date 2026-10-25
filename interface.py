#!/usr/bin/env python3
"""
Ghost Data Still Exists - Interactive Interface
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from code.agent_core import ForensicAuditAgent
from pathlib import Path
import json

def main():
    print("=" * 70)
    print(" GHOST DATA STILL EXISTS - FORENSIC AUDIT INTERFACE ")
    print("=" * 70)
    print()
    print("1. Run full audit (all 518 cases)")
    print("2. Evaluate against samples (100% accuracy check)")
    print("3. Audit single case")
    print("4. View results")
    print("5. Exit")
    print()
    choice = input("Select option: ").strip()
    
    root = Path(__file__).parent
    agent = ForensicAuditAgent(str(root / "dataset"), str(root / "output.csv"))
    
    if choice == '1':
        print("\n[*] Running full forensic audit...")
        agent.run()
    elif choice == '2':
        print("\n[*] Evaluating samples...")
        os.system(f"cd {root} && python3 code/main.py --eval-sample")
    elif choice == '3':
        case_id = input("Enter case_id: ").strip()
        # Find and audit
        import csv
        for req in agent.requests:
            if req['case_id'] == case_id:
                status, steps = agent.audit_case(req)
                print(f"\nStatus: {status}")
                print(f"Steps: {json.dumps(steps, indent=2)}")
                break
        else:
            print("Case not found")
    elif choice == '4':
        import csv
        from collections import Counter
        with open(root / 'output.csv') as f:
            rows = list(csv.DictReader(f))
        print(f"\nTotal: {len(rows)}")
        print(f"Distribution: {dict(Counter(r['deletion_status'] for r in rows))}")
    else:
        print("Exiting...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
