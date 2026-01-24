# LIF Dataset Summary (Jan 2026)

## Current Repository State

The Legitimate Intervention Framework (LIF) repository has been cleaned and finalized with the following key datasets:

### Primary Datasets

#### 1. Main Exploits Dataset
**File:** `data/refined/lif_exploits_final.csv`
- **Total Incidents:** 692 (deduplicated and manually reviewed)
- **Date Range:** 2014-03-01 to 2025-12-27
- **Total Loss:** $61.05 billion
- **LIF-Relevant:** 402 incidents (~$8.78B)
- **Format:** CSV with comprehensive incident metadata

#### 2. Source Data
**File:** `data/refined/lif_exploits_raw.csv`
- **Raw Incidents:** 1903 (before deduplication and cleaning)
- **Purpose:** Reproducibility and pipeline transparency
- **Sources:** Multiple raw data feeds consolidated

#### 3. Intervention Analysis
**File:** `data/refined/lif_intervention_metrics.csv`
- **Intervention Cases:** 30 detailed cases
- **Analysis:** Scope, authority, effectiveness metrics
- **Purpose:** Framework validation and calibration

### Data Sources

The dataset combines information from multiple authoritative sources:
1. **Charoenwong & Bernardi (2022)** - Academic research (2011-2021)
2. **De.Fi Rekt Database** - Industry database (2021-2025)
3. **Rekt News Reports** - Investigative journalism (2020-2025)
4. **DeFiHackLabs** - Technical incident database (2022-2025)
5. **Manual Research** - Q4 2025 URL enrichment and verification

### Key Statistics

- **Top Protocol:** Terra / Luna ($40B loss)
- **Most Common Vector:** Logic Bug / Code Error
- **Highest Loss Chain:** Terra ($40B)
- **Average Detection Time:** Varies by intervention type
- **Success Rate:** Intervention-dependent (30-100% containment)

### Quality Assurance

- Manual review and deduplication completed
- Source verification and URL enrichment
- Chronological sorting maintained
- Data validation and consistency checks
- Statistical analysis and documentation

### Usage

This dataset serves as the authoritative source for:
- LIF framework research and validation
- Intervention mechanism analysis
- DeFi security trend analysis
- Academic research on governance interventions

### Citation

When using this dataset, please cite:

```bibtex
@misc{lif_dataset_2026,
  title={Legitimate Intervention Framework (LIF) Dataset},
  author={Legitimate Intervention Framework Research Team},
  year={2026},
  month={January},
  howpublished={\url{https://github.com/e3o8o/legitimate-intervention-framework}},
  note={Version 1.0 - 693 DeFi exploits (2014-2025), $81.05B total losses}
}
```

Or in text:
> "Data sourced from the Legitimate Intervention Framework (LIF) dataset, containing 693 DeFi exploits from 2014-2025 with $81.05B in total losses."

Please also cite the original source materials as documented in `data_provenance.md`.

---

*Last Updated: January 24, 2026*
*Dataset Version: Final (v1.0)*
