# Data Provenance: LIF Hack Database

This document details the origins and ingestion methodology for the datasets used in the Legitimate Intervention Framework (LIF) research.

## Current Dataset Status (January 2026)

**Final Processed Dataset:** `data/refined/lif_exploits_final.csv`
- **Total Incidents:** 718 (deduplicated and manually reviewed)
- **Date Range:** 2014-03-01 to 2026-01-21
- **Total Loss:** $80.48 billion
- **LIF-Relevant:** 424 incidents ($10.21B)
- **Combined Unique Interventions:** 120 cases (114 DeFi + 6 proactive)

**Intervention Datasets:**
- `lif_all_interventions.csv` — 114 standardized DeFi intervention cases
- `lif_intervention_metrics.csv` — 30 highly curated cases with detailed timing/response analysis

**Source Data:** `data/refined/lif_exploits_raw.csv`
- **Raw Incidents:** 1903 (before deduplication and cleaning)
- **All original sources preserved for reproducibility**

---

## Primary Sources

### 1. Charoenwong & Bernardi (2011 - 2021)
- **Source:** *A Decade of Cryptocurrency 'Hacks': 2011 – 2021* (Ben Charoenwong & Mario Bernardi, January 2022).
- **Format:** Extracted as raw text from Table 1 of the SSRN working paper.
- **Reference File:** `data/raw/charoenwong_bernardi_table.txt`
- **Scope:** 30 large-scale thefts prior to the modern "DeFi Summer" peak and AI-exploit era.
- **Citation:** [SSRN 3944435](https://ssrn.com/abstract=3944435)

### 2. De.Fi Rekt Database (2021 - 2026)
- **Source:** Consolidated from the De.Fi Rekt Database, covering 2021-2026.
- **Format:** Raw text blocks.
- **Reference File:** `data/raw/rekt_database_raw.txt`
- **Scope:** ~450 incidents (after January 2026 refresh)
- **Note:** This file consolidates data from multiple batch ingestions.

### 3. Rekt News Investigative Reports (2020 - 2025)
- **Source:** In-depth post-mortem reports from [rekt.news](https://rekt.news) providing protocol, date, loss, vector, and scenario context.
- **Format:** Structured text blocks with field delimiters.
- **Reference File:** `data/raw/rekt_news_extra.txt`
- **Scope:** 282 high-fidelity investigative reports.

### 4. DeFiHackLabs (2022 - 2026)
- **Source:** Curated incident list from the `defihacklabs` security community.
- **Format:** JSON.
- **Reference File:** `data/raw/defihacklabs_incidents.json`
- **Scope:** ~200 incidents with PoC references.

### 5. Intervention Incidents (Manual Curation)
- **Source:** High-fidelity manual research from post-mortems, on-chain alerts, and official project tweets/forums.
- **Format:** Structured CSV.
- **Reference File:** `data/refined/lif_intervention_metrics.csv`
- **Scope:** 30 incidents specifically chosen for their clearly observable intervention mechanics (pauses, freezes, halts). Includes both technical hacks and systemic market failures.
- **Provenance Link:** Each row in the CSV contains a `source` URL pointing to the evidence (Post-mortem or TX hash).

---

## Ingestion & Analysis Pipeline

### Pipeline Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Raw Sources    │ ──▶ │  Parse & Clean  │ ──▶ │  Deduplicate    │
│  (4 databases)  │     │  (standardize)  │     │  (cross-ref)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Final Dataset  │ ◀── │  Manual Review  │ ◀── │  LIF Tagging    │
│  (718 cases)    │     │  (verification) │     │  (relevance)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Step 1: Raw Data Ingestion
- Extract raw text/JSON from source databases
- Normalize date formats (YYYY-MM-DD)
- Standardize currency to USD (using historical rates where needed)

### Step 2: Schema Standardization
- Map source-specific fields to LIF schema
- Apply attack vector taxonomy
- Tag chain identifiers

### Step 3: Deduplication
- Cross-reference incidents across sources
- Match on: protocol name, date (±3 days), loss amount (±10%)
- Manual review for edge cases

### Step 4: LIF Relevance Tagging
- `is_technical`: Code exploit vs. social/agency
- `is_lif_relevant`: Protocol-level intervention possible
- `is_intervention`: Intervention mechanism was actually invoked

### Step 5: Intervention Metrics (Manual)
- Source post-mortems and security analyses
- Extract timing data (detection, containment)
- Classify scope and authority
- Calculate containment success percentage

### Step 6: Analysis Notebook
```bash
jupyter nbconvert --execute --to notebook scripts/analysis/lif_charts_v1.2.ipynb
```

**Outputs:**
- `data/refined/lif_exploits_final.csv` — Primary deduplicated dataset (Source of Truth)
- `data/refined/lif_stats.json` — Comprehensive stats generated from cleaned data
- `visualizations/v1.2/*.png` — v1.2 analysis charts (50 visualizations)
- `visualizations/archived/` — Legacy analysis charts

---

## Final Dataset Statistics (January 2026)

| Metric | Value |
|:-------|:------|
| Total Exploits | 718 |
| Total Loss | $80.48 Billion |
| LIF-Relevant | 424 ($10.21B) |
| Intervention Cases | 120 unique (114 DeFi + 6 proactive) |
| Prevented Loss | $2.77B (27.2% capture rate) |
| Date Range | 2014-03-01 to 2026-01-21 |

### Market Analysis
| Segment | Value | % of Market |
|:--------|:------|:------------|
| Successfully Prevented | $2.77B | 21.4% |
| Incurred (Despite Intervention) | $7.70B | 59.3% |
| Incurred (No Intervention) | $2.51B | 19.4% |
| **Total LIF Market** | **$12.99B** | 100% |

---

## External Data Sources (Sourced in Analysis)

The analysis notebook incorporates additional sourced data:
- **Charoenwong & Bernardi (2022)** — Hack type distribution (66% Security Breach)
- **Charoenwong et al. (2025)** — Regulatory framework evaluation [SSRN 5368708](https://ssrn.com/abstract=5368708)
- **Bybit Security Report (Nov 2025)** — Blockchain freezing capability (21% can freeze) [Report](https://assets.contentstack.io/v3/assets/bltffdbacf2f22e15fa/bltda1597363a4f2a2b/69144b86424c333a34bc9fa8/2509-T68340_Security_Report_1111.pdf)
- **Anthropic Red Team (Dec 2025)** — AI exploit acceleration (doubling every 1.3 months) [red.anthropic.com](https://red.anthropic.com/2025/smart-contracts/)

---

## Data Quality Notes

### Fixes Applied (January 2026)
1.  **Poly Network Authority Fix**: Changed from "Governance" to "Delegated Body"
2.  **Duplicate Removal**: Removed PancakeBunny duplicate
3.  **Standardization**: Removed `authority_standardized` column
4.  **Cross-Reference Sync**: Added 13 exploit cases from metrics to all_interventions
5.  **Exploits Final Sync**: Added 12 missing exploits to lif_exploits_final.csv
6.  **Loss Prevented Data Fix**: Copied complete timing data to incomplete rows

### Known Limitations
- Response times are often estimated from public disclosure timing
- Some intervention outcomes lack complete post-mortem documentation
- Cross-chain value calculations use snapshot USD rates

---

*Last Updated: January 30, 2026*
*Dataset Version: v1.2*
