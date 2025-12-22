# NCF Data Dictionary

This document defines the schema used in the `ncf_exploits_final.csv` and across the research pipeline.

| Field | Definition | Enum / Format |
| :--- | :--- | :--- |
| `date` | The date the exploit occurred or was reported. | YYYY-MM-DD |
| `protocol` | The primary target of the attack. | String |
| `chain` | The network where the exploit took place. | Enum (Ethereum, BSC, SOL, etc.) |
| `loss_usd` | The total value of stolen assets in USD at the time of the hack. | Float |
| `vector_category` | The technical entry point of the exploit. | Enum (Reentrancy, Logic Flaw, CPIMP, etc.) |
| `is_technical` | Boolean flag. True = Code exploit. False = Social/Agency (Rugpull). | Boolean |
| `description` | Contextual details or contract references. | String |
| `source_file` | Reference to the raw evidence in `data/raw/`. | String |

---

## Methodology Note on Inclusion vs. Exclusion

The final refined dataset (`ncf_exploits_final.csv`) applies two filters:
1. `is_technical == True`
2. `loss_usd >= 100,000`

This methodology **intentionally excludes** two categories of high-impact incidents:

### 1. Agency Problem Incidents (Insider Theft / Exit Scams)
> **Examples:** Africrypt ($3.6B, 2021), QuadrigaCX ($130M, 2018), BTER ($1.75M, 2015)

Per Charoenwong & Bernardi (2022), Agency Problem hacks—while only 5/30 incidents (17%)—produced **the highest single-event losses** in the decade (e.g., Africrypt: $3.6B). These are excluded from the *refined* NCF dataset because:

- **Root Cause:** Human betrayal, not code vulnerability. The "exploit" is the insider's abuse of trust, not a programmable flaw.
- **NCF Mitigation Scope:** The Native Compliance Framework focuses on *code-level protections* (Ex Ante circuit breakers, Freeze First protocols). Agency problems require *governance controls* (multisig requirements, DAO oversight, key rotation) that are outside the scope of purely technical analysis.
- **Separate Research Track:** These incidents are better addressed by governance mechanism design and corporate law research (e.g., DUNA wrappers, multi-party key custody).

> [!IMPORTANT]
> **The NCF acknowledges that Agency Problems are among the most devastating attacks by dollar value.** They are included in `parsed_raw.csv` and `merged_master.csv` for total loss context, but filtered out of `ncf_exploits_final.csv` which focuses on *technical resilience*.

### 2. Centralized Exchange (CEX) Hacks
> **Examples:** Bybit ($1.4B, 2025), Mt. Gox ($460M, 2014), Coincheck ($533M, 2018), KuCoin ($281M, 2020)

CEX hacks are included in the case studies for **strategic context** (they constitute 66% of early-era losses) but are not the primary focus of NCF because:

- **Centralized Custody:** CEX hacks are "Access Control" failures where the "Freeze" is a manual, centralized action by the exchange operator (or law enforcement).
- **NCF Focus:** The NCF is concerned with *decentralized protocol governance*—how to build automated, transparent, and auditable control mechanisms that work without a central operator.
- **Distinct Mitigation Path:** CEX security is addressed by traditional InfoSec (SOC 2 compliance, HSM key management, insurance funds like SAFU), not by on-chain governance mechanisms.

> [!NOTE]
> **CEX hacks like Bybit are explicitly discussed in the NCF case studies** because they demonstrate:
> 1. The scale of the threat (>$1B single event).
> 2. The industry's existing "freeze" capability (Bybit's coordination with law enforcement).
> 3. The need for NCF-style transparency in how these interventions are executed.

---

## Implications for Analysis

When citing NCF statistics in the manuscript:
- **Total Loss Context:** Use `parsed_raw.csv` or `merged_master.csv` to cite aggregate losses across all categories (including Agency Problem and CEX).
- **Technical Resilience Focus:** Use `ncf_exploits_final.csv` to cite losses that could have been mitigated by the NCF's technical proposals (Ex Ante, Freeze First, etc.).

**Reference:** Charoenwong, B., & Bernardi, M. (2022). *A Decade of Cryptocurrency 'Hacks': 2011–2021*. SSRN. https://ssrn.com/abstract=3944435
