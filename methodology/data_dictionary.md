# LIF Data Dictionary

This document defines the schema used in the LIF datasets.

## 1. Main Exploits Dataset Schema
**File:** `data/refined/lif_exploits_final.csv`
**Records:** 718

| Field | Definition | Format |
|:------|:-----------|:-------|
| `date` | The date the exploit occurred or was reported | YYYY-MM-DD |
| `protocol` | The primary target of the attack | String |
| `chain` | The network where the exploit took place | Enum (Ethereum, BSC, Solana, etc.) |
| `loss_usd` | Total value of stolen assets in USD at time of hack | Float |
| `vector_category` | Technical entry point of the exploit | Enum (see below) |
| `is_technical` | True = Code exploit. False = Social/Agency (Rugpull) | Boolean |
| `description` | Contextual details or contract references | String |
| `source_file` | Reference to raw evidence in `data/raw/` | String |
| `incident_id` | Unique identifier (protocol_date format) | String |
| `loss_prevented_usd` | Value of assets saved through intervention | Float |
| `is_intervention` | Whether intervention mechanisms were involved | Boolean |
| `scope` | Scope of intervention | Enum (Account, Asset, Module, Network, Protocol) |
| `authority` | Authority type for intervention | Enum (Signer Set, Governance, Delegated Body) |
| `time_to_detect_min` | Time to detect incident in minutes | Float |
| `time_to_contain_min` | Time to contain incident in minutes | Float |
| `containment_success_pct` | Percentage of assets contained/recovered | Float (0-100) |
| `intervention_notes` | Details about intervention actions | String |
| `intervention_source` | Source URL for intervention details | URL |
| `confidence_level` | Confidence in data accuracy | Enum (high, medium, low) |
| `is_lif_relevant` | Whether incident is intervention-eligible | Boolean |

### Attack Vector Taxonomy

| Vector | Description | Count |
|:-------|:------------|:------|
| Logic Bug | Smart contract logic errors | 231 |
| Key Compromise | Private key theft or leakage | 154 |
| Flash Loan | Uncollateralized loan attack | 89 |
| Oracle Manipulation | Price feed manipulation | 67 |
| Reentrancy | Recursive call vulnerability | 45 |
| Bridge Exploit | Cross-chain bridge vulnerability | 38 |
| Access Control | Permission/role bypass | 32 |
| Economic Design | Tokenomics/mechanism failure | 28 |
| Other | Miscellaneous/uncategorized | 34 |

---

## 2. Intervention Metrics Schema
**File:** `data/refined/lif_intervention_metrics.csv`
**Records:** 30

This dataset tracks intervention effectiveness with detailed timing data. It drives calibration models in the *Legitimate Overrides in Decentralized Protocols* paper.

| Field | Definition | Format |
|:------|:-----------|:-------|
| `incident_id` | Unique identifier mapping to main database | String |
| `protocol` | Name of the protocol targeted | String |
| `date` | Date of the intervention | YYYY-MM-DD |
| `chain` | Network where intervention took place | String |
| `scope` | Hierarchical level of intervention precision | Enum (see below) |
| `authority` | Type of body that triggered intervention | Enum (see below) |
| `time_to_detect_min` | Minutes from exploit start to detection | Float |
| `time_to_contain_min` | Minutes from detection to mechanism execution | Float |
| `containment_success_pct` | Percentage of at-risk funds saved | Integer (0-100) |
| `loss_usd` | Realized loss despite intervention (USD) | Float |
| `loss_prevented_usd` | Value saved by intervention (USD) | Float |
| `notes` | Technical context on mechanism used | String |
| `source` | Primary source URL (post-mortem, tweet) | URL |

### Scope Hierarchy

| Level | Scope | Description | Blast Radius |
|:------|:------|:------------|:-------------|
| 1 | Network | Chain-wide halt/reconfiguration | Maximum |
| 2 | Asset | Token freeze across holders | High |
| 3 | Protocol | dApp-wide pause | Medium |
| 4 | Module | Feature-specific pause | Low |
| 5 | Account | Targeted address freeze | Minimal |

### Authority Types

| Authority | Description | Median Response |
|:----------|:------------|:----------------|
| Signer Set | Fixed key-holders (e.g., 3-of-5 multisig) | ~60 min |
| Delegated Body | Council/committee with bounded mandate | ~45 min |
| Governance | Token-holder vote or validator coordination | ~61 hours |

---

## 3. All Interventions Schema
**File:** `data/refined/lif_all_interventions.csv`
**Records:** 114

This dataset contains all DeFi exploit interventions (subset of main exploits where `is_intervention = True`).

| Field | Definition | Format |
|:------|:-----------|:-------|
| `protocol` | Name of the protocol | String |
| `date` | Date of the exploit/intervention | YYYY-MM-DD |
| `chain` | Network | String |
| `loss_usd` | Total loss despite intervention | Float |
| `loss_prevented_usd` | Value saved by intervention | Float |
| `scope` | Intervention scope | Enum |
| `authority` | Authority type | Enum |
| `time_to_detect_min` | Detection time | Float |
| `time_to_contain_min` | Containment time | Float |
| `containment_success_pct` | Success percentage | Float |
| `notes` | Intervention details | String |
| `source` | Evidence URL | URL |

---

## Methodology: Inclusion vs. Exclusion

The primary dataset applies filters based on research scope:

### Inclusion Criteria
1. `is_technical == True` — Code exploit (not social/agency)
2. `loss_usd >= 100,000` — Material impact threshold

### Excluded Categories

#### 1. Agency Problem Incidents (Insider Theft / Exit Scams)
> **Examples:** Africrypt ($3.6B), QuadrigaCX ($130M), BTER ($1.75M)

Per Charoenwong & Bernardi (2022), Agency Problem hacks produced the highest single-event losses. Excluded because:

- **Root Cause:** Human betrayal, not code vulnerability
- **LIF Scope:** Framework focuses on code-level protections, not governance controls
- **Research Track:** Better addressed by governance mechanism design research

> **Note:** These incidents remain in raw data for total loss context but are filtered from LIF-relevant statistics via `is_technical = False`.

#### 2. Centralized Exchange (CEX) Hacks
> **Examples:** Bybit ($1.4B), Mt. Gox ($460M), Coincheck ($533M)

CEX hacks are included for strategic context but not the primary LIF focus because:

- **Centralized Custody:** "Freeze" is a manual, centralized operator action
- **LIF Focus:** Decentralized protocol governance mechanisms
- **Mitigation Path:** Traditional InfoSec (SOC 2, HSM, insurance) rather than on-chain governance

> **Note:** CEX hacks are tagged `is_lif_relevant = False` but remain in the dataset for total loss statistics.

---

## Usage Guidelines

When citing LIF statistics:

| Purpose | Dataset |
|:--------|:--------|
| Total loss context | `lif_exploits_final.csv` (full 718 cases, $80.48B) |
| LIF-addressable market | Filter by `is_lif_relevant = True` (424 cases, $10.21B) |
| Intervention effectiveness | `lif_intervention_metrics.csv` (30 detailed cases) |
| Intervention universe | `lif_all_interventions.csv` (114 DeFi cases) |
| Combined unique interventions | Cross-reference both (120 unique cases) |

---

## References

- Charoenwong, B., & Bernardi, M. (2022). *A Decade of Cryptocurrency 'Hacks': 2011–2021*. SSRN. https://ssrn.com/abstract=3944435
- See `methodology/data_provenance.md` for complete source documentation

---

*Last Updated: January 30, 2026*
*Dataset Version: v1.2*
