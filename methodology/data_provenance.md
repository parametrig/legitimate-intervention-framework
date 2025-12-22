# Data Provenance: NCF Hack Database

This document details the origins and ingestion methodology for the datasets used in the Native Compliance Framework (NCF) research.

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
- **Note:** This file consolidates data from multiple batch ingestions (originally `batch_2.txt` to `batch_5.txt` from the `ncf` working directory).

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

## Ingestion Methodology

To ensure reproducibility and zero manual manipulation, all data follows this 3-step pipeline:

1. **Parse (`scripts/core/parse_sources.py`):** Reads all raw files from `data/raw/` and maps them to a unified CSV schema. Output: `data/build/parsed_raw.csv`.
2. **Deduplicate (`scripts/core/deduplicate.py`):** Merges records that refer to the same incident (keyed by date and protocol name). Output: `data/build/merged_master.csv`.
3. **Filter (`scripts/core/filter_ncf.py`):** Applies high-signal NCF filters:
    - `is_technical == True` (Eliminates Rugpulls, Honeypots, Agency Problems)
    - `loss_usd >= 100,000` (Eliminates low-value noise)
    - Output: `data/refined/ncf_exploits_final.csv`

### Reproducibility Command
```bash
# From the repository root:
cd scripts/core/
python3 parse_sources.py
python3 deduplicate.py
python3 filter_ncf.py
```
