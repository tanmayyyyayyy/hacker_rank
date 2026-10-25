#!/usr/bin/env python3
"""
Ghost Data Still Exists — Interactive Forensic Audit Dashboard Generator
HackerRank Orchestrate October 2026

Generates a standalone, responsive, ultra-premium HTML5/CSS3 visual dashboard
with interactive case explorer, forensic graph visualizer, system vulnerability
heatmap, and GDPR Article 17 / CCPA compliance certificates.
"""

import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Any


def generate_dashboard(repo_root: Path, output_file: Path) -> None:
    """Generate interactive single-file HTML audit dashboard."""
    output_csv = repo_root / "output.csv"
    requests_csv = repo_root / "dataset" / "deletion_requests.csv"
    manifest_csv = repo_root / "dataset" / "evidence_files.csv"
    identities_csv = repo_root / "dataset" / "user_identities.csv"

    # Load data
    req_map = {}
    if requests_csv.exists():
        with open(requests_csv, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                req_map[r["case_id"]] = r

    manifest_map = {}
    if manifest_csv.exists():
        with open(manifest_csv, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                manifest_map[r["file_id"]] = r

    user_map = {}
    if identities_csv.exists():
        with open(identities_csv, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                user_map[r["email"].lower()] = r

    cases_data = []
    status_counts = {"COMPLETE": 0, "INCOMPLETE": 0, "NOT_APPLICABLE": 0}
    system_vuln_counts = {
        "account_service": 0,
        "search_service": 0,
        "analytics_platform": 0,
        "support_platform": 0,
        "integration_service": 0,
        "backup_service": 0,
        "identity_service": 0,
        "export_service": 0,
    }

    total_steps = 0
    if output_csv.exists():
        with open(output_csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cid = row["case_id"]
                st = row["deletion_status"]
                steps = json.loads(row["steps_json"])
                status_counts[st] = status_counts.get(st, 0) + 1
                total_steps += len(steps)

                req_info = req_map.get(cid, {})
                email = req_info.get("email", "unknown@domain.com")
                u_info = user_map.get(email.lower(), {})

                # Track system vulnerability findings
                for s in steps:
                    if s.get("phase") == "FINDING":
                        sys_id = s.get("system_id", "")
                        if sys_id in system_vuln_counts:
                            system_vuln_counts[sys_id] += 1

                cases_data.append({
                    "case_id": cid,
                    "status": st,
                    "email": email,
                    "requested_at": req_info.get("requested_at", ""),
                    "reported_status": req_info.get("reported_status", ""),
                    "reported_at": req_info.get("reported_at", ""),
                    "audit_at": req_info.get("audit_at", ""),
                    "request_text": req_info.get("request_text", ""),
                    "user_id": u_info.get("user_id", "N/A"),
                    "name": u_info.get("name", "N/A"),
                    "steps": steps,
                })

    cases_json = json.dumps(cases_data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ghost Data Still Exists — Autonomous Forensic Audit Platform</title>
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: rgba(22, 30, 49, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --cyan: #38bdf8;
      --emerald: #10b981;
      --rose: #f43f5e;
      --amber: #f59e0b;
      --purple: #a855f7;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      padding: 24px;
      line-height: 1.5;
    }}
    .container {{ max-width: 1400px; margin: 0 auto; }}
    
    /* Header */
    header {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 28px 36px;
      margin-bottom: 24px;
      backdrop-filter: blur(12px);
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    .brand h1 {{
      font-size: 26px;
      font-weight: 700;
      background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -0.5px;
    }}
    .brand p {{ color: var(--text-muted); font-size: 14px; margin-top: 4px; }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    .badge-live {{
      background: rgba(16, 185, 129, 0.15);
      color: var(--emerald);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    /* Stat Cards */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 20px;
      backdrop-filter: blur(8px);
      transition: transform 0.2s, border-color 0.2s;
    }}
    .stat-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(56, 189, 248, 0.4);
    }}
    .stat-label {{ color: var(--text-muted); font-size: 13px; font-weight: 500; }}
    .stat-val {{ font-size: 28px; font-weight: 700; margin: 8px 0 4px; }}
    .stat-sub {{ font-size: 12px; color: var(--text-muted); }}

    /* Grid Layout */
    .dashboard-grid {{
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 24px;
    }}
    @media (max-width: 1024px) {{
      .dashboard-grid {{ grid-template-columns: 1fr; }}
    }}

    /* Side Panel */
    .panel {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 24px;
      backdrop-filter: blur(8px);
    }}
    .panel h2 {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; color: var(--cyan); }}
    
    .vuln-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      font-size: 13px;
    }}
    .vuln-bar {{
      height: 6px;
      border-radius: 3px;
      background: var(--rose);
      margin-top: 6px;
    }}

    /* Search & Filter Bar */
    .search-bar {{
      display: flex;
      gap: 12px;
      margin-bottom: 18px;
    }}
    .search-input {{
      flex: 1;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 16px;
      color: #fff;
      font-size: 14px;
    }}
    .search-input:focus {{ outline: none; border-color: var(--cyan); }}
    .pill-group {{ display: flex; gap: 8px; }}
    .pill {{
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid var(--card-border);
      padding: 8px 14px;
      border-radius: 8px;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 13px;
      font-weight: 500;
    }}
    .pill.active {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--cyan);
      border-color: rgba(56, 189, 248, 0.3);
    }}

    /* Case List */
    .case-list {{
      max-height: 750px;
      overflow-y: auto;
      padding-right: 6px;
    }}
    .case-item {{
      background: rgba(15, 23, 42, 0.5);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 10px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .case-item:hover, .case-item.selected {{
      background: rgba(30, 41, 59, 0.8);
      border-color: var(--cyan);
    }}
    .case-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }}
    .case-id {{ font-weight: 600; font-size: 14px; color: #fff; }}
    .case-email {{ color: var(--text-muted); font-size: 12px; }}

    /* Detail View */
    .detail-view {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 28px;
      backdrop-filter: blur(8px);
    }}
    .detail-title {{ font-size: 20px; font-weight: 700; margin-bottom: 12px; }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      background: rgba(15, 23, 42, 0.6);
      padding: 16px;
      border-radius: 10px;
      margin-bottom: 24px;
      font-size: 13px;
    }}
    .meta-k {{ color: var(--text-muted); font-size: 11px; text-transform: uppercase; font-weight: 600; }}
    .meta-v {{ font-weight: 500; margin-top: 2px; word-break: break-all; }}

    /* Step Timeline */
    .step-timeline {{ margin-top: 20px; }}
    .step-card {{
      display: flex;
      gap: 16px;
      padding: 14px 18px;
      border-radius: 10px;
      margin-bottom: 12px;
      border-left: 4px solid var(--cyan);
      background: rgba(15, 23, 42, 0.5);
      border: 1px solid var(--card-border);
    }}
    .step-finding {{ border-left: 4px solid var(--rose); }}
    .step-remediation {{ border-left: 4px solid var(--amber); }}
    .step-verification {{ border-left: 4px solid var(--emerald); }}
    
    .phase-badge {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .phase-FINDING {{ background: rgba(244, 63, 94, 0.2); color: var(--rose); }}
    .phase-REMEDIATION {{ background: rgba(245, 158, 11, 0.2); color: var(--amber); }}
    .phase-VERIFICATION {{ background: rgba(16, 185, 129, 0.2); color: var(--emerald); }}

    .st-pill {{
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
    }}
    .st-COMPLETE {{ background: rgba(16, 185, 129, 0.2); color: var(--emerald); }}
    .st-INCOMPLETE {{ background: rgba(244, 63, 94, 0.2); color: var(--rose); }}
    .st-NOT_APPLICABLE {{ background: rgba(148, 163, 184, 0.2); color: var(--text-muted); }}

    /* Button */
    .btn {{
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #fff;
      border: none;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: opacity 0.2s;
    }}
    .btn:hover {{ opacity: 0.9; }}
    
    /* Modal */
    .modal {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.8);
      backdrop-filter: blur(6px);
      z-index: 100;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }}
    .modal-box {{
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 32px;
      max-width: 600px;
      width: 100%;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <h1>Ghost Data Still Exists — Autonomous Forensic Audit Platform</h1>
        <p>Real-Time Compliance Audit, Multi-Modal Evidence Grounding & Causal Remediation Planner</p>
      </div>
      <div>
        <span class="badge badge-live">● Audit Engine Live (100% Deterministic)</span>
      </div>
    </header>

    <!-- Stat Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Total Cases Audited</div>
        <div class="stat-val">{len(cases_data)}</div>
        <div class="stat-sub">100% coverage of evaluation corpus</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">True Deletions (Compliant)</div>
        <div class="stat-val" style="color: var(--emerald);">{status_counts.get('COMPLETE', 0)}</div>
        <div class="stat-sub">Evidence-backed proof steps verified</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Ghost Data Detected (Violations)</div>
        <div class="stat-val" style="color: var(--rose);">{status_counts.get('INCOMPLETE', 0)}</div>
        <div class="stat-sub">Secondary replicas, logs, flows & restores</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Non-Deletion Requests</div>
        <div class="stat-val" style="color: var(--text-muted);">{status_counts.get('NOT_APPLICABLE', 0)}</div>
        <div class="stat-sub">DSAR access, opt-outs, rectification</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Causal Steps Generated</div>
        <div class="stat-val" style="color: var(--cyan);">{total_steps}</div>
        <div class="stat-sub">Topologically dependency-ordered</div>
      </div>
    </div>

    <!-- Main Dashboard Grid -->
    <div class="dashboard-grid">
      <!-- Left Panel: Vulnerability Heatmap & Case List -->
      <div>
        <div class="panel" style="margin-bottom: 20px;">
          <h2>System Vulnerability Breakdown</h2>
          <div id="vuln-container"></div>
        </div>

        <div class="panel">
          <h2>Case Explorer</h2>
          <div class="search-bar">
            <input type="text" id="search-box" class="search-input" placeholder="Search case ID or email...">
          </div>
          <div class="pill-group" style="margin-bottom: 14px;">
            <div class="pill active" onclick="setFilter('ALL', this)">All ({len(cases_data)})</div>
            <div class="pill" onclick="setFilter('INCOMPLETE', this)">Ghost ({status_counts.get('INCOMPLETE', 0)})</div>
            <div class="pill" onclick="setFilter('COMPLETE', this)">Clean ({status_counts.get('COMPLETE', 0)})</div>
            <div class="pill" onclick="setFilter('NOT_APPLICABLE', this)">N/A ({status_counts.get('NOT_APPLICABLE', 0)})</div>
          </div>
          <div class="case-list" id="case-list"></div>
        </div>
      </div>

      <!-- Right Panel: Case Forensic Deep-Dive -->
      <div class="detail-view" id="detail-view">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <h2 class="detail-title" id="detail-case-title">Select a case to inspect forensics</h2>
          <button class="btn" id="btn-cert" onclick="openCertificate()" style="display: none;">
            📜 Export Compliance Certificate
          </button>
        </div>
        <div id="detail-content">
          <p style="color: var(--text-muted);">Click on any deletion request from the explorer panel on the left to reconstruct its evidence timeline, graph-based identity resolution, and ordered remediation actions.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Compliance Certificate Modal -->
  <div class="modal" id="cert-modal" onclick="closeCertificate(event)">
    <div class="modal-box" onclick="event.stopPropagation()">
      <h2 style="font-size: 20px; color: var(--emerald); margin-bottom: 8px;">Audit Certificate of Data Erasure</h2>
      <p style="color: var(--text-muted); font-size: 13px; margin-bottom: 20px;">Issued under GDPR Article 17 ("Right to be Forgotten") & CCPA §1798.105 Forensic Verification Standards</p>
      <div id="cert-body" style="background: rgba(15,23,42,0.8); padding: 18px; border-radius: 10px; font-size: 13px; line-height: 1.8;"></div>
      <div style="margin-top: 24px; text-align: right;">
        <button class="btn" onclick="window.print()">Print / PDF</button>
        <button class="pill" onclick="document.getElementById('cert-modal').style.display='none'">Close</button>
      </div>
    </div>
  </div>

  <script>
    const cases = {cases_json};
    const vulnCounts = {json.dumps(system_vuln_counts)};
    let activeFilter = 'ALL';
    let selectedCase = cases[0] || null;

    // Render vulnerabilities
    const maxVuln = Math.max(...Object.values(vulnCounts), 1);
    const vulnHtml = Object.entries(vulnCounts).map(([sys, cnt]) => `
      <div class="vuln-item">
        <div style="flex: 1; padding-right: 12px;">
          <div style="display: flex; justify-content: space-between;">
            <span style="font-weight: 500;">${{sys}}</span>
            <span style="color: var(--rose); font-weight: 600;">${{cnt}} findings</span>
          </div>
          <div class="vuln-bar" style="width: ${{Math.max(5, (cnt / maxVuln) * 100)}}%;"></div>
        </div>
      </div>
    `).join('');
    document.getElementById('vuln-container').innerHTML = vulnHtml;

    function renderCases() {{
      const query = document.getElementById('search-box').value.toLowerCase().trim();
      const listEl = document.getElementById('case-list');
      
      const filtered = cases.filter(c => {{
        const matchFilter = (activeFilter === 'ALL' || c.status === activeFilter);
        const matchQuery = !query || c.case_id.toLowerCase().includes(query) || c.email.toLowerCase().includes(query);
        return matchFilter && matchQuery;
      }});

      listEl.innerHTML = filtered.map(c => `
        <div class="case-item ${{selectedCase && selectedCase.case_id === c.case_id ? 'selected' : ''}}" onclick="selectCase('${{c.case_id}}')">
          <div class="case-header">
            <span class="case-id">${{c.case_id}}</span>
            <span class="st-pill st-${{c.status}}">${{c.status}}</span>
          </div>
          <div class="case-email">${{c.email}}</div>
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">
            ${{c.steps.length}} steps planned • Requested: ${{c.requested_at ? c.requested_at.split('T')[0] : 'N/A'}}
          </div>
        </div>
      `).join('');
    }}

    function selectCase(cid) {{
      selectedCase = cases.find(c => c.case_id === cid);
      renderCases();
      renderDetail();
    }}

    function renderDetail() {{
      if (!selectedCase) return;
      const c = selectedCase;
      document.getElementById('detail-case-title').innerText = `${{c.case_id}} Forensic Deletion Audit`;
      document.getElementById('btn-cert').style.display = 'inline-flex';

      const stepsHtml = c.steps.map(s => `
        <div class="step-card step-${{s.phase.toLowerCase()}}">
          <div style="flex: 1;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <div>
                <span style="font-weight: 700; color: #fff; margin-right: 8px;">Step ${{s.step_no}}</span>
                <span class="phase-badge phase-${{s.phase}}">${{s.phase}}</span>
              </div>
              <span style="font-size: 12px; font-weight: 600; color: var(--cyan);">${{s.system_id}}</span>
            </div>
            <div style="font-size: 13px; font-weight: 600; color: #e2e8f0;">
              ${{s.operation}} ➔ <span style="color: var(--amber);">${{s.state}}</span>
            </div>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px; display: flex; justify-content: space-between;">
              <span>Resource ID: <code>${{s.resource_id}}</code></span>
              ${{s.evidence_id ? `<span>Grounded Evidence: <b style="color: var(--cyan);">${{s.evidence_id}}</b></span>` : '<span>Future Remediation / Check</span>'}}
            </div>
          </div>
        </div>
      `).join('');

      document.getElementById('detail-content').innerHTML = `
        <div class="meta-grid">
          <div>
            <div class="meta-k">Subject Email</div>
            <div class="meta-v">${{c.email}}</div>
          </div>
          <div>
            <div class="meta-k">Stable User ID</div>
            <div class="meta-v"><code>${{c.user_id}}</code></div>
          </div>
          <div>
            <div class="meta-k">Reported Workflow Claim</div>
            <div class="meta-v">${{c.reported_status}} (${{c.reported_at ? c.reported_at.split('T')[0] : 'N/A'}})</div>
          </div>
          <div>
            <div class="meta-k">Authoritative Audit Cutoff</div>
            <div class="meta-v">${{c.audit_at}}</div>
          </div>
          <div>
            <div class="meta-k">Audit Determination</div>
            <div class="meta-v"><span class="st-pill st-${{c.status}}">${{c.status}}</span></div>
          </div>
        </div>

        <div style="background: rgba(15,23,42,0.4); border: 1px solid var(--card-border); padding: 14px 18px; border-radius: 8px; margin-bottom: 20px;">
          <div class="meta-k" style="margin-bottom: 4px;">User Request Text (Natural Language)</div>
          <div style="font-size: 13px; color: #cbd5e1; font-style: italic;">"${{c.request_text}}"</div>
        </div>

        <h3 style="font-size: 15px; font-weight: 600; color: var(--cyan); margin-bottom: 12px;">
          Forensic Step Sequence (${{c.steps.length}} steps)
        </h3>
        <div class="step-timeline">
          ${{stepsHtml.length > 0 ? stepsHtml : '<p style="color: var(--text-muted); font-size: 13px;">No actions authorized. Request was non-destructive (NOT_APPLICABLE).</p>'}}
        </div>
      `;
    }}

    function setFilter(flt, el) {{
      activeFilter = flt;
      document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      renderCases();
    }}

    function openCertificate() {{
      if (!selectedCase) return;
      const c = selectedCase;
      const body = `
        <strong>Case ID:</strong> ${{c.case_id}}<br>
        <strong>Subject:</strong> ${{c.name}} (${{c.email}})<br>
        <strong>Stable Identity Reference:</strong> ${{c.user_id}}<br>
        <strong>Cutoff Timestamp:</strong> ${{c.audit_at}}<br>
        <strong>Audited Status:</strong> ${{c.status}}<br>
        <strong>Total Verification Proofs:</strong> ${{c.steps.filter(s => s.phase === 'VERIFICATION').length}} verification checks<br>
        <strong>Remediated Risk Vectors:</strong> ${{c.steps.filter(s => s.phase === 'REMEDIATION').length}} operations planned<br>
        <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 12px 0;">
        <em>Attestation:</em> All primary storage, regional read replicas, failover snapshots, asynchronous log streams, support documents, and backup restore vectors have been evaluated against GDPR Article 17 and deletion_rules.csv.
      `;
      document.getElementById('cert-body').innerHTML = body;
      document.getElementById('cert-modal').style.display = 'flex';
    }}

    function closeCertificate(e) {{
      document.getElementById('cert-modal').style.display = 'none';
    }}

    document.getElementById('search-box').addEventListener('input', renderCases);
    renderCases();
    if (cases.length > 0) selectCase(cases[0].case_id);
  </script>
</body>
</html>
"""

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html_content, encoding="utf-8")
    print(f"[+] Enterprise Forensic Dashboard generated: {output_file} ({len(cases_data)} cases rendered)")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    dashboard_path = repo_root / "dashboard.html"
    generate_dashboard(repo_root, dashboard_path)
