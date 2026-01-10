# Legitimate Intervention Framework (LIF)

An open-source research framework for onchain governance and protocol safety.

## Overview
This repository contains the data pipeline, research methodology, and manuscript for the Legitimate Intervention Framework (LIF). The project quantifies and analyzes systemic risk in decentralized finance, proposing automated "Ex Ante" (Circuit Breaker) and "Ex Post" (Governance Freeze) mechanisms.

**Key Stats (Dec 2025):**
- **759 exploits** analyzed (2014-2025)
- **$91.3 billion** in total losses
- **440 LIF-addressable** incidents (~$10.9B)

## Project Structure
```
├── data/
│   ├── raw/          # source files
│   ├── build/        # intermediate pipeline outputs
│   └── refined/      # final datasets (lif_exploits_final.csv)
├── scripts/
│   ├── core/         # data pipeline (parse, dedupe, filter)
│   └── analysis/     # lif_charts.ipynb (single source of truth)
├── methodology/      # data provenance, dictionary, chart requirements
├── visualizations/   # PNG charts 
└── manuscript/       # research paper 
```

## Quick Start

### Prerequisites
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas matplotlib seaborn nbformat nbconvert ipykernel
```

### Reproduce Data Pipeline
```bash
python3 scripts/core/parse_sources.py
python3 scripts/core/deduplicate.py
python3 scripts/core/filter_lif.py
```

### Generate Charts & Statistics
```bash
# Run the master analysis notebook
jupyter nbconvert --execute --to notebook scripts/analysis/lif_charts.ipynb
```

**Outputs:**
- `visualizations/*.png` 
- `data/refined/lif_exploits_cleaned.csv` (cleaned dataset)
- `data/refined/lif_stats.json` (rich statistics with sources)

## Data Sources
| Source | Coverage | Records |
|:-------|:---------|:--------|
| Charoenwong & Bernardi (2022) | 2011-2021 | 30 |
| De.Fi Rekt Database | 2021-2025 | ~400 |
| Rekt.news Reports | 2020-2025 | 282 |
| DeFiHackLabs | 2022-2025 | ~200 |

See `methodology/data_provenance.md` for full details.
