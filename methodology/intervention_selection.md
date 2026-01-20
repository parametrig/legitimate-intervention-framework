# Intervention Selection Methodology

## Purpose
This document details the curation criteria used to select the **28 intervention incidents** included in the `lif_intervention_metrics.csv` dataset. Unlike the broader `lif_exploits_cleaned.csv`, which tracks all primary DeFi security exploits (>750), this dataset focuses on incidents where **on-chain emergency mechanisms** (pauses, freezes, halts) were triggered in response to either technical exploits or systemic market failures.

## Selection Criteria

To be included in the Intervention Metrics dataset, an event must meet three strict conditions:

### 1. Active On-Chain Intervention
There must be a definitive, **on-chain action** (e.g., `pause()`, `freeze()`, or validator-coordinated halt) taken by a legitimate authority.
- **Included**:
    - **Technical Exploits**: Immediate response to code vulnerabilities, flash loans, or bridge hacks.
    - **Systemic Failures**: Emergency actions taken during depegs, oracle malfunctions, or extreme market volatility (e.g., Maker PSM pause, Aave market freeze).
    - **On-Chain Regulatory Enforcement**: Native contract-level freezes (e.g., Tether/Circle blacklist) triggered by legal/compliance mandates.
- **Excluded**:
    - **CEX Freezes**: Actions taken inside centralized exchanges (off-chain) are excluded.
    - **Passive Failures**: Attacks that ceased naturally without intervention.

### 2. Classifiable Taxonomy
The intervention must neatly fit into the **Scope × Authority** matrix defined in the Legitimate Intervention Framework (LIF).
- **Scope**: Network, Asset, Protocol, Module, or Account.
- **Authority**: Signer Set (Multisig), Delegated Body (Guardian/Council), or Governance (DAO vote).

### 3. Verifiable Timing Data
We must be able to establish two timestamps to calculate `Time to Contain`:
1.  **Time of Detection ($t_0$)**: The moment the incident effectively began or was publicly noted (first malicious tx or monitoring alert).
2.  **Time of Containment ($t_c$)**: The moment the intervention became effective (e.g., the block height of the `pause()` transaction).

## Data Quality Tiers

Cases are graded based on the precision of the timing data:

| Tier | Quality | Description | Example |
|------|---------|-------------|---------|
| **Tier 1** | **On-Chain Exact** | Both detection and containment found in block explorer data. | Balancer CSPv6 (Automated Pause) |
| **Tier 2** | **Social Approximate** | Containment time verified on-chain, detection estimated from social channels. | Nomad Bridge, Euler |
| **Tier 3** | **Coarse Estimate** | Times estimated from post-mortem reports without exact tx hashes. | Harmony Bridge |

**Note**: We purposely exclude "Preventive" interventions (where Loss = $0 and no attack occurred) unless they were triggered by a *threat* of attack (e.g., whitehat rescue).

## Scope Coverage Strategy

The dataset is curated to ensure representation across the full hierarchy:

1.  **Network**: Rare, high-impact events (e.g., BNB Halt, DAO Fork).
2.  **Asset**: Standardized stablecoin freezes (Tether, Circle) vs. unique asset resets.
3.  **Protocol**: The most common DeFi intervention (Pausing).
4.  **Module**: Feature-specific toggles (e.g., disabling a specific Maker PSM).
5.  **Account**: Targeted address blacklists (Validator-coordinated L1/Infra freezes).

## Curation Changelog

- **Jan 2026**: Expanded from 20 to 28 cases to include Module-level examples (Aave, Liqwid) and recent 2025 incidents (Flow, Sonic). Purified to exclude CEX-only custodial actions.
- **Criterion Refinement**: Clarified that "Module" scope applies to interventions that disable *features* without stopping the *entire* protocol.
