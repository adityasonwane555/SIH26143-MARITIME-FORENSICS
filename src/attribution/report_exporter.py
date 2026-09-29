"""
Forensic Report Exporter.
Generates comprehensive, court- and board-defensible investigation reports
in Markdown, printable HTML, and JSON formats in compliance with Section 76.
"""

from typing import Dict, Any, Optional
import json
from datetime import datetime, timezone
from src.config.schemas import ForensicDossier


class ForensicReportExporter:
    """Exports ForensicDossier into standard archival and presentation formats."""

    @staticmethod
    def to_markdown(dossier: ForensicDossier) -> str:
        """Formats the entire investigation dossier as structured Markdown."""
        now_utc = datetime.now(timezone.utc).isoformat()

        lines = [
            "# MARITIME FORENSIC INTELLIGENCE DOSSIER",
            f"**Case Reference:** `{dossier.incident_id}` | **Title:** {dossier.title}",
            f"**Generated At:** {now_utc} | **Engine:** SIH26143 v1.0.0",
            f"**Forensic Posture:** Investigation Support & Attribution Analysis (Defensible Proof Standards)",
            "",
            "---",
            "",
            "## 1. Executive Summary & Legal/Operational Posture",
            f"- **Attribution Status:** `{dossier.decision.value}`",
            f"- **Leading Hypothesis:** `{dossier.leading_hypothesis_id or 'None'}` ({dossier.leading_subject_name or 'Unattributed'})",
            f"- **Attribution Confidence:** {dossier.attribution_confidence * 100:.1f}%",
            f"- **Information Entropy:** {dossier.entropy_bits:.3f} bits",
            f"- **Abstention Invoked:** `{'YES' if dossier.is_abstention else 'NO'}`",
        ]

        if dossier.abstention_reason:
            lines.append(f"- **Abstention Rationale:** {dossier.abstention_reason}")

        # Summary Narrative
        narrative = dossier.audit_trail.get("summary_narrative", "Forensic analysis completed.")
        lines.extend([
            f"- **Forensic Assessment Narrative:**",
            f"  > {narrative}",
            "",
            "---",
            ""
        ])

        # 2. Satellite Observation & Spill Geometry
        if dossier.detected_slick:
            lines.extend([
                "## 2. Satellite Observation & Spill Geometry",
                f"- **Spill Polygon ID:** `{dossier.detected_slick.spill_id}`",
                f"- **Surface Area:** {dossier.detected_slick.area_km2:.2f} km²",
                f"- **Perimeter:** {dossier.detected_slick.perimeter_km:.2f} km",
                f"- **Centroid:** ({dossier.detected_slick.centroid.latitude:.5f}°N, {dossier.detected_slick.centroid.longitude:.5f}°E)",
                f"- **Major Axis Orientation:** {dossier.detected_slick.orientation_deg:.1f}°",
                f"- **Elongation Ratio:** {dossier.detected_slick.elongation:.2f}",
                f"- **SAR Detection Confidence:** {dossier.detected_slick.confidence * 100:.1f}%",
                "",
                "---",
                ""
            ])

        # 3. Origin Reconstruction
        if dossier.origin_estimate:
            w0 = dossier.origin_estimate.estimated_release_window[0].isoformat()
            w1 = dossier.origin_estimate.estimated_release_window[1].isoformat()
            lines.extend([
                "## 3. Metocean Conditions & Lagrangian Hindcast",
                f"- **Estimated Release Window:** `{w0}` to `{w1}`",
                f"- **Peak Inferred Origin Point:** ({dossier.origin_estimate.estimated_centroid.latitude:.5f}°N, {dossier.origin_estimate.estimated_centroid.longitude:.5f}°E)",
                f"- **Probability Surface Lat Resolution:** {dossier.origin_estimate.resolution_lat:.4f}°",
                f"- **Contour Confidence Envelopes:** 50%, 80%, 95% spatial boundaries calculated",
                "",
                "---",
                ""
            ])

        # 4. Competing Hypotheses
        lines.extend([
            "## 4. Competing Hypotheses & Posterior Probabilities",
            "",
            "| Hypothesis ID | Type | Subject / Candidate | Prior | Posterior | Falsified? |",
            "|---|---|---|---|---|---|",
        ])

        for h in dossier.hypotheses:
            is_fals = "YES (Contradicted)" if h.is_falsified else "NO (Survives)"
            lines.append(f"| `{h.hypothesis_id}` | {h.type.value} | **{h.subject_name}** | {h.prior_probability:.3f} | **{h.posterior_probability:.3f}** | {is_fals} |")

        lines.extend([
            "",
            "### Evidentiary Proofs by Hypothesis",
            ""
        ])

        for h in dossier.hypotheses:
            lines.append(f"#### Hypothesis `{h.hypothesis_id}` ({h.subject_name})")
            if h.supporting_evidence:
                lines.append("**Supporting Evidence:**")
                for e in h.supporting_evidence:
                    lines.append(f"- [+] **{e.type}**: {e.explanation} (value: {e.value:.3f}, source: {e.source})")
            else:
                lines.append("- *No supporting evidence registered.*")

            if h.contradicting_evidence:
                lines.append("**Contradicting Evidence:**")
                for e in h.contradicting_evidence:
                    lines.append(f"- [-] **{e.type}**: {e.explanation} (value: {e.value:.3f}, source: {e.source})")
            else:
                lines.append("- *No contradicting evidence identified.*")
            lines.append("")

        # 5. Adversarial Falsification
        lines.extend([
            "---",
            "",
            "## 5. Adversarial Falsification Challenge Results",
            "",
            "| Candidate | Challenge Status | Contradicting Reasons |",
            "|---|---|---|",
        ])

        for h in dossier.hypotheses:
            if h.falsification:
                status = "SURVIVES" if h.falsification.survives else "FALSIFIED"
                reasons = "; ".join(h.falsification.contradicting_reasons) if h.falsification.contradicting_reasons else "All physical challenges passed"
                lines.append(f"| `{h.subject_name}` | **{status}** | {reasons} |")

        # 6. Active Sensing Recommendations
        if dossier.recommended_evidence:
            lines.extend([
                "",
                "---",
                "",
                "## 6. Active Sensing & Next-Best-Evidence Recommendations",
                ""
            ])
            for idx, r in enumerate(dossier.recommended_evidence, 1):
                lines.append(f"### {idx}. Action: `{r.action_type}` (Urgency: {r.urgency})")
                lines.append(f"- **Expected Information Gain:** **{r.expected_information_gain_bits:.3f} bits**")
                lines.append(f"- **Separates Hypotheses:** `{r.separates_hypotheses[0]}` vs `{r.separates_hypotheses[1]}`")
                lines.append(f"- **Operational Rationale:** {r.rationale}")
                lines.append(f"- **Target Sector:** [{r.target_sector.min_lat:.3f}°N, {r.target_sector.min_lon:.3f}°E] to [{r.target_sector.max_lat:.3f}°N, {r.target_sector.max_lon:.3f}°E]")
                lines.append("")

        # 7. Audit Trail & Provenance
        lines.extend([
            "---",
            "",
            "## 7. Provenance & Audit Trail",
            f"- **Pipeline Stage:** `{dossier.audit_trail.get('pipeline_stage', 'complete')}`",
            f"- **Execution Timestamp:** `{dossier.audit_trail.get('execution_timestamp', now_utc)}`",
            f"- **Data Hash:** `{dossier.audit_trail.get('provenance_hash', 'N/A')}`",
            "- **Governing Standard:** SIH26143 / NTRO Master Build Specification. Outputs are probabilistic decision support.",
            ""
        ])

        return "\n".join(lines)

    @staticmethod
    def to_html(dossier: ForensicDossier) -> str:
        """Formats the entire investigation dossier as standalone printable HTML."""
        status_color = "#10b981" if dossier.decision.value == "ATTRIBUTED_TO_HYPOTHESIS" else "#f59e0b"
        now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

        rows_hypo = ""
        for h in dossier.hypotheses:
            is_fals = "<span style='color:#ef4444;font-weight:700;'>FAILED (Contradicted)</span>" if h.is_falsified else "<span style='color:#10b981;font-weight:700;'>ACTIVE (Survives)</span>"
            rows_hypo += f"<tr><td><code>{h.hypothesis_id}</code></td><td><strong>{h.subject_name}</strong></td><td>{h.prior_probability:.3f}</td><td><strong>{h.posterior_probability:.3f}</strong></td><td>{is_fals}</td></tr>"

        rows_recs = ""
        for r in dossier.recommended_evidence:
            rows_recs += f"<tr><td><strong>{r.action_type}</strong><br><small style='color:#64748b'>{r.rationale}</small></td><td><strong>{r.expected_information_gain_bits:.3f} bits</strong></td><td><code>{r.separates_hypotheses[0]} vs {r.separates_hypotheses[1]}</code></td><td>{r.urgency}</td></tr>"

        area_val = f"{dossier.detected_slick.area_km2:.2f} km²" if dossier.detected_slick else "N/A"
        narrative = dossier.audit_trail.get("summary_narrative", "Investigation complete.")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Maritime Forensic Dossier — {dossier.incident_id}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      background: #f8fafc;
      margin: 0;
      padding: 40px;
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
      background: #ffffff;
      padding: 48px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      border: 1px solid #e2e8f0;
    }}
    .header {{
      border-bottom: 2px solid #0f172a;
      padding-bottom: 24px;
      margin-bottom: 32px;
    }}
    .header h1 {{
      font-size: 26px;
      margin: 0 0 8px 0;
      color: #0f172a;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      margin-right: 8px;
    }}
    .badge-status {{
      background: {status_color};
      color: #ffffff;
    }}
    .badge-conf {{
      background: #0284c7;
      color: #ffffff;
    }}
    h2 {{
      font-size: 18px;
      color: #0f172a;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 8px;
      margin-top: 32px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      font-size: 14px;
    }}
    th, td {{
      padding: 10px 14px;
      border: 1px solid #cbd5e1;
      text-align: left;
    }}
    th {{
      background: #f1f5f9;
      font-weight: 600;
      color: #334155;
    }}
    .callout {{
      background: #f8fafc;
      border-left: 4px solid #0284c7;
      padding: 16px;
      border-radius: 4px;
      margin: 16px 0;
      font-style: italic;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin: 16px 0;
    }}
    .card {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 16px;
    }}
    .card-title {{
      font-size: 12px;
      text-transform: uppercase;
      color: #64748b;
      font-weight: 700;
    }}
    .card-value {{
      font-size: 20px;
      font-weight: 700;
      color: #0f172a;
      margin-top: 4px;
    }}
    @media print {{
      body {{ background: #fff; padding: 0; }}
      .container {{ box-shadow: none; border: none; padding: 0; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Maritime Forensic Intelligence Dossier</h1>
      <div style="margin-top: 12px;">
        <span class="badge badge-status">{dossier.decision.value}</span>
        <span class="badge badge-conf">CONFIDENCE: {dossier.attribution_confidence * 100:.1f}%</span>
        <span style="color: #64748b; font-size: 13px;">Case ID: <strong>{dossier.incident_id}</strong> | Generated: {now_str}</span>
      </div>
    </div>

    <div class="callout">
      <strong>Investigative Assessment:</strong> {narrative}
    </div>

    <div class="grid">
      <div class="card">
        <div class="card-title">Detected Slick Area</div>
        <div class="card-value">{area_val}</div>
      </div>
      <div class="card">
        <div class="card-title">Information Entropy</div>
        <div class="card-value">{dossier.entropy_bits:.3f} bits</div>
      </div>
      <div class="card">
        <div class="card-title">Leading Candidate</div>
        <div class="card-value">{dossier.leading_subject_name or 'Unattributed'}</div>
      </div>
      <div class="card">
        <div class="card-title">Attribution Decision</div>
        <div class="card-value">{dossier.decision.value}</div>
      </div>
    </div>

    <h2>Competing Source Hypotheses</h2>
    <table>
      <thead>
        <tr>
          <th>Hypothesis ID</th>
          <th>Subject / Candidate</th>
          <th>Prior</th>
          <th>Posterior</th>
          <th>Falsification Status</th>
        </tr>
      </thead>
      <tbody>
        {rows_hypo}
      </tbody>
    </table>

    <h2>Active Sensing Recommendations</h2>
    <table>
      <thead>
        <tr>
          <th>Recommended Action</th>
          <th>Expected Info Gain</th>
          <th>Hypothesis Separation</th>
          <th>Urgency</th>
        </tr>
      </thead>
      <tbody>
        {rows_recs}
      </tbody>
    </table>

    <h2>Provenance & Integrity Fingerprint</h2>
    <p style="font-size: 13px; color: #475569;">
      <strong>Data Hash:</strong> <code>{dossier.audit_trail.get('provenance_hash', 'SHA256_ACTIVE')}</code><br>
      <strong>Governing Standard:</strong> Smart India Hackathon 2026 (SIH26143 / NTRO). System outputs are mathematically objective Bayesian posterior estimates and adversarial challenges, strictly not legal adjudications.
    </p>
  </div>
</body>
</html>"""
        return html

    @staticmethod
    def to_json(dossier: ForensicDossier) -> str:
        """Serializes the entire investigation dossier to standard JSON."""
        return dossier.model_dump_json(indent=2)
