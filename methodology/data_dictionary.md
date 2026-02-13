# LIF Data Dictionary

This document defines the schema used in the LIF datasets.

**Last Updated:** 2026-02-03  
**Dataset Version:** 1.0

---

## 1. Main Exploits Dataset Schema
**File:** `data/refined/lif_exploits_final.csv`  
**Records:** 705

| Field | Definition | Format |
|:------|:-----------|:-------|
| `incident_id` | Unique identifier (PROTOCOL-YYYY-MM-DD format) | String |
| `date` | The date the exploit occurred or was reported | YYYY-MM-DD |
| `protocol` | The primary target of the attack | String |
| `chain` | The network where the exploit took place | Enum (Ethereum, Solana, BSC, etc.) |
| `loss_usd` | Total value of stolen assets in USD at time of hack | Float |
| `loss_prevented_usd` | Value of assets saved through intervention | Float |
| `is_technical` | True = Code exploit. False = Social/Agency (Rugpull) | Boolean |
| `is_lif_relevant` | Whether case is relevant to LIF framework | Boolean |
| `is_intervention` | Whether intervention mechanisms were involved | Boolean |
| `vector_category` | Technical entry point of the exploit | Enum (see below) |
| `ecosystem` | Blockchain ecosystem classification | Enum (EVM, Non-EVM, CeFi, App-Chain, Other/Multi) |
| `scope` | Scope of intervention | Enum (Account, Asset, Module, Network, Protocol) |
| `authority` | Authority type for intervention | Enum (Signer Set, Governance, Delegated Body) |
| `time_to_detect_min` | Minutes from exploit start to detection | Float |
| `time_to_contain_min` | Minutes from detection to containment | Float |
| `containment_success_pct` | Percentage of funds successfully protected | Float |
| `success_tier` | Categorical success level | Enum (Full, Partial, Reactive, N/A) |
| `description` | Contextual details or contract references | String |
| `notes` | Additional notes | String |
| `intervention_notes` | Specific intervention details | String |
| `source_type` | Type of source material | Enum |
| `intervention_source` | URL to primary source | String |
| `source_raw` | Raw source reference | String |
| `confidence_level` | Data confidence (high/medium/low) | Enum |
| `source_file` | Reference to raw evidence | String |
| `is_high_fidelity` | Whether case has detailed intervention data | Boolean |

---

## 2. All Interventions Dataset Schema
**File:** `data/refined/lif_all_interventions.csv`  
**Records:** 130

Same schema as exploits_final, but filtered to only cases with `is_intervention=True`.

---

## 3. Intervention Metrics Dataset Schema
**File:** `data/refined/lif_intervention_metrics.csv`  
**Records:** 52

High-fidelity intervention cases with detailed timing and effectiveness metrics.

| Field | Definition | Format |
|:------|:-----------|:-------|
| `incident_id` | Unique identifier | String |
| `date` | Date of incident | YYYY-MM-DD |
| `protocol` | Protocol name | String |
| `chain` | Blockchain network | String |
| `loss_usd` | USD value lost | Float |
| `loss_prevented_usd` | USD value prevented | Float |
| `is_lif_relevant` | LIF framework relevance | Boolean |
| `ecosystem` | Ecosystem classification | Enum |
| `scope` | Intervention scope | Enum |
| `authority` | Intervention authority | Enum |
| `time_to_detect_min` | Detection time in minutes | Float |
| `time_to_contain_min` | Containment time in minutes | Float |
| `containment_success_pct` | Success percentage | Float |
| `success_tier` | Success category | Enum |
| `notes` | Detailed intervention notes | String |
| `source_type` | Source type | Enum |
| `confidence_level` | Confidence rating | Enum |
| `intervention_source` | Source URL | String |

---

## Vector Categories

- **Access Control / Key Compromise**
- **Flash Loan Attack**
- **Oracle Manipulation**
- **Reentrancy**
- **Logic Bug / Code Error**
- **Price Manipulation**
- **Denial Of Service**
- **Security Breach**
- **Insider Threat / Exit Scam**
- **Signature Replay / Validation**
- **Other / Unknown**

---

## Ecosystem Values

- **EVM** - Ethereum Virtual Machine chains (Ethereum, Polygon, Arbitrum, etc.)
- **Non-EVM** - Solana, Cardano, and other non-EVM chains
- **CeFi** - Centralized finance platforms
- **App-Chain** - Application-specific blockchains
- **Other/Multi** - Cross-chain or other classifications

---

## Scope Values

- **Account** - Individual account-level intervention
- **Asset** - Asset/token-level intervention
- **Module** - Smart contract module intervention
- **Network** - Network-wide intervention
- **Protocol** - Entire protocol intervention

---

## Authority Values

- **Signer Set** - Multisig or emergency signer group
- **Governance** - Community governance process
- **Delegated Body** - Council or committee with delegated authority

---

## Statistics Summary

- **Total Exploit Cases:** 705
- **Total Intervention Cases:** 130
- **High-Fidelity Metrics Cases:** 52
- **Total Losses:** $78,805,538,747
- **Total Prevented:** $2,121,149,380
- **LIF-Relevant Cases:** 601
- **Date Range:** 2014-03-01 to 2026-01-21
