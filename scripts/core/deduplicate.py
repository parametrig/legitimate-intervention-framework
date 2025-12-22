import csv
import os

# --- CONFIGURATION ---
# Resolve BASE_DIR relative to this script's location (scripts/core/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
BUILD_DIR = os.path.join(BASE_DIR, "data/build")
INPUT_CSV = os.path.join(BUILD_DIR, "parsed_raw.csv")
OUTPUT_CSV = os.path.join(BUILD_DIR, "merged_master.csv")

SCHEMA = [
    "date", "protocol", "chain", "loss_usd", 
    "vector_category", "is_technical", "description", "source_file"
]

def main():
    print("Step 2: Deduplicating records...")
    if not os.path.exists(INPUT_CSV):
        print("Error: parsed_raw.csv not found. Run parse_sources.py first.")
        return

    master = []
    with open(INPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        master = list(reader)

    unique_items = {}
    for item in master:
        # Key: "Date|Protocol" (normalized)
        # Using first 5 chars for protocol to handle slight name variations (fuzzier dedupe)
        protocol_slug = item['protocol'].lower().replace(" ", "")[:5]
        key = f"{item['date']}|{protocol_slug}"
        
        # If new item has higher loss, prefer it
        if key not in unique_items or float(item['loss_usd']) > float(unique_items[key]['loss_usd']):
            unique_items[key] = item
            
    merged = list(unique_items.values())
    merged.sort(key=lambda x: x['date'], reverse=True)

    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(merged)
    print(f"Step 2 Complete: {len(merged)} unique records saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
