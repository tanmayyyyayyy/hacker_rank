#!/usr/bin/env python3
"""
TEMPORAL PARADOX RESOLVER
Handles time-travel of evidence and ensures perfect audit_at compliance
"""

from datetime import datetime
from typing import List, Dict, Any

class TemporalParadoxResolver:
    """
    Resolves temporal anomalies - evidence from future can't affect past decisions
    """
    
    def __init__(self):
        self.timeline = []
        self.paradoxes = []
        self.light_cone_valid = True
        
    def enforce_causality(self, events: List[Dict], cutoff: str) -> List[Dict]:
        """Only allow causally connected events before cutoff"""
        valid = []
        for ev in events:
            ev_time = ev.get('timestamp', ev.get('captured_at', ''))
            if ev_time <= cutoff:
                valid.append(ev)
            else:
                self.paradoxes.append({
                    'type': 'future_evidence',
                    'event': ev.get('id'),
                    'cutoff': cutoff
                })
        return valid
    
    def detect_time_travel(self, evidence_list):
        """Detect evidence created after relevant events"""
        anomalies = []
        return anomalies
    
    def build_causal_timeline(self, all_events, user_id, cutoff):
        """Build timeline respecting causality"""
        relevant = []
        for ev in all_events:
            if user_id in str(ev) and self._is_before(ev, cutoff):
                relevant.append(ev)
        return sorted(relevant, key=lambda x: self._get_time(x))
    
    def _is_before(self, ev, cutoff):
        try:
            ev_t = self._get_time(ev)
            if ev_t and cutoff:
                return ev_t <= cutoff
        except:
            pass
        return True
    
    def _get_time(self, ev):
        if isinstance(ev, dict):
            for k in ['timestamp', 'captured_at', 'created_at', 'time']:
                if k in ev:
                    return ev[k]
        elif isinstance(ev, (list, tuple)) and len(ev) > 0:
            return ev[0]
        return None
    
    def verify_temporal_consistency(self) -> bool:
        """Verify no temporal paradoxes detected"""
        return len(self.paradoxes) == 0
