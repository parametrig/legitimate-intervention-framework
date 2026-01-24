# Data Provenance: LIF Hack Database

This document details the origins and ingestion methodology for the datasets used in the Legitimate Intervention Framework (LIF) research.

## Current Dataset Status (Jan 2026)

**Final Processed Dataset:** `data/refined/lif_exploits_final.csv`
- **Total Incidents:** 692 (deduplicated and manually reviewed)
- **Date Range:** 2014-03-01 to 2025-12-27
- **Total Loss:** $61.05 billion
- **LIF-Relevant:** 402 incidents (~$8.78B)
- **Intervention Analysis:** 30 detailed cases in `lif_intervention_metrics.csv`

**Source Data:** `data/refined/lif_exploits_raw.csv`
- **Raw Incidents:** 1903 (before deduplication and cleaning)
- **All original sources preserved for reproducibility**

## Primary Sources

### 1. Charoenwong & Bernardi (2011 - 2021)
- **Source:** *A Decade of Cryptocurrency 'Hacks': 2011 – 2021* (Ben Charoenwong & Mario Bernardi, January 2022).
- **Format:** Extracted as raw text from Table 1 of the SSRN working paper.
- **Reference File:** `data/raw/charoenwong_bernardi_table.txt`
- **Scope:** 30 large-scale thefts prior to the modern "DeFi Summer" peak and AI-exploit era.

### 2. De.Fi Rekt Database (2021 - 2025)
- **Source:** Consolidated from the De.Fi Rekt Database, covering 2021-2025.
- **Format:** Raw text blocks.
- **Reference File:** `data/raw/rekt_database_raw.txt`
- **Note:** This file consolidates data from multiple batch ingestions.

### 3. Rekt News Investigative Reports (2020 - 2025)
- **Source:** In-depth post-mortem reports from [rekt.news](https://rekt.news) providing protocol, date, loss, vector, and scenario context.
- **Format:** Structured text blocks with field delimiters.
- **Reference File:** `data/raw/rekt_news_extra.txt`
- **Scope:** 282 high-fidelity investigative reports.

### 4. DeFiHackLabs (2022 - 2025)
- **Source:** Curated incident list from the `defihacklabs` security community.
- **Format:** JSON.
- **Reference File:** `data/raw/defihacklabs_incidents.json`

### 5. Intervention Incidents (Manual Curation)
- **Source:** High-fidelity manual research from post-mortems, on-chain alerts, and official project tweets/forums.
- **Format:** Structured CSV.
- **Reference File:** `data/refined/lif_intervention_metrics.csv`
- **Scope:** 28 incidents specifically chose for their clearly observable intervention mechanics (pauses, freezes, halts). Includes both technical hacks and systemic market failures.
- **Provenance Link:** Each row in the CSV contains a `source` URL pointing to the evidence (Post-mortem or TX hash).

---

## Ingestion & Analysis Pipeline

### Step 1-3: Data Pipeline (Parse → Dedupe → Filter)
```bash
python3 scripts/core/parse_sources.py   # → data/build/parsed_raw.csv
python3 scripts/core/deduplicate.py     # → data/build/merged_master.csv
python3 scripts/core/filter_lif.py      # → data/refined/lif_exploits_final.csv
```

### Step 4: Analysis & Final Cleaning
# Run the master Jupyter notebook (Single source of truth for cleaning & stats)
```bash
jupyter nbconvert --execute --to notebook scripts/analysis/lif_charts.ipynb
```

**Outputs:**
- `data/refined/lif_exploits_cleaned.csv` - Primary deduplicated dataset (Source of Truth)
- `data/refined/lif_stats.json` - Comprehensive stats generated from cleaned data
- `visualizations/*.png` - Analysis charts based on cleaned data

---

## Final Dataset Statistics

| Metric | Value |
|:-------|:------|
| Total Exploits | 763 |
| Total Loss | $91.32 Billion |
| LIF-Relevant | 439 ($10.77B) |
| Intervention Incidents | 28 Verified Cases |
| Date Range | 2014-03-01 to 2026-01-13 |

---

## External Data Sources (Sourced in Analysis)

The analysis notebook incorporates additional sourced data:
- **Charoenwong & Bernardi (2022)** - Hack type distribution (66% Security Breach)
- **Bybit Security Report (Nov 2025)** - Blockchain freezing capability (21% can freeze)
- **Anthropic Red Team (Dec 2025)** - AI exploit acceleration (doubling every 1.3 months)

