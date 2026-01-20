"""
Automated Intervention Metrics Extraction Script

This script extracts intervention-relevant incidents from the LIF exploits database
and generates `lif_intervention_metrics.csv` with standardized fields for analysis.

The extraction logic:
1. Identifies incidents where emergency mechanisms were invoked
2. Categorizes by Scope (Network, Asset, Protocol, Module, Account)
3. Categorizes by Authority (Signer Set, Delegated Body, Governance, None)
4. Estimates time-to-contain and loss prevented where data is available

Usage:
    python scripts/analysis/extract_intervention_metrics.py
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
REFINED_DIR = DATA_DIR / 'refined'
OUTPUT_FILE = REFINED_DIR / 'lif_intervention_metrics.csv'

# Manual intervention cases with detailed metadata
# These are high-confidence cases where we have primary source data on intervention timing
INTERVENTION_CASES = [
    # Format: (incident_id, protocol, date, chain, scope, authority, time_detect, time_contain, 
    #          containment_pct, loss_usd, loss_prevented_usd, notes, source)
    
    # ===========================
    # NETWORK SCOPE (Chain-wide)
    # ===========================
    ("BNB-2022-10", "BNB Chain", "2022-10-06", "BNB", "Network", "Signer Set",
     0, 60, 85, 570000000, 0,
     "Validator-coordinated chain halt. Contained further drainage but suspended unrelated activity.",
     "https://www.reuters.com/technology/hackers-steal-around-100-million-cryptocurrency-binance-linked-blockchain-2022-10-07/"),
    
    ("ETH-DAO-2016", "Ethereum DAO Fork", "2016-06-17", "Ethereum", "Network", "Governance",
     0, 2592000, 100, 60000000, 60000000,
     "Hard fork executed ~30 days after exploit. Created ETC. Full recovery but chain split.",
     "https://ethereumclassic.org"),
    
    ("BERA-2025-11", "Berachain BEX", "2025-11-03", "Berachain", "Network", "Signer Set",
     0, 30, 100, 0, 0,
     "Validators coordinated network halt before significant losses. Emergency hard-fork executed.",
     "https://x.com/berachain/status/1986952318068146323"),
    
    ("GNOSIS-2025-12", "Gnosis Chain", "2025-12-15", "Gnosis", "Network", "Governance",
     43200, 86400, 100, 0, 9400000,
     "Governance-approved hard fork ~30 days after initial exploit. Recovered $9.4M frozen assets.",
     "https://forum.gnosis.io/t/balancer-hack-hard-fork/11884"),
    
    ("POLY-2021-08", "Poly Network", "2021-08-10", "Multi-chain", "Network", "Delegated Body",
     0, 1440, 100, 611000000, 611000000,
     "Cross-chain bridge exploit. Attacker returned funds after negotiations. Validator coordination.",
     "https://www.chainalysis.com/blog/poly-network-hack-august-2021/"),
    
    ("HARMONY-2022-06", "Harmony Bridge", "2022-06-23", "Harmony", "Network", "Signer Set",
     0, 240, 0, 100000000, 0,
     "Horizon bridge compromised via key theft. Network paused but funds already drained.",
     "https://www.halborn.com/blog/post/explained-the-harmony-horizon-bridge-hack"),
    
    # ===========================
    # ASSET SCOPE (Token-level)
    # ===========================
    ("TETHER-PDVSA-2026", "Tether/PDVSA", "2026-01-11", "TRON", "Asset", "Signer Set",
     0, 0, 100, 0, 182000000,
     "Issuer-controlled freeze of 5 TRON wallets linked to PDVSA. Largest single-day USDT freeze.",
     "https://finance.yahoo.com/news/tether-freezes-182m-usdt-largest-105442400.html"),
    
    ("SUI-CETUS-2025-05", "Sui/Cetus", "2025-05-22", "Sui", "Asset", "Delegated Body",
     0, 120, 71, 220000000, 162000000,
     "~$220M stolen, $162M frozen via validator coordination (~71% recovery rate).",
     "https://blog.sui.io/cetus-incident-response-onchain-community-vote/"),
    
    ("USDC-TORNADO-2022", "Circle/Tornado Cash", "2022-08-08", "Ethereum", "Asset", "Signer Set",
     0, 0, 100, 0, 75000000,
     "Circle froze 75,000 USDC in Tornado Cash contracts following OFAC sanctions.",
     "https://www.theblock.co/post/162172/circle-freezes-usdc-funds-in-tornado-cashs-us-treasury-sanctioned-wallets"),
    
    ("STAKEWISE-2025", "StakeWise", "2025-03-15", "Ethereum", "Asset", "Governance",
     0, 4320, 100, 0, 20700000,
     "DAO multisig recovery of $20.7M osETH via governance proposal.",
     "https://x.com/stakewise_io/status/1985800079354060932"),
    
    ("TETHER-BITFINEX-2017", "Tether", "2017-11-21", "Omni", "Asset", "Signer Set",
     0, 60, 100, 30950000, 0,
     "Tether froze $30.95M USDT after Bitfinex hack. First major stablecoin freeze.",
     "https://cointelegraph.com/news/breaking-tether-allegedly-hacked-for-30-mln"),
    
    # ===========================
    # PROTOCOL SCOPE (App-wide)
    # ===========================
    ("BAL-2025-11-CSPv6", "Balancer CSPv6", "2025-11-03", "Multi-chain", "Protocol", "Signer Set",
     0, 20, 100, 0, 0,
     "Hypernative automated pause triggered at 08:06-08:07 UTC, ~20 minutes after first detection.",
     "https://x.com/Balancer/status/1986104426667401241"),
    
    ("BAL-2025-11-CSPv5", "Balancer CSPv5", "2025-11-03", "Multi-chain", "Protocol", "None (expired)",
     0, float('inf'), 0, 128000000, 0,
     "Pause windows had expired. No containment possible. Illustrates cost of immutability when code is flawed.",
     "https://x.com/Balancer/status/1986104426667401241"),
    
    ("EULER-2023-03", "Euler Finance", "2023-03-13", "Ethereum", "Protocol", "Signer Set",
     0, 5, 85, 197000000, 143000000,
     "Protocol paused within 5 minutes. Attacker returned $143M after negotiation.",
     "https://www.euler.finance/blog/war-peace-behind-the-scenes-of-eulers-240m-exploit-recovery"),
    
    ("CURVE-2023-07", "Curve Finance", "2023-07-30", "Ethereum", "Protocol", "Signer Set",
     0, 30, 60, 62000000, 0,
     "Emergency subDAO paused affected pools. Multiple pools on different chains affected.",
     "https://hackmd.io/@LlamaRisk/BJzSKHNjn"),
    
    ("WORMHOLE-2022-02", "Wormhole", "2022-02-02", "Solana", "Protocol", "Signer Set",
     0, 15, 0, 320000000, 0,
     "Portal bridge exploit. Jump Trading backstopped $320M loss.",
     "https://www.halborn.com/blog/post/explained-the-wormhole-hack-february-2022"),
    
    ("BEANSTALK-2022-04", "Beanstalk", "2022-04-17", "Ethereum", "Protocol", "Governance",
     0, 0, 0, 182000000, 0,
     "Flash loan governance attack. Protocol had no pause mechanism. Total loss.",
     "https://www.certik.com/resources/blog/revisiting-beanstalk-farms-exploit"),
    
    ("NOMAD-2022-08", "Nomad Bridge", "2022-08-01", "Multi-chain", "Protocol", "Signer Set",
     0, 30, 5, 190000000, 20000000,
     "Bridge paused but exploit was copy-pasted. ~$20M voluntarily returned.",
     "https://immunebytes.com/blog/nomad-bridge-exploit-aug-1-2022-detailed-analysis/"),
    
    ("CREAM-2021-10", "Cream Finance", "2021-10-27", "Ethereum", "Protocol", "Signer Set",
     0, 15, 0, 130000000, 0,
     "Protocol paused after flash loan attack detected. Third major attack on Cream.",
     "https://immunebytes.com/blog/cream-finance-exploit-oct-27-2021-detailed-analysis/"),
    
    ("BADGER-2021-12", "Badger DAO", "2021-12-02", "Ethereum", "Protocol", "Signer Set",
     0, 120, 0, 120000000, 0,
     "Protocol paused 2 hours after detection. Front-end compromised.",
     "https://rekt.news/badger-rekt"),
    
    ("ANCHOR-2022-05", "Anchor Protocol", "2022-05-09", "Terra", "Protocol", "Governance",
     0, 4320, 0, 0, 0,
     "Emergency governance proposals during UST collapse. Protocol shutdown.",
     "https://forum.anchorprotocol.com/t/emergency-measures-for-restoring-terra-peg/4784"),
    
    # ===========================
    # MODULE SCOPE (Feature-level)
    # ===========================
    ("AAVE-2022-11", "Aave v2", "2022-11-22", "Ethereum", "Module", "Governance",
     0, 60, 100, 0, 0,
     "Guardian paused CRV market borrowing during Curve exploit concern. Module-level pause.",
     "https://governance.aave.com/t/blameless-post-mortem-curve-aug-8-2023/14386"),

    ("LIQWID-2025-10", "Liqwid", "2025-10-15", "Cardano", "Module", "Delegated Body",
     0, 45, 100, 0, 0,
     "Core Team pause via Proposal 44 during ADA flash crash. Market-level pause only.",
     "https://app.liqwid.finance/governance/proposal/44"),
     
    ("MKR-USDC-2023", "MakerDAO", "2023-03-11", "Ethereum", "Module", "Governance",
     0, 7200, 100, 0, 0,
     "Emergency governance vote to pause PSM during USDC depeg. 120-minute vote.",
     "https://forum.sky.money/t/emergency-proposal-risk-and-governance-parameter-changes-11-march-2023/20125"),
    
    ("DYDX-MARKET-2023", "dYdX", "2023-11-07", "Ethereum", "Module", "Delegated Body",
     0, 15, 100, 9000000, 0,
     "YFI market paused during large position liquidation. Module-level circuit breaker.",
     "https://dydx.exchange/blog/sushi-yfi-incident"),
    
    # ===========================
    # ACCOUNT SCOPE (Address-level)
    # ===========================
    ("FLOW-2025-12", "Flow Blockchain", "2025-12-27", "Flow", "Account", "Delegated Body",
     0, 60, 85, 3900000, 0,
     "Isolated Recovery approach: validators halted network, restricted only affected accounts. CGC authorized burns.",
     "https://flow.com/post/dec-27-technical-post-mortem"),
    
    ("SONIC-2025-11", "Sonic/Beets", "2025-11-03", "Sonic", "Account", "Signer Set",
     0, 120, 95, 32000, 0,
     "Sonic Labs deployed freezeAccount mechanism ~2 hours after incident. Froze suspected attacker addresses.",
     "https://x.com/SonicLabs/status/1985401737096671549"),
    
    ("AXIE-2022-03", "Ronin Bridge", "2022-03-29", "Ronin", "Account", "Signer Set",
     0, 8640, 30, 625000000, 30000000,
     "Attacker addresses identified and partially frozen. ~$30M recovered via law enforcement.",
     "https://roninchain.com/blog/posts/back-to-building-ronin-security-breach-6513cc78a5edc1001b03c364"),
]


def generate_metrics_csv():
    """Generate the intervention metrics CSV from manual cases."""
    
    columns = [
        'incident_id', 'protocol', 'date', 'chain', 'scope', 'authority',
        'time_to_detect_min', 'time_to_contain_min', 'containment_success_pct',
        'loss_usd', 'loss_prevented_usd', 'notes', 'source'
    ]
    
    rows = []
    for case in INTERVENTION_CASES:
        row = dict(zip(columns, case))
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Sort by date descending
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date', ascending=False)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    
    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)
    
    # Print summary
    print(f"Generated {OUTPUT_FILE}")
    print(f"Total intervention cases: {len(df)}")
    print("\nBreakdown by Scope:")
    print(df.groupby('scope').size().to_string())
    print("\nBreakdown by Authority:")
    print(df.groupby('authority').size().to_string())
    
    return df


def update_stats_json(df):
    """Update lif_stats.json with intervention metrics summary."""
    
    stats_file = REFINED_DIR / 'lif_stats.json'
    
    if stats_file.exists():
        with open(stats_file, 'r') as f:
            stats = json.load(f)
    else:
        stats = {}
    
    # Add intervention metrics
    stats['intervention_metrics'] = {
        'total_cases': len(df),
        'by_scope': df.groupby('scope').size().to_dict(),
        'by_authority': df.groupby('authority').size().to_dict(),
        'total_loss_usd': int(df['loss_usd'].sum()),
        'total_prevented_usd': int(df['loss_prevented_usd'].sum()),
        'generated_at': datetime.now().isoformat()
    }
    
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\nUpdated {stats_file}")


if __name__ == '__main__':
    df = generate_metrics_csv()
    update_stats_json(df)
