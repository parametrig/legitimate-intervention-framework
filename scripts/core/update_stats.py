import json
import pandas as pd
from datetime import datetime
import os

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/refined')
STATS_FILE = os.path.join(DATA_DIR, 'lif_stats.json')
EXPLOITS_FILE = os.path.join(DATA_DIR, 'lif_exploits_cleaned.csv')

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

    # Load existing stats to preserve other sections (like intervention_metrics)
    with open(STATS_FILE, 'r') as f:
        stats = json.load(f)

    # Update summary section
    stats['summary'].update({
        'total_exploits': int(total_exploits),
        'total_loss_usd': float(total_loss),
        'lif_relevant_exploits': int(lif_relevant_exploits),
        'lif_relevant_loss_usd': float(lif_relevant_loss),
        'top_protocol': top_protocol,
        'date_range': {
            'start': start_date,
            'end': end_date
        },
        'generated_at': datetime.now().isoformat()
    })

    # Write back
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"Updated {STATS_FILE} successfully.")

if __name__ == "__main__":
    update_stats()
