# LIF Dataset Summary (January 2026)

## Current Repository State

The Legitimate Intervention Framework (LIF) repository contains comprehensive data on cryptocurrency exploits and intervention responses.

### Primary Datasets

#### 1. Main Exploits Dataset
**File:** `data/refined/lif_exploits_final.csv`
- **Total Incidents:** 718 (deduplicated and manually reviewed)
- **Date Range:** 2014-03-01 to 2026-01-21
- **Total Loss:** $80.48 billion
- **LIF-Relevant:** 424 incidents ($10.21B)
- **Format:** CSV with comprehensive incident metadata

#### 2. All Interventions Dataset
**File:** `data/refined/lif_all_interventions.csv`
- **Total Cases:** 114 exploit-linked intervention cases
- **Coverage:** 2016-2026
- **Scope:** All DeFi incidents where `is_intervention = True`
- **Purpose:** Comprehensive intervention universe, statistical analysis

#### 3. Intervention Metrics Dataset
**File:** `data/refined/lif_intervention_metrics.csv`
- **Total Cases:** 30 highly curated cases
- **Scope:** Representative sample with detailed timing/response metrics
- **Coverage:** 2020-2025 (focus on recent, well-documented cases)
- **Purpose:** Framework validation, intervention effectiveness study

#### 4. Source Data
**File:** `data/refined/lif_exploits_raw.csv`
- **Raw Incidents:** 1903 (before deduplication and cleaning)
- **Purpose:** Reproducibility and pipeline transparency

### Combined Statistics

| Metric | Value |
|:-------|:------|
| Total Exploits | 718 |
| Total Loss | $80.48 Billion |
| LIF-Relevant | 424 cases ($10.21B) |
| Unique Interventions | 120 (114 DeFi + 6 proactive) |
| Loss Prevented | $2.77B (27.2% capture rate) |
| Coverage | 80.6% of at-risk capital |
| Effectiveness | 26.5% of covered risk saved |

### Data Sources

The dataset combines information from multiple authoritative sources:
1. **Charoenwong & Bernardi (2022)** — Academic research (2011-2021)
2. **De.Fi Rekt Database** — Industry database (2021-2026)
3. **Rekt News Reports** — Investigative journalism (2020-2025)
4. **DeFiHackLabs** — Technical incident database (2022-2026)
5. **Manual Research** — Intervention curation, URL enrichment (2024-2026)

### Key Statistics

| Category | Value |
|:---------|:------|
| **Top Incident** | Terra / Luna ($40B loss) |
| **Most Common Vector** | Logic Bug / Code Error (231 cases) |
| **Highest Loss Chain** | Terra ($40B) |
| **Top Authority** | Delegated Body (53 intervention cases) |
| **Fastest Response** | Signer Set (~60 min median) |
| **Slowest Response** | Governance (~61 hours median) |

### Quality Assurance

- Manual review and deduplication completed
- Source verification and URL enrichment
- Chronological sorting maintained
- Data validation and consistency checks
- Cross-reference sync between datasets
- Statistical analysis and 50 visualizations

### Usage

This dataset serves as the authoritative source for:
- LIF framework research and validation
- Intervention mechanism effectiveness analysis
- DeFi security trend analysis
- Academic research on governance interventions
- Protocol designer decision support

### Citation

When using this dataset, please cite:

```bibtex
@misc{lif_dataset_2026,
  title={Legitimate Intervention Framework (LIF) Dataset},
  author={Oghenekaro, Elem},
  year={2026},
  month={January},
  howpublished={\url{https://github.com/e3o8o/legitimate-intervention-framework}},
  note={Version 1.2 - 718 DeFi exploits (2014-2026), \$80.48B total losses, 120 intervention cases}
}
```

Or in text:
> "Data sourced from the Legitimate Intervention Framework (LIF) dataset v1.2, containing 718 DeFi exploits from 2014-2026 with $80.48B in total losses and 120 documented interventions."

Please also cite the original source materials as documented in `data_provenance.md`.

---

*Last Updated: January 30, 2026*
*Dataset Version: v1.2*
