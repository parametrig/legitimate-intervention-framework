# NCF Chart & Visualization Requirements

This document consolidates all charts, infographics, and animated visualizations required for the NCF manuscript and website, organized by data source and narrative part.

---

## 📊 MASTER CHART INDEX

| ID | Chart Name | Source | Priority | Type | Notes |
|:---|:-----------|:-------|:---------|:-----|:------|
| C01 | Hack Type Distribution (2011-2021) | Charoenwong & Bernardi | HIGH | Pie/Donut | 66% Security, 17% Human, 17% Agency |
| C02 | The $88B Acceleration | Charoenwong & Bernardi | HIGH | Line/Area | Annual losses doubling ~2 years |
| C03 | Code is Law Breakdown | Bybit Report | HIGH | Pie/Donut | 79% No Freeze, 9.6% Active, 11.4% Potential |
| C04 | Freezing Methodology Matrix | Bybit Report | MEDIUM | Comparison | Hardcoded vs Config vs Smart Contract |
| C05 | Recovery Rate vs Intervention Speed | Case Studies | HIGH | Bar | Minutes/Hours/Days/Weeks |
| C06 | AI Exploit Revenue Acceleration | Anthropic Red | HIGH | Line (Log) | Doubling every 1.3 months |
| C07 | AI Token Cost Collapse | Anthropic Red | MEDIUM | Line | 70.2% reduction in 6 months |
| C08 | AI Cost per Scan | Anthropic Red | MEDIUM | Metric | $1.22 per contract scan |
| C09 | Freeze First Timeline | Case Studies | HIGH | Timeline | Nov 2025 events (Balancer, Moonwell) |
| C10 | 4 Architectures of Control | Bybit + Analysis | HIGH | Diagram | Hardcoded, Config, Contract, Reactive |
| C11 | Control Architecture Matrix | Bybit + Analysis | MEDIUM | Quadrant | Transparency vs Speed |
| C12 | Regulatory Timeline Evolution | Regulatory Framework | MEDIUM | Timeline | 2015-2025 paradigm shift |
| C13 | 5 Regulatory Models | Regulatory Framework | HIGH | Comparison | Centralized → Gatekeeper → RegTech → Ex Ante → Ex Post |
| C14 | Technical Evaluation Framework | Regulatory Framework | MEDIUM | Hierarchy | 4 dimensions of compliance |
| C15 | Sovereignty Risk Spectrum | _004_final | HIGH | Spectrum | Code as Law ↔ Law as Code |
| C16 | NCF Pipeline Flow | Data Pipeline | HIGH | Mermaid | Raw → Parsed → Dedupe → Filter |
| C17 | Top 10 Exploits by Loss | NCF Database | HIGH | Bar (Horizontal) | From ncf_exploits_final.csv |
| C18 | Vector Category Distribution | NCF Database | HIGH | Pie/Donut | From ncf_exploits_final.csv |
| C19 | Chain Distribution | NCF Database | MEDIUM | Bar | From ncf_exploits_final.csv |
| C20 | Losses by Year | NCF Database | HIGH | Line/Area | From ncf_exploits_final.csv |
| C21 | Institutional Deduction Flow | _004_final | MEDIUM | Flowchart | Institutional → Compliance → Control |
| C22 | Complete NCF Stack | Part 4 | HIGH | Layer Cake | L1 Consensus, L2 Safety, L3 Legal |
| C23 | Legal Entity Comparison | Part 4 | MEDIUM | Table | LLC vs Foundation vs DUNA |
| C24 | Separating Equilibrium | Part 2 | MEDIUM | Game Theory | Attacker payoff matrix |
| C25 | ZKP Architecture Flow | Part 2 | HIGH | Diagram | Prover → Proof → Verifier |
| C26 | Optimistic Freeze Flow | Part 3 | HIGH | Flowchart | Trigger → Pause → Vote → Slash/Confirm |
| C27 | Insurance Payout Loop | Part 3 | MEDIUM | Cycle | Parametrig mechanism |

---

## 📁 SOURCE 1: CHAROENWONG & BERNARDI (2011-2021)

### C01: Hack Type Distribution
**Data:**
- Security Breach: 20/30 (66%)
- Human Error: 5/30 (17%)
- Agency Problem: 5/30 (17%)

**Visual:** Donut chart with icons for each type.
**Animation:** Segments morph into icons (key, person, insider).

### C02: The $88B Acceleration
**Data:**
| Year Range | Cumulative Loss |
|------------|-----------------|
| 2011-2013  | ~$500M |
| 2014-2016  | ~$1.5B |
| 2017-2019  | ~$5B |
| 2020-2021  | ~$88B (peak) |

**Visual:** Area chart with exponential curve.
**Animation:** Rising tide filling the chart.

---

## 📁 SOURCE 2: BYBIT SECURITY REPORT (Nov 2025)

### C03: Code is Law Breakdown
**Data:**
- No Freezing: 131/166 (79%)
- Confirmed Freezing: 16/166 (9.6%)
- Potential Freezing: 19/166 (11.4%)

**Visual:** Pie chart with callouts for each segment.
**Animation:** Pie slice transition, with "21% Adapt" highlight.

### C04: Freezing Methodology Matrix
**Data:**
| Method | Chains | Transparency | Speed | Flexibility |
|--------|--------|--------------|-------|-------------|
| Hardcoded | BNB, VeChain, Chiliz, VIC, XDC | High | Slow (Hard Fork) | Low |
| Config File | Sui, Aptos, Harmony, Linea, Waves, EOS, Oasis, WAXP, Supra, HVH | Low | Medium (Node Restart) | Medium |
| Smart Contract | HECO | High | Fast (On-chain Tx) | High |

**Visual:** Comparison table with progress bars.
**Animation:** Rows slide in sequentially.

### C10: 4 Architectures of Control
**Diagram:**
```
1. HARDCODED → Protocol Layer → Requires Hard Fork
2. CONFIG-BASED → Validator Config → Requires Node Restart
3. SMART CONTRACT → Admin Contract → On-chain Tx
4. REACTIVE DEPLOYMENT → GitHub Commit → Chain Upgrade → Freeze (Sonic Model)
```
**Animation:** Each layer animates on scroll.

---

## 📁 SOURCE 3: ANTHROPIC RED TEAM (Dec 2025)

### C06: AI Exploit Revenue Acceleration
**Data (Doubling every 1.3 months):**
| Date | Cumulative Revenue |
|------|-------------------|
| Jan 2025 | ~$5K |
| Mar 2025 | ~$50K |
| Jun 2025 | ~$500K |
| Oct 2025 | ~$2M |
| Dec 2025 | ~$4.6M |

**Visual:** Log-scale line chart.
**Animation:** Line draws progressively with glowing effect.

### C07: AI Token Cost Collapse
**Data (70.2% reduction in 6 months):**
| Model | Relative Token Cost |
|-------|---------------------|
| Opus 4.0 (Jun 2025) | 100% |
| Sonnet 4.0 (Aug 2025) | 77% |
| Opus 4.5 (Oct 2025) | 50% |
| Current (Dec 2025) | 29.8% |

**Visual:** Declining step chart.
**Animation:** Bars shrink sequentially.

### C08: AI Cost per Scan (Metric Card)
**Value:** $1.22 average cost per contract scan
**Context:** 2,849 contracts scanned, 2 novel zero-days found
**Visual:** Large metric with supporting text.

---

## 📁 SOURCE 4: REGULATORY FRAMEWORK (Charoenwong et al.)

### C13: 5 Regulatory Models
**Diagram:**
```
CENTRALIZED → GATEKEEPER → REGTECH → EX ANTE AUTOMATED → EX POST DeFi
     ↓            ↓           ↓              ↓                ↓
  Gov't        Banks      Chainalysis     Code           Code + Human
```

**Data Table:**
| Approach | Fixed Costs | Variable Costs | Timing | Authority |
|----------|-------------|----------------|--------|-----------|
| Centralized | Moderate | High | Ex Post | Human |
| Gatekeeper | Moderate | Moderate | Mixed | Human |
| RegTech | High | Low | Real-time | Algorithmic + Human |
| **Ex Ante Automated** | **Very High** | **Very Low** | **Preventive** | **Algorithmic** |
| Ex Post DeFi | Very High | High | Ex Post | Human |

**Visual:** Comparison table or pyramid diagram.
**Animation:** Models stack progressively.

### C14: Technical Evaluation Framework
**Hierarchy:**
```
AUTOMATED COMPLIANCE
├── TECHNICAL EFFECTIVENESS
│   ├── Scope
│   ├── Privacy Level
│   ├── Compliance Basis
│   └── Enforcement Mode
├── STAKEHOLDER BURDENS
│   ├── User Burden
│   ├── System Burden
│   └── Regulator Burden
├── REGULATORY EFFECTIVENESS
│   ├── Auditability
│   ├── Adaptability
│   └── Revocability
└── DEPLOYMENT CONSIDERATIONS
    ├── Integration Complexity
    └── Cross-Jurisdictional Portability
```
**Visual:** Collapsible tree diagram.

---

## 📁 SOURCE 5: CASE STUDIES (Nov 2025 Events)

### C05: Recovery Rate vs Intervention Speed
**Data:**
| Intervention Time | Recovery Rate | Example |
|-------------------|---------------|---------|
| Minutes | ~100% | HECO |
| Hours | ~50-75% | Sui |
| Days | ~25-37% | BNB |
| Weeks (or No Action) | ~0% | Most exploits |

**Visual:** Bar chart with time on X-axis.
**Animation:** Bars grow with urgency gradient (green → red).

### C09: Freeze First Timeline (Nov 3-4, 2025)
**Events:**
```
Nov 3, 07:46 UTC → Balancer exploit begins ($121M)
Nov 3, 07:52 UTC → Hypernative flagged
Nov 3, 08:07 UTC → V6 pools paused ($19.3M protected)
Nov 3, 08:14 UTC → SEAL 911 contacted
Nov 3, 11:01 UTC → Recovery Mode activated
Nov 4, 05:45 UTC → Moonwell oracle exploit ($1M)
```
**Visual:** Horizontal timeline with event markers.
**Animation:** Events appear sequentially with countdown timer.

---

## 📁 SOURCE 6: NCF DATABASE (ncf_exploits_final.csv)

### C17: Top 10 Exploits by Loss
**Generate from:** `data/refined/ncf_exploits_final.csv`
**Fields:** protocol, loss_usd
**Visual:** Horizontal bar chart.

### C18: Vector Category Distribution
**Generate from:** `data/refined/ncf_exploits_final.csv`
**Fields:** vector_category, count
**Visual:** Pie/Donut chart.

### C19: Chain Distribution
**Generate from:** `data/refined/ncf_exploits_final.csv`
**Fields:** chain, count
**Visual:** Bar chart.

### C20: Losses by Year
**Generate from:** `data/refined/ncf_exploits_final.csv`
**Fields:** date (extract year), loss_usd (sum)
**Visual:** Line/Area chart.

---

## 🎨 DESIGN CONSIDERATIONS

### Color Palette (Light Mode - Active)
```
Background: #F8FAFC (Slate 50)
Primary:    #9AA6B2 (Slate 400)
Secondary:  #BCCCDC (Slate 200)
Light:      #D9EAFD (Blue 100)
Danger:     #EF4444 (Red 500)
Warning:    #F59E0B (Amber 500)
Success:    #10B981 (Emerald 500)
Text:       #475569 (Slate 600)
```

### Animation Principles (Web Phase)
1. **Reveal on scroll:** Charts appear as user scrolls into view.
2. **Progressive disclosure:** Data points animate in sequence.
3. **Hover states:** Tooltips with additional context.
4. **Looping backgrounds:** Subtle grid animations.

---

## 📋 CHART GENERATION STATUS

### ✅ Generated (24 Charts)
All charts generated via `scripts/analysis/ncf_charts.ipynb`:

| ID | Chart | Status |
|:---|:------|:-------|
| C01 | Hack Type Distribution | ✅ |
| C02 | Cumulative Losses | ✅ |
| C03 | Code is Law Breakdown | ✅ |
| C04 | Freezing Methodology | ✅ |
| C05 | Recovery vs Speed | ✅ |
| C06 | AI Exploit Acceleration | ✅ |
| C07 | AI Token Cost | ✅ |
| C08 | AI Cost Metric | ✅ |
| C09 | Freeze Timeline | ✅ |
| C10 | 4 Architectures | ✅ |
| C13 | 5 Regulatory Models | ✅ |
| C15 | Sovereignty Spectrum | ✅ |
| C17 | Top 10 Exploits | ✅ |
| C18 | Vector Distribution | ✅ |
| C19 | Chain Distribution | ✅ |
| C20 | Losses by Year | ✅ |
| C22 | NCF Stack | ✅ |
| C25 | ZKP Flow | ✅ |
| C26 | Optimistic Freeze | ✅ |
| A01 | Scatter Plot | ✅ |
| A02 | Pareto | ✅ |
| A03 | Heatmap | ✅ |
| - | Monthly Trends | ✅ |
| - | NCF Addressable | ✅ |

### 🔲 Pending (Web Phase)
- C12: Regulatory Timeline Evolution
- C16: NCF Pipeline Flow (Mermaid)
- C21: Institutional Deduction Flow
- C24: Separating Equilibrium (Game Theory)
- C27: Insurance Payout Loop

---

## 🔗 REFERENCES

- [Charoenwong & Bernardi (2022)](https://ssrn.com/abstract=3944435)
- Bybit Security Report (Nov 2025) - See `external_data` in `ncf_stats.json`
- [Anthropic Red Team (Dec 2025)](https://red.anthropic.com/2025/smart-contracts/)
- [Regulatory Framework (Charoenwong et al.)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5368708)

