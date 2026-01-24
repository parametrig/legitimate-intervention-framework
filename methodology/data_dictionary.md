# LIF Data Dictionary

This document defines the schema used in the `lif_exploits_final.csv` (primary dataset) and across the research pipeline.

## 1. Main Exploits Dataset Schema
**File:** `data/refined/lif_exploits_final.csv`

| Field | Definition | Enum / Format |
| :--- | :--- | :--- |
| `date` | The date the exploit occurred or was reported. | YYYY-MM-DD |
| `protocol` | The primary target of the attack. | String |
| `chain` | The network where the exploit took place. | Enum (Ethereum, BSC, SOL, etc.) |
| `loss_usd` | The total value of stolen assets in USD at the time of the hack. | Float |
| `vector_category` | The technical entry point of the exploit. | Enum (Reentrancy, Logic Flaw, CPIMP, etc.) |
| `is_technical` | Boolean flag. True = Code exploit. False = Social/Agency (Rugpull). | Boolean |
| `description` | Contextual details or contract references. | String |
| `source_file` | Reference to the raw evidence in `data/raw/` or refined data sources. | String |
| `incident_id` | Unique identifier for the incident (protocol_date format). | String |
| `loss_prevented_usd` | Value of assets saved through intervention mechanisms. | Float |
| `is_intervention` | Boolean flag indicating if intervention mechanisms were involved. | Boolean |
| `scope` | Scope of intervention (Account, Asset, Module, Network, Protocol). | Enum |
| `authority` | Authority type for intervention (Signer Set, Governance, Delegated Body). | Enum |
| `time_to_detect_min` | Time to detect incident in minutes. | Float |
| `time_to_contain_min` | Time to contain incident in minutes. | Float |
| `containment_success_pct` | Percentage of assets successfully contained/recovered. | Float |
| `intervention_notes` | Detailed notes about intervention actions and effectiveness. | String |
| `intervention_source` | Source URL for intervention details. | String |
| `confidence_level` | Confidence level in data accuracy (high, medium, low). | Enum |
| `is_lif_relevant` | Boolean flag indicating if incident is relevant to LIF framework. | Boolean |

---

## 2. Intervention Incidents Schema
**File:** `data/refined/lif_intervention_metrics.csv`

This dataset tracks the effectiveness of on-chain emergency mechanisms triggered by both security exploits and systemic market failures. It drives the calibration models in the `Legitimate Overrides in Decentralized Protocols` paper.

| Field | Definition | Enum / Format |
| :--- | :--- | :--- |
| `incident_id` | Unique identifier for the incident mapping back to the main database. | String |
| `protocol` | The name of the protocol or system targeted by the intervention. | String |
| `date` | The date of the intervention (or start of the incident). | YYYY-MM-DD |
| `chain` | The network where the intervention took place. | String |
| `scope` | The hierarchical level of the intervention precision. | `Network`, `Asset`, `Protocol`, `Module`, `Account` |
| `authority` | The type of body that authorized/triggered the intervention. | `Signer Set`, `Delegated Body`, `Governance`, `None (expired)` |
| `time_to_detect_min` | Minutes from exploit start to first credible detection. | Float |
| `time_to_contain_min` | Minutes from detection to successful mechanism execution. | Float |
| `containment_success_pct` | Percentage of at-risk funds saved or successfully frozen/recovered. | Integer (0-100) |
| `loss_usd` | Realized loss despite (or before) intervention (USD). | Float |
| `loss_prevented_usd` | Estimated value saved directly by the intervention (USD). | Float |
| `notes` | Brief technical context on the intervention mechanism used. | String |
| `source` | Primary source URL for the intervention details (Post-mortems, Tweets). | URL |

---

## Methodology Note on Inclusion vs. Exclusion

The primary refined dataset (`lif_exploits_cleaned.csv`) applies two core filters and a final deduplication pass:
1. `is_technical == True`
2. `loss_usd >= 100,000`

This methodology **intentionally excludes** two categories of high-impact incidents:

### 1. Agency Problem Incidents (Insider Theft / Exit Scams)
> **Examples:** Africrypt ($3.6B, 2021), QuadrigaCX ($130M, 2018), BTER ($1.75M, 2015)

Per Charoenwong & Bernardi (2022), Agency Problem hacks—while only 5/30 incidents (17%)—produced **the highest single-event losses** in the decade (e.g., Africrypt: $3.6B). These are excluded from the *refined* LIF dataset because:

- **Root Cause:** Human betrayal, not code vulnerability. The "exploit" is the insider's abuse of trust, not a programmable flaw.
- **LIF Mitigation Scope:** The Legitimate Intervention Framework focuses on *code-level protections* (Ex Ante circuit breakers, Freeze First protocols). Agency problems require *governance controls* (multisig requirements, DAO oversight, key rotation) that are outside the scope of purely technical analysis.
- **Separate Research Track:** These incidents are better addressed by governance mechanism design and corporate law research (e.g., DUNA wrappers, multi-party key custody).

> [!IMPORTANT]
> **The LIF acknowledges that Agency Problems are among the most devastating attacks by dollar value.** They are included in `parsed_raw.csv` and `merged_master.csv` for total loss context, but **physically filtered out** of `lif_exploits_cleaned.csv` via the `is_technical` check.

> [!NOTE]
> **CEX hacks stay in `lif_exploits_cleaned.csv`** to maintain accurate "Total Loss" historical context, but they are excluded from "LIF-Addressable" stats via the `is_lif_relevant = False` tag.

### 2. Centralized Exchange (CEX) Hacks
> **Examples:** Bybit ($1.4B, 2025), Mt. Gox ($460M, 2014), Coincheck ($533M, 2018), KuCoin ($281M, 2020)

CEX hacks are included in the case studies for **strategic context** (they constitute 66% of early-era losses) but are not the primary focus of LIF because:

- **Centralized Custody:** CEX hacks are "Access Control" failures where the "Freeze" is a manual, centralized action by the exchange operator (or law enforcement).
- **LIF Focus:** The LIF is concerned with *decentralized protocol governance* — how to build automated, transparent, and auditable control mechanisms that work without a central operator.
- **Distinct Mitigation Path:** CEX security is addressed by traditional InfoSec (SOC 2 compliance, HSM key management, insurance funds like SAFU), not by on-chain governance mechanisms.

> [!NOTE]
> **CEX hacks like Bybit are explicitly discussed in the LIF case studies** because they demonstrate:
> 1. The scale of the threat (>$1B single event).
> 2. The industry's existing "freeze" capability (Bybit's coordination with law enforcement).
> 3. The need for LIF-style transparency in how these interventions are executed.

---

## Implications for Analysis

When citing LIF statistics in the manuscript:
- **Total Loss Context:** Use `parsed_raw.csv` or `merged_master.csv` to cite aggregate losses across all categories (including Agency Problem and CEX).
- **Technical Resilience Focus:** Use `lif_exploits_cleaned.csv` to cite losses that could have been mitigated by the LIF's technical proposals (Ex Ante, Freeze First, etc.).
- **Intervention Effectiveness:** Use `lif_intervention_metrics.csv` to cite empirical data on intervention effectiveness.

**Reference:** Charoenwong, B., & Bernardi, M. (2022). *A Decade of Cryptocurrency 'Hacks': 2011–2021*. SSRN. https://ssrn.com/abstract=3944435
