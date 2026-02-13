# LIF Data Provenance

**Last Updated:** 2026-02-03  
**Version:** 1.0

---

## Data Sources

The LIF dataset integrates information from multiple authoritative sources:

### Primary Sources
- **Rekt News** - Detailed exploit postmortems
- **DeFiHackLabs** - Comprehensive incident database
- **Official Postmortems** - Protocol-published reports
- **Security Firm Reports** - CertiK, Trail of Bits, OpenZeppelin
- **Academic Research** - Charoenwong & Bernardi tables

### Secondary Sources
- **News Outlets** - BBC, The Block, CoinDesk
- **Social Media** - Twitter/X official announcements
- **Governance Forums** - Protocol governance documentation
- **GitHub Repositories** - Technical postmortems

---

## Data Processing Pipeline

1. **Collection** - Aggregated from 15+ sources
2. **Standardization** - Unified date format and incident_id structure
3. **Classification** - Categorized by ecosystem, scope, authority
4. **Validation** - Cross-referenced multiple sources
5. **Enrichment** - Added intervention timing and effectiveness data
6. **Quality Control** - Manual review of high-value cases

---

## Dataset Status

| Dataset | Status | Records | Last Updated |
|:--------|:-------|:--------|:-------------|
| lif_exploits_final.csv | Complete | 705 | 2026-02-13 |
| lif_all_interventions.csv | Complete | 130 | 2026-02-13 |
| lif_intervention_metrics.csv | Complete | 52 | 2026-02-03 |

---

## Quality Metrics

- **Completeness:** 100% of cases have required fields
- **Accuracy:** All amounts cross-referenced with multiple sources
- **Consistency:** Standardized formatting across all records
- **Attribution:** All cases linked to primary sources

---

## Updates

- **v1.0** (2026-02-03) - Complete dataset overhaul
  - Standardized all incident_id formats
  - Added ecosystem classifications
  - Enhanced intervention metrics
  - Sorted by date (most recent first)
  - Fixed all Unknown/NaN values
