# Legitimate Intervention Framework (LIF)

LIF is an open-source research framework for onchain governance and protocol safety. This repository contains a standardized dataset of blockchain security incidents and emergency interventions.

**Version:** 1.0  
**Last Updated:** 2026-02-13

---

## Dataset Overview

| Dataset | Records | Description |
|:--------|:--------|:------------|
| `lif_exploits_final.csv` | 705 | All exploit incidents (2014-03-01 - 2026-01-21) |
| `lif_all_interventions.csv` | 130 | Cases with intervention mechanisms |
| `lif_intervention_metrics.csv` | 52 | High-fidelity intervention data (includes proactive cases) |

---

## Website data exports

The website consumes JSON exports generated from the CSVs in `data/refined/`.

| Web export | Records | Description |
|:----------|:--------|:------------|
| `web/data/exploits.json` | 705 | JSON export of `lif_exploits_final.csv` |
| `web/data/interventions.json` | 137 | JSON export of `lif_all_interventions.csv` (130 exploit-linked) plus 7 metrics-only proactive cases from `lif_intervention_metrics.csv` |

Each record in `web/data/interventions.json` includes `is_proactive` to distinguish proactive / metrics-only cases.

---

## Financial Summary

- **Total Losses:** $78,805,538,747
- **Total Prevented:** $2,511,574,380 (from all interventions dataset)
- **Total Prevented (Metrics Subset):** $1,666,149,380
- **LIF-Relevant Cases:** 601
- **Systemic Failures:** 10 cases ($61.80B)
- **Other Non-Addressable:** 94 cases ($7.41B)

---

## Repository Structure

```
legitimate-intervention-framework/
├── data/
│   └── refined/
│       ├── lif_exploits_final.csv          # Main exploits dataset
│       ├── lif_all_interventions.csv       # Intervention cases
│       └── lif_intervention_metrics.csv    # High-fidelity metrics
├── methodology/
│   ├── data_dictionary.md                  # Field definitions
│   ├── dataset_summary.md                  # Statistics & overview
│   ├── data_provenance.md                  # Data sources
│   └── intervention_datasets.md            # Intervention methodology
└── README.md                               # This file
```

---

## Quick Start

```python
import pandas as pd

# Load exploits dataset
exploits = pd.read_csv('data/refined/lif_exploits_final.csv')

# Load interventions
interventions = pd.read_csv('data/refined/lif_all_interventions.csv')

# Load high-fidelity metrics
metrics = pd.read_csv('data/refined/lif_intervention_metrics.csv')
```

---

## Documentation

- **[Website Documentation](web/WEBSITE.md)** - Architecture, design system, chart pipeline, deployment
- **[Data Dictionary](methodology/data_dictionary.md)** - Complete field definitions
- **[Dataset Summary](methodology/dataset_summary.md)** - Statistics and overview
- **[Data Provenance](methodology/data_provenance.md)** - Sources and methodology
- **[Intervention Methodology](methodology/intervention_datasets.md)** - Intervention classification

---

## Key Features

- **Standardized Format:** Consistent incident_id format (PROTOCOL-YYYY-MM-DD)
- **High Quality:** All cases manually reviewed and validated
- **Complete Coverage:** Ecosystem classifications (EVM, Non-EVM, CeFi, etc.)
- **Intervention Data:** Timing, scope, authority, and effectiveness metrics
- **Source Attribution:** All cases linked to primary sources

---

## Related Projects

- **Research Paper**: https://github.com/e3o8o/legitimate-overrides-paper  
  Academic paper by Oghenekaro Elem & Nimrod Talmon: "Legitimate Overrides in Decentralized Protocols."
> **ArXiv**: https://arxiv.org/pdf/2602.12260

---

## License

This dataset is provided for research purposes. Please cite appropriately when using in academic work.

---

## Contact

For questions or issues, please open a GitHub issue or contact x.com/elemoghenekaro.
