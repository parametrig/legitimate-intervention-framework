# LIF Intervention Datasets

**Last Updated:** 2026-02-03  
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

Complete database of all cases where intervention mechanisms were activated, including:
- Exploit responses
- Proactive interventions
- Governance actions
- Emergency pauses

---

## Intervention Classification

### By Scope
| Scope | Count | Description |
|:------|:------|:------------|
| Protocol | ~20 | Entire protocol intervention |
| Module | ~10 | Specific module/function pause |
| Account | ~8 | Individual account freeze |
| Asset | ~7 | Token/asset-level action |
| Network | ~7 | Network-wide intervention |

### By Authority
| Authority | Count | Description |
|:----------|:------|:------------|
| Signer Set | 37 | Multisig emergency signers |
| Delegated Body | 8 | Council/committee |
| Governance | 6 | Community vote |

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
- **Count:** ~47 cases in metrics dataset

### Proactive Interventions
Cases where protocols intervened without active exploit:
- **Example:** MakerDAO PSM pause during USDC depeg
- **Example:** Tether PDVSA wallet freeze
- **Count:** ~5 cases in metrics dataset

---

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
