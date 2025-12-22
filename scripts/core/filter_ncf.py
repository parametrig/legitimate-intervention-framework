import csv
import os

# --- CONFIGURATION ---
# Resolve BASE_DIR relative to this script's location (scripts/core/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
BUILD_DIR = os.path.join(BASE_DIR, "data/build")
REFINED_DIR = os.path.join(BASE_DIR, "data/refined")
INPUT_CSV = os.path.join(BUILD_DIR, "merged_master.csv")
OUTPUT_CSV = os.path.join(REFINED_DIR, "ncf_exploits_final.csv")

SCHEMA = [
    "date", "protocol", "chain", "loss_usd", 
    "vector_category", "is_technical", "description", "source_file"
]

def main():
    print("Step 3: Applying High-Signal NCF Filters...")
    if not os.path.exists(INPUT_CSV):
        print("Error: merged_master.csv not found. Run deduplicate.py first.")
        return

    master = []
    with open(INPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        master = list(reader)

    # NCF High-Signal Filter Logic:
    # 1. is_technical == True (Eliminates Rugpulls, Honeypots, Agency Problems)
    # 2. loss_usd >= 100,000 (Eliminates low-value noise)
    refined = [
        r for r in master 
        if r['is_technical'].lower() == 'true' and float(r['loss_usd']) >= 100000
    ]
    
    os.makedirs(REFINED_DIR, exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(refined)
        
    print(f"Step 3 Complete: {len(refined)} high-signal exploits saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
