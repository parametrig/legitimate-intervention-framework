# Manual Update Procedure (Q4 2025+ Incidents)

This document defines the **manual addition workflow** for late-breaking incidents not yet captured by upstream aggregators. It keeps the LIF dataset reproducible and citation-ready while supporting fast inclusion of critical events.

## When to Use Manual Additions
Use this procedure only when:
- An incident is **verified and widely reported**, but not yet in the source aggregators.
- The event materially affects LIF conclusions, charts, or calibration (e.g., response speed, governance recovery).

## Required Fields
Manual incident rows **must** include:
- `date` (ISO format `YYYY-MM-DD`)
- `protocol`
- `chain`
- `loss_usd`
- `vector_category`
- `is_lif_relevant`
- `source_file` → **canonical URL** (postmortem, forum post, or official statement)

## Workflow
1. **Collect sources**
   - Identify the canonical post-mortem or official thread.
   - Prefer primary sources (foundation blog, forum proposal, incident report).

2. **Append to datasets**
   - Add the incident row to both refined files to maintain consistency:
     - `data/refined/lif_exploits_final.csv` (Pipeline intermediate)
     - `data/refined/lif_exploits_cleaned.csv` (Primary Analysis Dataset)
   - Ensure the `source_file` column is a valid URL.

3. **Update intervention metrics (if applicable)**
   - If the incident includes clear intervention timing, add to:
     - `data/refined/lif_intervention_metrics.csv`

4. **Recompute summary stats**
   - Update `data/refined/lif_stats.json` with new totals using `scripts/core/update_stats.py`.
   - Update `README.md` and `methodology/data_provenance.md` to match.

5. **Verify charts**
   - If the new event affects charts, re-run:
     - `scripts/analysis/lif_charts.ipynb`

## Mermaid Overview
```mermaid
flowchart TD
    A[New Incident Verified] --> B[Collect Canonical Source URL]
    B --> C[Append to lif_exploits_final.csv (Intermediate)]
    B --> D[Append to lif_exploits_cleaned.csv (Primary)]
    C --> E[Update lif_intervention_metrics.csv (if timing data)]
    D --> F[Recompute lif_stats.json]
    F --> G[Update README + data_provenance]
    F --> H[Re-run lif_charts.ipynb if charts affected]
```

## Checklist
- [ ] Source URL verified
- [ ] Added to both refined datasets
- [ ] `is_lif_relevant` reviewed
- [ ] `lif_stats.json` updated
- [ ] README + data_provenance updated
- [ ] Charts re-generated if needed
