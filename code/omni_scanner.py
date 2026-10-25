#!/usr/bin/env python3
"""
OMNI-SCANNER - Universal Evidence Scanner
Scans every byte for PII and data remnants
"""

import os
import re
from pathlib import Path

class OmniScanner:
    def __init__(self):
        self.pii_patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'\+?\d{10,15}',
            'name_indicators': r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        }
        self.scan_results = []
    
    def deep_scan(self, directory):
        """Deep scan all files recursively"""
        results = []
        for root, dirs, files in os.walk(directory):
            for fname in files:
                fpath = Path(root) / fname
                try:
                    if fpath.stat().st_size > 50_000_000:  # Skip very large
                        continue
                    content = fpath.read_text(errors='ignore')
                    results.append(self._analyze_file(str(fpath), content))
                except:
                    continue
        return results
    
    def _analyze_file(self, path, content):
        findings = []
        for ptype, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                findings.append({'type': ptype, 'count': len(matches)})
        return {'path': path, 'pii_findings': findings}
    
    def scan_for_user(self, content, identifiers):
        """Scan content for specific user identifiers"""
        found = []
        for ident in identifiers:
            if ident and len(ident) > 3 and ident.lower() in content.lower():
                found.append(ident)
        return found
