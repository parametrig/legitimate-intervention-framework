# LIF Case Studies: Historical & Recent Exploits (2020-2025)

> [!NOTE]
> **CEX vs. DEX Distinction:** While the database includes CEX hacks (Upbit, DMM Bitcoin, WazirX) for total loss context, the LIF primarily addresses **decentralized protocol governance**. CEX incidents are usually "Access Control" (private key) failures where the "Freeze" is a manual, centralized action. LIF focuses on how to automate or govern these powers in a decentralized stack.

> [!IMPORTANT]
> **On Agency Problem Exclusions:** Per Charoenwong & Bernardi (2022), "Agency Problem" hacks (insider theft, exit scams) produced the **highest single-event losses** in the 2011-2021 decade e.g., Africrypt ($3.6B). These are documented here for context but are **not the primary focus of LIF's technical proposals**. Insider betrayal requires governance controls (multisig, DAO oversight) rather than code-level circuit breakers. See `methodology/data_dictionary.md` for the full rationale.

---

## 🔒 FREEZE SUCCESS CASES (Critical for LIF Thesis)

### Upbit (Nov 27, 2025) - $36M → $8M Recovered
**Chain:** Solana | **Type:** Hot Wallet Compromise

- **Key LIF Data:** ~2.3B KRW (~$1.7M) of LAYER tokens **frozen on-chain**
- **Recovery Method:** Coordination with Solayer project for on-chain freeze
- **Exchange Response:** Upbit committed to **cover all losses with own assets**
- **Tokens Affected:** 24 Solana-based tokens (SOL, USDC, BONK, JUP, RAY, RENDER, ORCA, PYTH, TRUMP, LAYER, ME, MEW, DRIFT, PENGU)
- **Timeline:** Detected 4:42 AM KST → Immediate suspension of Solana deposits/withdrawals
- **LIF Relevance:** Shows **institutional coordination + on-chain freeze** working together

### Beets/Balancer V2 (Nov 3, 2025) - $3M Frozen
**Chain:** Sonic | **Type:** Balancer V2 Pool Vulnerability

- **Key LIF Data:** Sonic Labs deployed **emergency safety mechanism ahead of scheduled upgrade**
- **Frozen Wallets:**
  - `0xf19fd5c683a958ce9210948858b80d433f6bfae2`
  - `0x045371528a01071d6e5c934d42d641fd3cbe941c`
- **Pools Affected:** stS/S and stS/wOS (Balancer V2)
- **Unaffected:** V3 pools, stS LST token
- **LIF Relevance:** **"Freeze First" protocol in action** - rapid coordination between Beets and Sonic

### Astera/Linea (Oct 9, 2025) - $822K → $440K Rescued (54%)
**Chain:** Linea | **Type:** Liquidity Index Inflation Attack

- **Key LIF Data:** Linea security team **froze 46% of stolen funds**
- **Attack Details:** 5,600 flash loans across 112 transactions to inflate liquidity index 154x
- **Affected Minipools:**
  - `0x52280ea8979d52033e14df086f4df555a258beb4`
  - `0x65559abecd1227cc1779f500453da1f9fcadd928`
  - `0x0bafb30b72925e6d53f4d0a089be1cefbb5e3401`
- **LIF Relevance:** L2 security teams can act as **"Sentinels"** in the Freeze First model

---

## 🔄 RECOVERY & NEGOTIATION (Post-Ex Success)

### Euler Finance (March 13, 2023) - $196M → $180M+ Recovered
**Chain:** Ethereum | **Type:** Flash Loan / Donation Bug

- **Key LIF Data:** Attacker exploited a logic flaw in the `donateToReserves` function.
- **Recovery Method:** **Negotiation & Social Pressure.** After a series of on-chain messages, the attacker returned almost all funds.
- **LIF Relevance:** Highlights the **"Post-Ex" recovery** phase. While a freeze wasn't possible mid-attack, the transparency of the ledger enabled the social/legal pressure that led to recovery.

---

## ORACLE FAILURES (Supports "Ex Ante" Argument)

### Truebit (Jan 8, 2026) - $26.5M Lost
**Chain:** Ethereum | **Type:** Integer Overflow

- **Root Cause:** Integer overflow in `getPurchasePrice()` function caused numerator to exceed 2^256, rounding to zero.
- **Attack Method:** Attacker minted hundreds of millions of TRU tokens for 0 ETH cost, then sold them.
- **Impact:** Drained 8,535 ETH from contract `0x764C64b2A09b09Acb100B80d8c505Aa6a0302EF2`. TRU token dropped 100%.
- **Attribution:** Same attacker hit Sparkle protocol 12 days earlier.
- **LIF Relevance:** Classic **arithmetic vulnerability** that circuit breakers on minting rate could have detected.

### Yo Yield (Jan 13, 2026) - $3.73M Lost
**Chain:** Ethereum | **Type:** Slippage / Operational Error

- **Root Cause:** 3.84M GHO was swapped for only 112K USDC during a Vault operation (97% value loss).
- **Attack Type:** Not a hack—but an operational failure caused by inadequate slippage protection.
- **LIF Relevance:** **"Ex Ante" circuit breakers** on price deviation could have halted the transaction.

### Fusion/IPOR (Jan 6, 2026) - $336K Lost
**Chain:** Arbitrum | **Type:** EIP-7702 Delegation Exploit

- **Root Cause:** Legacy vault (490 days old) had missing fuse validation. Attacker used EIP-7702 to hijack admin identity.
- **Attack Method:** Injected malicious fuse via `configureInstantWithdrawalFuses`, drained USDC.
- **Laundering:** $267K bridged to Ethereum and deposited into Tornado Cash.
- **Response:** IPOR DAO providing full reimbursement from treasury.
- **LIF Relevance:** **New attack surface** from EIP-7702 delegation. Highlights need for legacy contract audits.

### Unleash Protocol (Dec 30, 2025) - $3.9M Lost
**Chain:** Story Protocol | **Type:** Multisig Governance Compromise

- **Root Cause:** Attacker obtained administrative control through multisig system.
- **Attack Method:** Executed unauthorized contract upgrade enabling asset withdrawals.
- **Tokens Stolen:** WIP, USDC, WETH, stIP, vIP.
- **Laundering:** 1337.1 ETH deposited into Tornado Cash.
- **Response:** Protocol paused all operations, engaged forensic investigators.
- **LIF Relevance:** **Multisig governance attacks** require multi-day timelocks and social review.

---

### Moonwell (Nov 4, 2025) - $3.7M Lost
**Chain:** Base | **Type:** Chainlink Oracle Malfunction

- **Root Cause:** wrsETH/ETH oracle reported **1 wrsETH = 1,649,934.60732 ETH** (~$5.8B)
- **Attack Speed:** 12 transactions in **26 seconds** after oracle failure
- **Attacker:** `0x6997a8c804642ae2de16d7b8ff09565a5d5658ff`
- **Response:** Zeroed supply/borrow caps for wrsETH within minutes
- **LIF Relevance:** "Ex Ante" circuit breakers on oracle price bounds could have prevented this

### Typus Finance (Oct 15, 2025) - $3.44M Lost
**Chain:** Sui | **Type:** Missing Oracle Authorization

- **Root Cause:** Missing `assert` check in `update_v2` function allowed unauthorized price updates
- **Attack Window:** 34 minutes (13:05 → 13:39 UTC)
- **Assets Stolen:** 588,357.9 SUI, 1,604,034.7 USDC, 0.6 xBTC, 32.227 suiETH
- **LIF Relevance:** Oracle module was **not in audit scope** - highlights need for comprehensive coverage

### BonqDAO (Feb 2, 2023) - $120M Lost
**Chain:** Polygon | **Type:** Oracle Price Manipulation

- **Root Cause:** Attacker manipulated the Tellor oracle price of ALBT to mint massive amounts of BEUR.
- **LIF Relevance:** Classic **Oracle Malfunction** that could have been mitigated by a "Freeze First" circuit breaker on price deviation.

### Terra/LUNA (May 8, 2022) - $40B Systemic Collapse
**Chain:** LUNC | **Type:** Stablecoin Depeg / Death Spiral

- **Root Cause:** UST lost its $1 peg, triggering a hyper-inflationary death spiral for LUNA.
- **LIF Relevance:** The ultimate **"Systemic Risk"** case. While not a "hack" in the traditional sense, it highlights the need for **automated circuit breakers** on stablecoin minting/redemption during extreme volatility.

---

## 💸 SYSTEMIC/CASCADE FAILURES

### Stream Finance (Nov 4, 2025) - $93M + $285M Cascade
**Chain:** Ethereum | **Type:** External Fund Manager Loss

- **Direct Loss:** $93M
- **Cascade Damage:** $285M across DeFi ecosystem
- **Debt Distribution:**
  - TelosC: $123.6M
  - Elixir: $68M
  - MEV Capital: $25.4M
  - Varlamore: $19.1M
  - Re7: $14.2M
- **xUSD Collapse:** $1.3 → $0.3
- **Ripple Effects:**
  - Elixir discontinued deUSD support
  - Stable Labs' USDX lost peg (60%+ drop)
- **LIF Relevance:** **"Contagion Risk"** - lack of circuit breakers amplified damage

---

## 🔑 PRIVATE KEY / ACCESS CONTROL FAILURES

### Hyperliquid User (Oct 10, 2025) - $21M Lost
**Chain:** HyperEVM | **Type:** Private Key Leak

- **Method:** Key likely leaked via phishing/malware
- **Stolen:** $17.75M DAI + $3.11M MSYRUPUSDP
- **LIF Relevance:** No smart contract flaw - pure key management failure

### EIP-7702 Delegation (Oct 3, 2025) - $336K Lost
**Chain:** BSC | **Type:** First EIP-7702 Exploit

- **Root Cause:** `pancakeV3SwapCallback()` function had **no access controls**
- **LIF Relevance:** **New attack surface** from delegation standards - requires updated security models

### Nomad Bridge (Aug 1, 2022) - $190M Lost
**Chain:** Ethereum/Multiple | **Type:** Logic Flaw / "Copy-Paste" Exploit

- **Root Cause:** A misconfiguration allowed anyone to replicate the attacker's transaction by simply replacing the address.
- **LIF Relevance:** **Mass Replicability.** This was a "decentralized" looting where hundreds of people participated. Shows the need for **network-level freezes** when an exploit becomes public.

### Beanstalk (April 18, 2022) - $181M Lost
**Chain:** Ethereum | **Type:** Flash Loan / Governance Attack

- **Root Cause:** Attacker used a flash loan to gain majority voting power and passed a malicious proposal to drain the treasury.
- **LIF Relevance:** **Governance Attack.** LIF's "Freeze First" model includes **governance delays** specifically to prevent flash-loan-voted proposals from executing instantly.

### DIMO Network (Nov 7, 2025) - $40K Lost → Recovered
**Chain:** Ethereum | **Type:** Developer Key Compromise

- **Method:** Bridge deployer key compromised
- **Tokens Stolen:** 30M DIMO (3% of supply)
- **Recovery:** Proxy changed back + ownership transferred to multisig `0xCED3c922200559128930180d3f0bfFd4d9f4F123`
- **LIF Relevance:** Shows **"Admin Key Risk"** but also **recoverable via proxy upgrades**

### Multichain (July 6, 2023) - $231M Lost
**Chain:** Multiple | **Type:** Access Control / Centralization Failure

- **Root Cause:** CEO arrested; MPC keys were centralized and compromised.
- **LIF Relevance:** The **Ultimate Centralization Risk.** LIF argues for "Legitimate Intervention" that is **decentralized** and not dependent on a single individual's keys.

### KyberSwap (Nov 22, 2023) - $45M Lost
**Chain:** Multiple | **Type:** Flash Loan / Tick Manipulation

- **Root Cause:** "Infinite money glitch" via complex tick manipulation in concentrated liquidity pools.
- **LIF Relevance:** **AI Replicability.** This was a highly complex "math" exploit that AI agents are increasingly capable of finding (and eventually, preventing).

### Ronin Bridge (March 29, 2022) - $625M Lost
**Chain:** Ronin | **Type:** Access Control (Validator Compromise)

- **Root Cause:** Sky Mavis's validator nodes were compromised via social engineering.
- **LIF Relevance:** **Validator-Level Security.** Shows that even "decentralized" bridges often rely on a small number of validators. LIF argues for **cross-chain monitoring** that can trigger freezes if bridge outflows exceed normal bounds.

### Wormhole (Feb 2, 2022) - $326M Lost
**Chain:** Solana/Multiple | **Type:** Logic Flaw (Signature Verification)

- **Root Cause:** Attacker bypassed signature verification to mint 120k wETH on Solana.
- **LIF Relevance:** **Bridge Security.** Highlights the critical nature of cross-chain message verification.

---

## 🛡️ DEPLOYMENT VERIFICATION (The CPIMP Vector)

### Palm USD (USPD) (Dec 4, 2025) - $1.05M Lost
**Chain:** Ethereum | **Type:** CPIMP (Front-running Initialization)

- **Root Cause:** 24-second gap between proxy deployment and initialization allowed an attacker to front-run the `initialize` call.
- **Mechanism:** Attacker installed a "shadow proxy" that forwarded calls to the real implementation but gave them admin rights. They waited 78 days before upgrading to a malicious implementation to mint 98M unbacked tokens.
- **LIF Relevance:** **Deployment Verification.** LIF argues that security audits must extend to the **live deployment state**. A "Freeze First" sentinel could have flagged the unauthorized initialization within seconds of deployment.
- **LIF Mitigation:**
    - **Deployment Gate:** LIF-integrated deployment scripts would require atomic "Deploy-and-Init" transactions.
    - **State Sentinel:** A State Sentinel would detect a non-authorized address holding "Guardian" roles immediately upon initialization and trigger an automated freeze.

### Pump.fun (May 16, 2024) - $2M Lost → Restored
**Chain:** Solana | **Type:** Flash Loan / Insider Attack

- **Key LIF Data:** Exploited by a **former employee** with a private key.
- **Mechanism:** Attacker used flash loans from MarginFi to withdraw liquidity meant for Raydium.
- **Response:** Team managing to **upgrade contracts** to prevent further damage.
- **Recovery:** Full liquidity **restitution within 24 hours** from team funds.
- **LIF Relevance:** Highlights the **"Insider Threat"** and how rapid contract upgrades (a form of freeze/intervention) can limit damage.

---

## 📊 RUGPULLS & EXIT SCAMS

| Date | Protocol | Loss | Notes |
|------|----------|------|-------|
| Sep 26 | Hypervault | $3.6M | 752 ETH to Tornado Cash |
| Oct 10 | OracleBNB | $80K | Token crashed 95% |
| Sep 9 | Aqua (Solana) | $4.65M | Exit scam |
| Dec 10 | MUBARA | $55K | Yi He WeChat hijack pump-and-dump |

---

## 🛡️ COMPENSATION COMMITMENTS

| Protocol | Date | Loss | Response |
|----------|------|------|----------|
| WaveX | Dec 6 | $430K | "Fully compensating all user losses" |
| Sharwa Finance | Oct 20 | $147K | 100% refund commitment |
| Upbit | Nov 27 | $36M | Covered with own reserves |
| Abracadabra | Oct 4 | $1.7M | Bought back MIM to cover losses |

---

## 🔗 Key Addresses for Analysis

**Frozen/Seized:**
- Beets attacker: `0xf19fd5c683a958ce9210948858b80d433f6bfae2`

**Flash Loan Exploits:**
- Yearn (Dec 17): `0xcAca279dff5110EFa61091BEcF577911a2fa4cC3`
- Moonwell (Nov 4): `0x6997a8c804642ae2de16d7b8ff09565a5d5658ff`

**Rugpull Wallets:**
- Hypervault: Bridged to ETH → 752 ETH to Tornado Cash

---

## 💡 THEORETICAL EXPANSIONS (The "Sentinel" Model)

### 1. Insurer-as-Sentinel (Tx Hash Insurance)
**Concept:** Insurers and the network can "insure" specific transaction hashes.
- **Mechanism:** Projects buy into an insurance pool. Insurers, having "skin in the game," are incentivized to perform deep, real-time reviews of transactions.
- **Incentive:** If a hack occurs, the insurer pays. Therefore, they build/deploy sophisticated monitoring to **intercept** suspicious transactions or those exceeding a specific value threshold.
- **LIF Integration:** This moves the "Freeze" power from a potentially slow DAO to a motivated, professional "Sentinel" (the insurer).

### 2. Parametric Safety Net (The "Oops" Fund)
**Concept:** Using Parametric Insurance to hedge against **False Positives** in the "Freeze First" model.
- **The Problem:** A "Freeze First" action might be a poor judgment call, causing lost opportunity or utility for users.
- **The Solution:** If a freeze is triggered and later proven to be a "False Positive" (via a secondary oracle or governance review), a **parametric insurance policy** is automatically invoked.
- **Payout:** Users are immediately compensated for the downtime/inconvenience without needing a manual claims process.
- **LIF Relevance:** This reduces the "political cost" of freezing, making governance more willing to act decisively in ambiguous situations.

### 3. Stablecoin Chain Resilience (The "Multi-Stable" Future)
**Concept:** Preparing for the rise of multiple stablecoins across specialized "Stablecoin Chains."
- **The Problem:** As stablecoins proliferate across dozens of chains (L2s, AppChains), the surface area for depegs and liquidity drains increases exponentially.
- **The LIF Solution:**
    - **Cross-Chain Circuit Breakers:** LIF proposes a standard where stablecoin issuers can trigger a "Global Pause" across all supported chains if a systemic depeg is detected on one.
    - **Native Minting Limits:** Protocols on "Stablecoin Chains" should have native, hard-coded minting caps that require a multi-day governance delay to increase, preventing USPD-style "infinite mint" exploits.
    - **Interoperability Sentinels:** Bridges between stablecoin chains must act as active sentinels, verifying the "backing" of a stablecoin before allowing cross-chain transfers.

---

## 📚 SOURCES & ATTRIBUTION

This database and the associated case studies are compiled from the following primary security research sources. Proper attribution will be maintained in all LIF publications and the final manuscript.

1.  **De.Fi Rekt Database:** [rekt.news](https://rekt.news) - Primary source for incident details, loss amounts, and post-mortem analysis (2022-2025).
2.  **DeFiHackLabs:** [GitHub Repository](https://github.com/SunWeb3Sec/DeFiHackLabs) - Comprehensive open-source repository for smart contract exploit reproduction and historical data.
3.  **Charoenwong & Bernardi (2022):** *"The Decade of Hacks"* - Foundational research paper providing the 2011-2021 historical baseline.
4.  **SlowMist Hacked:** [slowmist.io](https://hacked.slowmist.io) - Secondary verification for major ecosystem incidents and cross-chain bridge exploits.
5.  **PeckShield Alert:** [Twitter/X](https://twitter.com/PeckShieldAlert) - Real-time verification and technical root cause analysis for 2024-2025 incidents.
6.  **Chainalysis:** [2024 Crypto Crime Report](https://www.chainalysis.com/blog/2024-crypto-crime-report-introduction/) - Macro-level data on total value stolen and laundering patterns.
