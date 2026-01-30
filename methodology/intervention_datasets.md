# LIF Intervention Datasets

This document explains the structure and purpose of the intervention-related datasets in the LIF repository.

## Dataset Overview

### 1. `lif_all_interventions.csv` (114 cases)
**Purpose:** Complete list of all identified DeFi exploit intervention cases

| Metric | Value |
|:-------|:------|
| **Size** | 114 records |
| **Coverage** | 2016-2026 |
| **Total Loss at Risk** | $7.70B |
| **Total Prevented** | $2.57B |

**Scope:** All DeFi incidents where `is_intervention = True`

**Key Statistics by Year:**
| Year | Cases |
|:-----|:------|
| 2016-2020 | 5 |
| 2021 | 15 |
| 2022 | 18 |
| 2023 | 12 |
| 2024 | 35 |
| 2025 | 25 |
| 2026 (Jan) | 4 |

**Top 10 by Loss:**
1. Ronin ($624M)
2. Poly Network ($611M)
3. Wormhole ($326M)
4. WazirX ($235M)
5. Cetus ($223M)
6. Euler Finance ($197M)
7. Nomad ($190M)
8. Beanstalk ($182M)
9. Wintermute ($160M)
10. Cream Finance ($130M)

---

### 2. `lif_intervention_metrics.csv` (30 cases)
**Purpose:** Highly curated subset with comprehensive timing and response analysis

| Metric | Value |
|:-------|:------|
| **Size** | 30 records |
| **Coverage** | 2020-2025 |
| **Total Loss at Risk** | $3.02B |
| **Total Prevented** | $2.41B |

**Key Metrics Available:**
- `time_to_detect_min`: Minutes from exploit start to first credible detection
- `time_to_contain_min`: Minutes from detection to successful mechanism execution
- `containment_success_pct`: Percentage of at-risk funds saved
- `scope`: Intervention scope (Account, Asset, Module, Network, Protocol)
- `authority`: Authority type (Signer Set, Delegated Body, Governance)
- Detailed notes and source URLs

---

## Combined Unique Interventions: 120 Cases

After cross-referencing and deduplication:

| Source | Records | Overlap | Unique |
|:-------|:--------|:--------|:-------|
| All Interventions | 114 | 24 | 90 |
| Metrics Dataset | 30 | 24 | 6 |
| **Combined** | — | — | **120** |

**Proactive-Only Cases (6 unique to metrics):**
- Tether/PDVSA — Sanctions compliance freeze
- Liqwid — Flash crash response
- StakeWise — Post-exploit recovery
- MakerDAO — USDC depeg emergency response
- Aave v2 — CRV market pause
- Circle/Tornado Cash — OFAC sanctions blacklist

---

## Selection Criteria for 30 Detailed Cases

The 30 cases in `lif_intervention_metrics.csv` were selected based on:

1. **Data Quality**: Well-documented interventions with reliable sources
2. **Representative Diversity**: Covers different scopes, authorities, and outcomes
3. **Recent Relevance**: Focus on 2020+ cases with modern DeFi context
4. **Analysis Value**: Cases that provide insights into intervention effectiveness
5. **Loss Significance**: Mix of high and medium impact interventions

---

## Scope Coverage Analysis

### Scope Distribution (Combined)
| Scope | Cases | % |
|:------|:------|:---|
| Protocol | 56 | 46.7% |
| Account | 50 | 41.7% |
| Network | 8 | 6.7% |
| Asset | 4 | 3.3% |
| Module | 2 | 1.7% |

### Authority Distribution (Combined)
| Authority | Cases | % |
|:----------|:------|:---|
| Delegated Body | 53 | 44.2% |
| Signer Set | 38 | 31.7% |
| Governance | 29 | 24.2% |

---

## Scope Coverage Differences

### Detailed 30 Cases (lif_intervention_metrics.csv)
- **Includes:** Module-level and Asset-level interventions
- **Coverage:** Broader intervention universe including preventative measures
- **Examples:** 
  - Module: Aave v2 governance pause, MakerDAO emergency response, dYdX market manipulation response
  - Asset: Tether wallet freezes, Circle blacklist actions, USDC sanctions compliance

### All Interventions (lif_all_interventions.csv)  
- **Includes:** Only on-chain exploit interventions
- **Coverage:** DeFi protocol exploits with intervention responses
- **Focus:** Technical exploits requiring on-chain intervention
- **Filtering:** Excludes infrastructure cases (e.g., browser extension compromises)

### Reconciliation Details
- **6 cases** in detailed analysis are **not in all interventions** because:
  - **3 Module cases:** System-level governance/risk management responses
    - dYdX (2023-11-07) — Market manipulation response  
    - Curve Finance (2023-07-30) — Vyper compiler bug response
    - MakerDAO (2023-03-11) — USDC depeg emergency response
  - **3 Asset cases:** Off-chain token issuer actions
    - Tether/PDVSA (2026-01-11) — Sanctions compliance freeze
    - Circle/Tornado Cash (2022-08-08) — OFAC sanctions blacklist
    - Aave v2 (2022-11-22) — CRV market pause

---

## Usage Guidelines

### For Paper Analysis
- Use `lif_intervention_metrics.csv` for detailed intervention effectiveness analysis
- Reference `lif_all_interventions.csv` for comprehensive statistics and context

### For Statistical Overview
- Use `lif_all_interventions.csv` for complete intervention universe statistics
- Filter by year, scope, authority, or loss amount as needed

### For Research Extensions
- `lif_all_interventions.csv` provides the full list for potential expansion
- New cases can be added to the detailed metrics file as they meet selection criteria

---

## Data Integrity

- All intervention cases verified through multiple sources
- Loss amounts standardized to USD (historical rates where needed)
- Timeline data cross-referenced across security reports
- Intervention details extracted from official post-mortems
- Cross-reference sync between datasets completed (Jan 2026)

---

*Last Updated: January 30, 2026*
*Dataset Version: v1.2*
