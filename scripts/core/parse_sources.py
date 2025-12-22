import csv
import json
import re
import os
from datetime import datetime

# --- CONFIGURATION ---
# Resolve BASE_DIR relative to this script's location (scripts/core/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
RAW_DIR = os.path.join(BASE_DIR, "data/raw")
BUILD_DIR = os.path.join(BASE_DIR, "data/build")
OUTPUT_CSV = os.path.join(BUILD_DIR, "parsed_raw.csv")

# Standard Schema for internal processing
SCHEMA = [
    "date", "protocol", "chain", "loss_usd", 
    "vector_category", "is_technical", "description", "source_file"
]

def clean_usd(val):
    if not val: return 0.0
    v = str(val).replace('$', '').replace(',', '').strip()
    try:
        return float(v)
    except ValueError:
        return 0.0

def parse_date(date_str):
    if not date_str or str(date_str).lower() == "unknown":
        return ""
    if len(str(date_str)) == 8 and str(date_str).isdigit():
        s = str(date_str)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', str(date_str))
    if match:
        m, d, y = match.groups()
        return f"{y}-{int(m):02d}-{int(d):02d}"
    months = ["january", "february", "march", "april", "may", "june", 
              "july", "august", "september", "october", "november", "december",
              "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    m_lower = str(date_str).lower()
    for i, m_name in enumerate(months):
        if m_name in m_lower:
            year_match = re.search(r'(\d{4})', str(date_str))
            if year_match:
                m_num = (i % 12) + 1
                # Try to find a day
                # Remove the year from the string to avoid matching year digits as day
                day_pool = str(date_str).replace(year_match.group(1), "")
                day_match = re.search(r'(\d{1,2})', day_pool)
                if day_match:
                    return f"{year_match.group(1)}-{m_num:02d}-{int(day_match.group(1)):02d}"
                return f"{year_match.group(1)}-{m_num:02d}-01"
    try:
        s = str(date_str)[:10]
        if re.match(r'\d{4}-\d{2}-\d{2}', s):
            return s
    except:
        pass
    return str(date_str)

def parse_charoenwong(file_path):
    incidents = []
    if not os.path.exists(file_path): return incidents
    with open(file_path, 'r') as f:
        lines = f.readlines()
    current_buffer = []
    table_started = False
    def process_buffer(buffer_lines):
        full_text = " ".join([l.strip() for l in buffer_lines if l.strip()])
        match = re.match(r'^(\d+)\s+([A-Za-z]+\s+\d{4})\s+(.*)', full_text)
        if not match: return None
        idx, date_str, rest = match.groups()
        types = ["Security Breach", "Human Error", "Agency Problem"]
        vector = "Other"
        for t in types:
            if t in rest:
                vector = t
                rest = rest.replace(t, "").strip()
                break
        found_amounts = re.findall(r'[\d,]{2,}', rest)
        usd_val = clean_usd(found_amounts[-1]) if found_amounts else 0.0
        protocol = rest.split(' ')[0]
        if protocol.lower() == "mt." and "gox" in rest.lower(): protocol = "Mt. Gox"
        elif protocol.lower() == "mt.gox": protocol = "Mt. Gox"
        return {
            "date": parse_date(date_str), "protocol": protocol.strip(),
            "description": full_text, "chain": "Unknown", "loss_usd": usd_val,
            "vector_category": vector, "is_technical": vector == "Security Breach",
            "source_file": os.path.basename(file_path)
        }
    for line in lines:
        if "No. Date Impetus" in line:
            table_started = True
            continue
        if not table_started: continue
        if "Total Amount Stolen" in line: break
        if re.match(r'^\d+\s+[A-Za-z]+\s+\d{4}\s+', line):
            if current_buffer:
                row = process_buffer(current_buffer)
                if row: incidents.append(row)
            current_buffer = [line]
        else:
            if current_buffer: current_buffer.append(line)
    if current_buffer:
        row = process_buffer(current_buffer)
        if row: incidents.append(row)
    return incidents

def parse_rekt_database(file_path):
    """Parses the consolidated De.Fi Rekt database file."""
    incidents = []
    if not os.path.exists(file_path): return incidents
    with open(file_path, 'r') as f:
        content = f.read()
        blocks = content.split('logo\n')
        for block in blocks:
            lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
            if len(lines) < 4: continue
            item = {
                "date": "", "protocol": lines[0], "chain": "Other",
                "loss_usd": 0.0, "vector_category": "Other",
                "is_technical": True, "description": " ".join(lines),
                "source_file": os.path.basename(file_path)
            }
            for l in lines:
                if l.startswith('$'): item["loss_usd"] = clean_usd(l)
                if '.' in l and re.search(r'\d{4}', l): item["date"] = parse_date(l)
                if l in ["Access Control", "Logic Flaw", "Oracle Issue", "Phishing", "Reentrancy", "Rugpull", "Honeypot", "Flash Loan Attack"]:
                    item["vector_category"] = l
                    if l in ["Rugpull", "Honeypot"]: item["is_technical"] = False
            if item["loss_usd"] > 0: incidents.append(item)
    return incidents

def parse_rekt_news_extra(file_path):
    """Parses the high-fidelity rekt_news_extra.txt file with block delimiters."""
    incidents = []
    if not os.path.exists(file_path): return incidents
    with open(file_path, 'r') as f:
        content = f.read()
        # Blocks are separated by ---
        blocks = content.split('---')
        for block in blocks:
            if "Protocol:" not in block: continue
            lines = block.strip().split('\n')
            item = {
                "date": "", "protocol": "", "chain": "Other",
                "loss_usd": 0.0, "vector_category": "Other",
                "is_technical": True, "description": block.strip(),
                "source_file": os.path.basename(file_path)
            }
            for line in lines:
                if line.startswith("Protocol:"): item["protocol"] = line.replace("Protocol:", "").strip()
                if line.startswith("Date:"): item["date"] = parse_date(line.replace("Date:", "").strip())
                if line.startswith("Loss:"): item["loss_usd"] = clean_usd(line.replace("Loss:", "").strip())
                if line.startswith("Vector:"): item["vector_category"] = line.replace("Vector:", "").strip()
                if line.startswith("Chain:"): item["chain"] = line.replace("Chain:", "").strip()
            if item["protocol"]:
                incidents.append(item)
    return incidents

def parse_defihacklabs(file_path):
    incidents = []
    if not os.path.exists(file_path): return incidents
    with open(file_path, 'r') as f:
        data = json.load(f)
        for d in data:
            incidents.append({
                "date": parse_date(d.get("date", "")),
                "protocol": d.get("name", "Unknown"),
                "chain": d.get("chain", "Unknown"),
                "loss_usd": clean_usd(d.get("Lost", 0)),
                "vector_category": d.get("type", "Other"),
                "is_technical": str(d.get("type", "")).lower() not in ["rugpull", "honeypot", "abandoned"],
                "description": d.get("Contract", ""),
                "source_file": os.path.basename(file_path)
            })
    return incidents

def main():
    print("Step 1: Parsing all raw sources...")
    master = []
    
    # 1. Academic Table
    master.extend(parse_charoenwong(os.path.join(RAW_DIR, "charoenwong_bernardi_table.txt")))
    
    # 2. Consolidated Rekt Database
    master.extend(parse_rekt_database(os.path.join(RAW_DIR, "rekt_database_raw.txt")))
    
    # 3. Investigative Extra reports
    master.extend(parse_rekt_news_extra(os.path.join(RAW_DIR, "rekt_news_extra.txt")))
    
    # 4. Community Security Tests
    master.extend(parse_defihacklabs(os.path.join(RAW_DIR, "defihacklabs_incidents.json")))
    
    # Cleanup: remove empty entries
    master = [i for i in master if i['date'] and i['protocol'] != "Unknown"]
    
    os.makedirs(BUILD_DIR, exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(master)
    print(f"Step 1 Complete: {len(master)} records saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
