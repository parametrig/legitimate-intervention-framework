# LIF Dataset Summary

**Last Updated:** 2026-02-13  
**Version:** 1.0

---

## Overview

The Legitimate Intervention Framework (LIF) dataset contains standardized, high-quality data on blockchain security incidents and emergency interventions from 2014-03-01 to 2026-01-21.

---

## Key Statistics

| Metric | Value |
|:-------|:------|
| **Total Exploit Cases** | 705 |
| **Non-Technical Cases** | 40 |
| **CeFi Technical Cases** | 18 |
| **Systemic Economic Cases** | 10 |
| **Technical Cases** | 640 |
| **LIF-Relevant Cases** | 601 |
| **Total Intervention Cases** | 130 |
| **High-Fidelity Metrics Cases** | 52 (includes proactive cases) |
| **Total Losses** | $78,805,538,747 |
| **Total Prevented (Interventions Dataset)** | $2,511,574,380 |
| **Total Prevented (Metrics Subset)** | $1,666,149,380 |
| **Date Range** | 2014-03-01 to 2026-01-21 |

---

## Case Classification Methodology

The dataset separates cases into distinct layers based on intervention potential and technical nature:

### Non-Technical Cases (40 cases)
**Criteria:** Social engineering, phishing, rugpulls, and agency-based attacks
- **Examples:** Wallet phishing scams, token rugpulls, social media impersonation
- **Intervention Potential:** Limited - requires user education and platform-level safeguards
- **Classification:** `is_technical = False`

### CeFi Technical Cases (18 cases)  
**Criteria:** Technical exploits at centralized exchanges and custodial services
- **Examples:** Mt. Gox hack, KuCoin breach, centralized exchange vulnerabilities
- **Intervention Potential:** Moderate - centralized authority can intervene
- **Classification:** `is_technical = True`, `ecosystem = CeFi`

### Systemic Economic Cases (10 cases)
**Criteria:** Economic collapses and systemic failures affecting entire ecosystems
- **Examples:** Terra/Luna depeg, FTX collapse, Three Arrows Capital liquidation
- **Intervention Potential:** Complex - requires coordinated multi-stakeholder response
- **Classification:** `is_technical = False` (economic rather than technical failure)
- **Total Value:** $61.80B

### Technical Cases (640 cases)
**Criteria:** Smart contract exploits, protocol vulnerabilities, and technical attacks
- **Examples:** DeFi protocol hacks, bridge exploits, oracle manipulation
- **Intervention Potential:** High - amenable to technical intervention mechanisms
- **Classification:** `is_technical = True`

### LIF-Relevant Cases (601 cases)
**Criteria:** Technical cases where intervention mechanisms could have prevented or mitigated losses
- **Subset:** All technical cases minus those with no viable intervention points
- **Classification:** `is_lif_relevant = True`
- **Focus:** Cases that inform the LIF framework design
- **Total Value:** $9.60B

---

## Dataset Files

### 1. `data/refined/lif_exploits_final.csv`
- **Records:** 705
- **Description:** Complete database of all exploit incidents
- **Fields:** 26 columns including incident details, classifications, and intervention data
- **Format:** CSV with headers

### 2. `data/refined/lif_all_interventions.csv`
- **Records:** 130
- **Description:** Subset of exploits with intervention mechanisms activated
- **Fields:** 26 columns (same schema as exploits)
- **Format:** CSV with headers

### 3. `data/refined/lif_intervention_metrics.csv`
- **Records:** 52
- **Description:** High-fidelity cases with detailed intervention timing and effectiveness
- **Fields:** 18 columns focused on metrics
- **Format:** CSV with headers

---

## Data Quality

- **Sorting:** All datasets sorted by date (most recent first)
- **Validation:** All incident_ids unique and formatted correctly
- **Congruence:** Interventions dataset contains all intervention cases from exploits
- **Completeness:** No missing required fields (date, protocol, loss_usd)
- **Classification:** All cases have ecosystem, scope, and authority assigned

---

## Usage Guidelines

1. **For exploit analysis:** Use `lif_exploits_final.csv`
2. **For intervention studies:** Use `lif_all_interventions.csv`
3. **For effectiveness metrics:** Use `lif_intervention_metrics.csv`

See `data_dictionary.md` for complete field definitions.

---

## Citation

If using this dataset in academic work, please cite:

```bibtex
@dataset{lif_dataset_2025,
  title={Legitimate Intervention Framework (LIF) Dataset},
  author={LIF Research Team},
  year={2025},
  url={https://github.com/e3o8o/legitimate-intervention-framework},
  note={Version 1.0, 2026-02-03}
}
```
