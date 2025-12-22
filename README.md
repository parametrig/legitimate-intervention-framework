# Native Compliance Framework (NCF)

An open-source research framework for on-chain governance and protocol safety.

## Overview
This repository contains the data pipeline, research methodology, and manuscript for the Native Compliance Framework (NCF). The project focuses on quantifying and mitigating systemic risk in decentralized finance through automated "Ex Ante" (Circuit Breaker) and "Ex Post" (Governance Freeze) mechanisms.

## Project Structure
- `data/raw/`: Immutable original source files (see `methodology/data_provenance.md` for details).
- `data/build/`: Intermediate script-generated assets (`parsed_raw.csv`, `merged_master.csv`).
- `data/refined/`: Final analyzed datasets (`ncf_exploits_final.csv`).
- `scripts/core/`: Data ingestion, deduplication, and refinement scripts.
- `scripts/analysis/`: Statistical analysis and data export for visuals.
- `methodology/`: Detailed documentation on data provenance, dictionary, and case studies.
- `manuscript/`: Project whitepaper and research documentation (PDF/LyX).
- `web/`: Scrollytelling microsite.

## Reproducibility
To reproduce the analysis:
1. Ensure Python 3.x is installed.
2. Run the 3-step data pipeline:
   ```bash
   python3 scripts/core/parse_sources.py
   python3 scripts/core/deduplicate.py
   python3 scripts/core/filter_ncf.py
   ```
3. (Optional) Run analysis scripts from `scripts/analysis/` to produce statistical artifacts.

## Data Sources
- **Charoenwong & Bernardi (2022):** Academic paper covering 2011-2021.
- **De.Fi Rekt Database:** Industry data covering 2021-2025.
- **Rekt.news Investigative Reports:** 282 high-fidelity post-mortems.
- **DeFiHackLabs:** Community-curated security incidents (JSON).

See `methodology/data_provenance.md` for full details.
