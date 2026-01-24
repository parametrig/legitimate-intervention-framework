# Legitimate Intervention Framework (LIF)

An open-source research framework for onchain governance and protocol safety.

## Overview
This repository contains the data pipeline, research methodology, and manuscript for the Legitimate Intervention Framework (LIF). The project quantifies and analyzes systemic risk in decentralized finance, proposing automated "Ex Ante" (Circuit Breaker) and "Ex Post" (Governance Freeze) mechanisms.

**Key Stats (Jan 2026):**
- **692 exploits** analyzed (2014-2025)
- **$61.05 billion** in total losses
- **402 LIF-addressable** incidents (~$8.78B)
- **30 intervention cases** with detailed analysis

## Project Structure
```
├── data/
│   ├── raw/          # source files
│   ├── build/        # intermediate pipeline outputs
│   └── refined/      # primary datasets
│       ├── lif_exploits_final.csv      # Main cleaned dataset (692 incidents)
│       ├── lif_exploits_raw.csv       # Source data (1903 incidents)
│       └── lif_intervention_metrics.csv # Intervention analysis (30 cases)
├── scripts/
│   ├── core/         # data pipeline (parse, dedupe, filter, update_stats)
│   └── analysis/     # lif_charts.ipynb (single source of truth)
├── methodology/      # data provenance, dictionary, chart requirements, manual update procedure
├── visualizations/   # PNG charts 
└── manuscript/       # research paper 
```

## Quick Start

### Prerequisites
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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
- `data/refined/lif_exploits_cleaned.csv` (primary cleaned dataset)
- `data/refined/lif_stats.json` (rich statistics with sources)
- `data/refined/lif_intervention_metrics.csv` (intervention effectiveness subset)

## Papers & Outputs

- **Main Paper**: [Legitimate Intervention Framework (LIF)](manuscript/gnosis_framework_response.pdf) — Response to GnosisDAO's "Framework for the Future" consultation
- **Technical Extension**: [Emergency Council Power Scope (Gnosis-specific)](manuscript/gnosis_framework_response_technical_extension.pdf) — Technical grounding for Emergency Council powers and limits

## Contributing

We welcome contributions! Areas where you can help:

- **Data pipeline**: Improve parsing, deduplication, or add new sources
- **Analysis**: Extend the charts, statistics, or cross-chain comparisons
- **Framework**: Refine the Hierarchy of Precision, legitimacy conditions, or procedural models
- **Code review**: Audit scripts, notebooks, or the Guard contract specifications

**To contribute:**
1. Fork this repository
2. Create a feature branch (`git checkout -b feature/your-contribution`)
3. Make your changes
4. Submit a pull request with clear description

---

## Data Sources
| Source | Coverage | Records |
|:-------|:---------|:--------|
| Charoenwong & Bernardi (2022) | 2011-2021 | 30 |
| De.Fi Rekt Database | 2021-2025 | ~400 |
| Rekt.news Reports | 2020-2025 | 282 |
| DeFiHackLabs | 2022-2025 | ~200 |

See `methodology/data_provenance.md` for full details.
