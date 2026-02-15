# LIF Intervention Datasets

**Last Updated:** 2026-02-13  
**Version:** 1.0

---

## Intervention Dataset Overview

The LIF intervention datasets track emergency response mechanisms in blockchain protocols.

---

## Dataset Structure

### High-Fidelity Metrics (`lif_intervention_metrics.csv`)
**Records:** 52 (includes proactive cases)

Contains detailed timing and effectiveness data for intervention cases:
- Detection time (minutes)
- Containment time (minutes)
- Success percentage
- Scope and authority classification
- Source attribution with confidence levels

### All Interventions (`lif_all_interventions.csv`)
**Records:** 130

Complete database of exploit-linked cases where intervention mechanisms were activated, including:
- Exploit responses
- Governance actions
- Emergency pauses

---

## Intervention Classification

### By Scope
| Scope | Count | Description |
|:------|:------|:------------|
| Protocol | 60 | Entire protocol intervention |
| Account | 46 | Individual account freeze |
| Network | 9 | Network-wide intervention |
| Module | 9 | Specific module/function pause |
| Asset | 6 | Token/asset-level action |

### By Authority
| Authority | Count | Description |
|:----------|:------|:------------|
| Delegated Body | 48 | Council/committee |
| Signer Set | 47 | Multisig emergency signers |
| Governance | 35 | Community vote |

### By Success Tier
| Tier | Count | Description |
|:-----|:------|:------------|
| Full (100%) | Prevented all losses |
| Partial (1-99%) | Prevented some losses |
| Reactive (0%) | Response after losses |
| N/A | No intervention |

---

## Case Types

### Exploit Interventions
Cases where protocols responded to active exploits:
- **Example:** Curve Finance vyper bug response
- **Example:** BNB Chain bridge exploit pause
- **Count:** 46 cases in metrics dataset

### Proactive Interventions
Cases where protocols intervened without active exploit:
- **Example:** MakerDAO PSM pause during USDC depeg
- **Example:** Tether PDVSA wallet freeze
- **Count:** 7 cases in metrics dataset

---

## Prevented Definitions

The project uses multiple valid but different “prevented loss” aggregates. To avoid ambiguity, always specify which dataset (and therefore which definition) you are using.

### Prevented (All Interventions)
- **Source:** `data/refined/lif_all_interventions.csv`
- **Definition:** `sum(loss_prevented_usd)` across exploit-linked intervention events.
- **Use for:** Website/report headlines about prevented losses across the 130 exploit-linked intervention cases.

### Prevented (Metrics Subset)
- **Source:** `data/refined/lif_intervention_metrics.csv`
- **Definition:** `sum(loss_prevented_usd)` across the 52-case curated, high-fidelity subset.
- **Use for:** Claims that explicitly reference the curated metrics subset (timing + prevention-confidence).

### Prevented (Eligible + Intervened subset)
- **Source:** `data/refined/lif_exploits_final.csv` (filter: `is_lif_relevant==True` and `is_intervention==True`)
- **Definition:** `sum(loss_prevented_usd)` across intervention-eligible exploits where an intervention occurred.
- **Use for:** Market-coverage style analysis where the unit of analysis is the “intervention-eligible exploit market.”

### Important note (paper model vs dataset totals)
- The paper-style market decomposition (e.g., coverage vs effectiveness layers) is a separate modeling/aggregation layer and should not be conflated with dataset-aggregate prevented sums.

## Data Quality Standards

All intervention cases meet these criteria:
1. Primary source documentation
2. Clear timeline of events
3. Quantified losses (actual or prevented)
4. Identified intervention mechanism
5. Confidence level assessment

---

## Usage

### For Researchers
Use `lif_intervention_metrics.csv` for:
- Effectiveness analysis
- Response time studies
- Authority performance comparison
- Scope effectiveness research

### For Protocol Developers
Reference `lif_all_interventions.csv` for:
- Incident response precedents
- Mechanism design patterns
- Failure mode analysis

---

## Methodology Notes

- **Detection Time:** From exploit start to protocol awareness
- **Containment Time:** From awareness to successful intervention
- **Success %:** Funds prevented / Total funds at risk
- **Confidence:** High (official source), Medium (multiple sources), Low (single source)
