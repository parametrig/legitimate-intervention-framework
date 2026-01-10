# Data Provenance: LIF Hack Database

This document details the origins and ingestion methodology for the datasets used in the Legitimate Intervention Framework (LIF) research.

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

---

## Ingestion & Analysis Pipeline

### Step 1-3: Data Pipeline (Parse → Dedupe → Filter)
```bash
python3 scripts/core/parse_sources.py   # → data/build/parsed_raw.csv
python3 scripts/core/deduplicate.py     # → data/build/merged_master.csv
python3 scripts/core/filter_lif.py      # → data/refined/lif_exploits_final.csv
```

### Step 4: Analysis & Visualization
```bash
# Run the master Jupyter notebook (single source of truth)
jupyter nbconvert --execute --to notebook scripts/analysis/lif_charts.ipynb
```

**Outputs:**
- `data/refined/lif_exploits_cleaned.csv` - Cleaned dataset with LIF relevance tagging
- `data/refined/lif_stats.json` - Rich JSON statistics with external data sources
- `visualizations/*.png` - 24 charts in Light Mode palette

---

## Final Dataset Statistics

| Metric | Value |
|:-------|:------|
| Total Exploits | 759 |
| Total Loss | $91.3 Billion |
| LIF-Relevant | 440 ($10.9B) |
| Date Range | 2014-03-01 to 2025-12-16 |

---

## External Data Sources (Sourced in Analysis)

The analysis notebook incorporates additional sourced data:
- **Charoenwong & Bernardi (2022)** - Hack type distribution (66% Security Breach)
- **Bybit Security Report (Nov 2025)** - Blockchain freezing capability (21% can freeze)
- **Anthropic Red Team (Dec 2025)** - AI exploit acceleration (doubling every 1.3 months)

