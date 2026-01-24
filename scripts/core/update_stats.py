import json
import pandas as pd
from datetime import datetime
import os

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/refined')
STATS_FILE = os.path.join(DATA_DIR, 'lif_stats.json')
EXPLOITS_FILE = os.path.join(DATA_DIR, 'lif_exploits_final.csv')
INTERVENTION_FILE = os.path.join(DATA_DIR, 'lif_intervention_metrics.csv')

def update_stats():
    print(f"Reading data from {EXPLOITS_FILE}...")
    df = pd.read_csv(EXPLOITS_FILE)

    # Calculate summaries
    total_exploits = len(df)
    total_loss = df['loss_usd'].sum()
    
    # LIF Relevant stats
    lif_df = df[df['is_lif_relevant'] == True]
    lif_relevant_exploits = len(lif_df)
    lif_relevant_loss = lif_df['loss_usd'].sum()

    # Date range
    df['date'] = pd.to_datetime(df['date'])
    start_date = df['date'].min().strftime('%Y-%m-%d')
    end_date = df['date'].max().strftime('%Y-%m-%d')

    # Top Protocol (by total loss)
    top_protocol = df.groupby('protocol')['loss_usd'].sum().idxmax()

    print(f"Calculated Stats:")
    print(f"Total Exploits: {total_exploits}")
    print(f"Total Loss: ${total_loss:,.2f}")
    print(f"LIF Relevant: {lif_relevant_exploits}")
    print(f"Date Range: {start_date} to {end_date}")

    # Top 10 exploits by loss
    top_10 = df.nlargest(10, 'loss_usd')[['protocol', 'loss_usd', 'date', 'vector_category', 'chain', 'is_lif_relevant']]
    top_10_list = []
    for _, row in top_10.iterrows():
        top_10_list.append({
            "protocol": row['protocol'],
            "loss_usd": float(row['loss_usd']),
            "date": f"{pd.to_datetime(row['date']).isoformat()}T00:00:00",
            "vector_category": row['vector_category'],
            "chain": row['chain'],
            "is_lif_relevant": bool(row['is_lif_relevant'])
        })

    # Yearly losses
    df['year'] = pd.to_datetime(df['date']).dt.year
    yearly_losses = df.groupby('year')['loss_usd'].sum().to_dict()
    yearly_losses = {str(k): float(v) for k, v in sorted(yearly_losses.items())}

    # Cumulative losses
    cumulative = {}
    running_total = 0
    for year in sorted(yearly_losses.keys()):
        running_total += yearly_losses[year]
        cumulative[year] = float(running_total)

    # Vector distribution
    vector_dist = df['vector_category'].value_counts().to_dict()

    # Chain distribution (by total loss)
    chain_losses = df.groupby('chain')['loss_usd'].sum().sort_values(ascending=False).to_dict()
    chain_losses = {str(k): float(v) for k, v in chain_losses.items()}

    # Intervention metrics
    try:
        intervention_df = pd.read_csv(INTERVENTION_FILE)
        intervention_scope = intervention_df['scope'].value_counts().to_dict()
        intervention_authority = intervention_df['authority'].value_counts().to_dict()
        intervention_loss_total = intervention_df['loss_usd'].fillna(0).sum()
        intervention_prevented_total = intervention_df['loss_prevented_usd'].fillna(0).sum()
        intervention_cases = len(intervention_df)
    except:
        intervention_scope = {}
        intervention_authority = {}
        intervention_loss_total = 0
        intervention_prevented_total = 0
        intervention_cases = 0

    # Generate fresh stats
    stats = {
        "summary": {
            "total_exploits": int(total_exploits),
            "total_loss_usd": float(total_loss),
            "lif_relevant_exploits": int(lif_relevant_exploits),
            "lif_relevant_loss_usd": float(lif_relevant_loss),
            "top_protocol": top_protocol,
            "date_range": {
                "start": start_date,
                "end": end_date
            },
            "generated_at": datetime.now().isoformat()
        },
        "top_10_exploits": top_10_list,
        "yearly_losses": yearly_losses,
        "cumulative_losses": cumulative,
        "vector_distribution": vector_dist,
        "chain_distribution": chain_losses,
        "intervention_metrics": {
            "total_cases": intervention_cases,
            "by_scope": intervention_scope,
            "by_authority": intervention_authority,
            "total_loss_usd": float(intervention_loss_total),
            "total_prevented_usd": float(intervention_prevented_total),
            "generated_at": datetime.now().isoformat()
        },
        "data_sources": [
            "charoenwong_bernardi_table.txt",
            "rekt_database_raw.txt", 
            "rekt_news_extra.txt",
            "defihacklabs_incidents.json",
            "manual_q4_2025_urls"
        ]
    }

    # Write fresh stats
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"Generated fresh {STATS_FILE} successfully.")

if __name__ == "__main__":
    update_stats()
