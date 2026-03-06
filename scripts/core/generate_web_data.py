#!/usr/bin/env python3
"""Generate JSON data files for the LIF web database.

When the Parametrig infrastructure repo is available in the same workspace,
the canonical normalized AUK JSON files are used as the source of truth for
`web/data/exploits.json` and `web/data/interventions.json`.

This keeps the website fallback data aligned with the live API contract.
If the infrastructure repo is unavailable, the script falls back to local CSV
generation for standalone use.
"""

import csv
import json
import os
from pathlib import Path
import shutil

# Get repository root (two levels up from scripts/core/)
REPO_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = REPO_ROOT / "data" / "refined"
WEB_DATA_DIR = REPO_ROOT / "web" / "data"
RATIONALES_FILE = REPO_ROOT / "manuscript" / "rationales.md"

SCHEMA_VERSION = "1.0"


def find_infra_defi_dir():
    """Locate the canonical infrastructure data directory if present."""
    env_dir = Path(os.environ["PARAMETRIG_INFRA_DATA_DIR"]) if "PARAMETRIG_INFRA_DATA_DIR" in os.environ else None
    candidates = [env_dir] if env_dir else []
    candidates.append(REPO_ROOT.parents[1] / "PARAMETRIG" / "parametrig" / "infrastructure" / "data" / "auk" / "defi")
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    return None

def load_csv(filepath):
    """Load CSV file and return list of dicts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def parse_float(val):
    """Safely parse float from string."""
    if not val or val == '':
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def parse_year(date_str):
    """Extract year from YYYY-MM-DD date string."""
    if not date_str:
        return None
    try:
        return int(date_str[:4])
    except (ValueError, TypeError):
        return None

def extract_rationale_cases():
    """Extract case rationale text from rationales.md."""
    rationales = {}
    try:
        with open(RATIONALES_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Map protocol names to their rationale key
            case_markers = [
                ("StakeWise", "stakewise"),
                ("VeChain", "vechain"),
                ("Sui/Cetus", "cetus"),
                ("BNB Chain", "bnb"),
                ("Berachain", "berachain"),
                ("Harmony", "harmony"),
                ("Gnosis Chain", "gnosis"),
                ("Flow Blockchain", "flow"),
                ("MakerDAO", "makerdao"),
                ("Euler", "euler"),
                ("Balancer", "balancer"),
                ("Liqwid", "liqwid"),
                ("Aave v2", "aave"),
                ("Curve", "curve"),
                ("dYdX", "dydx"),
                ("Poly Network", "poly"),
                ("Ronin", "ronin"),
                ("Cork", "cork"),
                ("Sonic", "sonic"),
                ("Tether", "tether"),
                ("Circle", "circle"),
                ("PlayDapp", "playdapp"),
                ("Radiant", "radiant"),
                ("DeltaPrime", "deltaprime"),
                ("Sonne", "sonne"),
                ("Badger", "badger"),
                ("Cream", "cream"),
                ("Revest", "revest"),
            ]
            
            for name, key in case_markers:
                # Find the section for this case
                section_start = content.find(f"### {name}")
                if section_start == -1:
                    continue
                    
                # Determine end of section (next ### or ## or end of file)
                # We search for newline + header to avoid matching the current header (e.g. ### contains ##)
                next_header_3 = content.find("\n### ", section_start + 1)
                next_header_2 = content.find("\n## ", section_start + 1)
                
                # If section starts at 0, first find might match if we search from 0. 
                # But section_start + 1 ensures we are past the first char.
                # However, to be safe and clean, looking for \n ensures we find new headers.
                
                if next_header_3 == -1 and next_header_2 == -1:
                    section_content = content[section_start:]
                elif next_header_3 == -1:
                    section_content = content[section_start:next_header_2]
                elif next_header_2 == -1:
                    section_content = content[section_start:next_header_3]
                else:
                    section_content = content[section_start:min(next_header_3, next_header_2)]
                
                # Strategies to extract rationale
                text = None
                
                # Strategy 1: "=== Classification Rationale ===" block
                rationale_header = "=== Classification Rationale ==="
                start_idx = section_content.find(rationale_header)
                if start_idx != -1:
                    content_start = start_idx + len(rationale_header)
                    end_idx = section_content.find("===", content_start)
                    if end_idx != -1:
                        text = section_content[content_start:end_idx].strip()
                    else:
                        text = section_content[content_start:].strip()
                
                # Strategy 2: "Rationale for Scope" (flexible search)
                if not text:
                    for marker in ["1. Rationale for Scope", "Rationale for Scope"]:
                        start_idx = section_content.find(marker)
                        if start_idx != -1:
                            text = section_content[start_idx:].strip()
                            break
                        
                # Strategy 3: "- Scope rationale:"
                if not text:
                    start_idx = section_content.find("- Scope rationale:")
                    if start_idx != -1:
                        text = section_content[start_idx:].strip()
                
                if text:
                    # Clean up formatting for HTML display
                    text = text.replace("1. Rationale for Scope:", "<strong>Rationale for Scope:</strong>")
                    text = text.replace("Rationale for Scope", "<strong>Rationale for Scope</strong>")
                    text = text.replace("2. Rationale for Authority:", "\n\n<strong>Rationale for Authority:</strong>")
                    text = text.replace("Rationale for Authority", "\n\n<strong>Rationale for Authority</strong>")
                    text = text.replace("- Scope rationale:", "<strong>Rationale for Scope:</strong>")
                    text = text.replace("- Authority rationale:", "\n\n<strong>Rationale for Authority:</strong>")
                    text = text.replace("Summary", "\n\n<strong>Summary</strong>")
                    
                    # Convert newlines to breaks, but preserve paragraph structure
                    text = text.replace('\n', '<br>')
                    
                    # Final cleanup of trailing dividers/newlines/breaks
                    text = text.strip()
                    while text.endswith('==='):
                        text = text[:-3].strip()
                    while text.endswith('<br>'):
                        text = text[:-4].strip()
                    while text.endswith('==='): # Handle edge case where === was before <br>
                        text = text[:-3].strip()
                    
                    rationales[key] = text.strip()
    except FileNotFoundError:
        print(f"Warning: Rationale file not found at {RATIONALES_FILE}")
        pass
    return rationales

def generate_exploits_json():
    """Generate exploits.json from lif_exploits_final.csv."""
    exploits_csv = DATA_DIR / "lif_exploits_final.csv"
    rows = load_csv(exploits_csv)
    
    exploits = []
    for row in rows:
        exploit = {
            "id": row.get("incident_id", f"{row.get('protocol', 'Unknown')}_{row.get('date', '')}"),
            "date": row.get("date", ""),
            "year": parse_year(row.get("date", "")),
            "protocol": row.get("protocol", ""),
            "chain": row.get("chain", ""),
            "loss_usd": parse_float(row.get("loss_usd")),
            "vector": row.get("vector_category", row.get("attack_type", "")),
            "is_intervention": row.get("is_intervention", "").lower() == "true",
            "is_lif_relevant": row.get("is_lif_relevant", "").lower() == "true",
            "description": row.get("description", ""),
            "source_url": row.get("source_url", row.get("source", "")),
        }
        exploits.append(exploit)
    
    # Sort by date descending (newest first)
    exploits.sort(key=lambda x: x["date"] or "", reverse=True)
    
    return exploits

def generate_interventions_json():
    """Generate interventions.json from both intervention CSVs."""
    all_interventions_csv = DATA_DIR / "lif_all_interventions.csv"
    metrics_csv = DATA_DIR / "lif_intervention_metrics.csv"
    
    # Load both datasets
    all_rows = load_csv(all_interventions_csv)
    metrics_rows = load_csv(metrics_csv)
    
    # Create lookup for metrics data
    metrics_lookup = {}
    for row in metrics_rows:
        key = row.get("incident_id", "")
        metrics_lookup[key] = row
    
    # Rationale cases
    rationale_map = extract_rationale_cases()
    
    # Merge data
    interventions = []
    seen_ids = set()
    
    for row in all_rows:
        incident_id = row.get("incident_id", f"{row.get('protocol', '')}_{row.get('date', '')}")
        if incident_id in seen_ids:
            continue
        seen_ids.add(incident_id)
        
        # Check for metrics enrichment
        metrics = metrics_lookup.get(incident_id, {})
        
        protocol = row.get("protocol", "")
        
        # Find rationale text if available
        rationale_text = None
        for name, key in [
                ("StakeWise", "stakewise"),
                ("VeChain", "vechain"),
                ("Sui/Cetus", "cetus"),
                ("BNB Chain", "bnb"),
                ("Berachain", "berachain"),
                ("Harmony", "harmony"),
                ("Gnosis Chain", "gnosis"),
                ("Flow Blockchain", "flow"),
                ("MakerDAO", "makerdao"),
                ("Euler", "euler"),
                ("Balancer", "balancer"),
                ("Liqwid", "liqwid"),
                ("Aave", "aave"),
                ("Curve", "curve"),
                ("dYdX", "dydx"),
                ("Poly Network", "poly"),
                ("Ronin", "ronin"),
                ("Cork", "cork"),
                ("Sonic", "sonic"),
                ("Tether", "tether"),
                ("Circle", "circle"),
                ("PlayDapp", "playdapp"),
                ("Radiant", "radiant"),
                ("DeltaPrime", "deltaprime"),
                ("Sonne", "sonne"),
                ("Badger", "badger"),
                ("Cream", "cream"),
                ("Revest", "revest"),
            ]:
            if name.lower() in protocol.lower() and key in rationale_map:
                rationale_text = rationale_map[key]
                break
        
        intervention = {
            "id": incident_id,
            "date": row.get("date", ""),
            "year": parse_year(row.get("date", "")),
            "protocol": protocol,
            "chain": row.get("chain", ""),
            "loss_usd": parse_float(row.get("loss_usd")),
            "loss_prevented_usd": parse_float(row.get("loss_prevented_usd") or metrics.get("loss_prevented_usd")),
            "vector": row.get("vector_category", ""),
            "scope": row.get("scope", ""),
            "authority": row.get("authority", ""),
            "is_proactive": False,
            "success_pct": parse_float(row.get("containment_success_pct") or metrics.get("containment_success_pct")),
            "time_to_detect_min": parse_float(row.get("time_to_detect_min") or metrics.get("time_to_detect_min")),
            "time_to_contain_min": parse_float(row.get("time_to_contain_min") or metrics.get("time_to_contain_min")),
            "description": row.get("description", ""),
            "intervention_notes": row.get("intervention_notes", metrics.get("notes", "")),
            "source_url": row.get("intervention_source", row.get("source_url", metrics.get("source", ""))),
            "has_rationale": rationale_text is not None,
            "rationale": rationale_text
        }
        interventions.append(intervention)
    
    # Add metrics-only cases (proactive interventions)
    for incident_id, row in metrics_lookup.items():
        if incident_id not in seen_ids:
            seen_ids.add(incident_id)
            protocol = row.get("protocol", "")
            
            # Find rationale text if available
            rationale_text = None
            for name, key in [
                    ("StakeWise", "stakewise"),
                    ("VeChain", "vechain"),
                    ("Sui/Cetus", "cetus"),
                    ("BNB Chain", "bnb"),
                    ("Berachain", "berachain"),
                    ("Harmony", "harmony"),
                    ("Gnosis Chain", "gnosis"),
                    ("Flow Blockchain", "flow"),
                    ("MakerDAO", "makerdao"),
                    ("Euler", "euler"),
                    ("Balancer", "balancer"),
                    ("Liqwid", "liqwid"),
                    ("Aave", "aave"),
                    ("Curve", "curve"),
                    ("dYdX", "dydx"),
                    ("Poly Network", "poly"),
                    ("Ronin", "ronin"),
                    ("Cork", "cork"),
                    ("Sonic", "sonic"),
                    ("Tether", "tether"),
                    ("Circle", "circle"),
                    ("PlayDapp", "playdapp"),
                    ("Radiant", "radiant"),
                    ("DeltaPrime", "deltaprime"),
                    ("Sonne", "sonne"),
                    ("Badger", "badger"),
                    ("Cream", "cream"),
                    ("Revest", "revest"),
                ]:
                if name.lower() in protocol.lower() and key in rationale_map:
                    rationale_text = rationale_map[key]
                    break

            intervention = {
                "id": incident_id,
                "date": row.get("date", ""),
                "year": parse_year(row.get("date", "")),
                "protocol": protocol,
                "chain": row.get("chain", ""),
                "loss_usd": parse_float(row.get("loss_usd")),
                "loss_prevented_usd": parse_float(row.get("loss_prevented_usd")),
                "vector": row.get("vector_category", ""),
                "scope": row.get("scope", ""),
                "authority": row.get("authority", ""),
                "is_proactive": True,
                "success_pct": parse_float(row.get("containment_success_pct")),
                "time_to_detect_min": parse_float(row.get("time_to_detect_min")),
                "time_to_contain_min": parse_float(row.get("time_to_contain_min")),
                "description": row.get("notes", ""),
                "intervention_notes": row.get("notes", ""),
                "source_url": row.get("source", ""),
                "has_rationale": rationale_text is not None,
                "rationale": rationale_text
            }
            interventions.append(intervention)
    
    # Sort by date descending (newest first)
    interventions.sort(key=lambda x: x["date"] or "", reverse=True)
    
    return interventions

def main():
    """Generate all JSON data files."""
    # Ensure output directory exists
    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)

    infra_defi_dir = find_infra_defi_dir()
    if infra_defi_dir:
        print(f"Using canonical infrastructure JSON from {infra_defi_dir}")
        shutil.copy2(infra_defi_dir / "exploits.json", WEB_DATA_DIR / "exploits.json")
        shutil.copy2(infra_defi_dir / "interventions.json", WEB_DATA_DIR / "interventions.json")
        with open(infra_defi_dir / "exploits.json", "r", encoding="utf-8") as f:
            exploits_records = json.load(f)
        with open(infra_defi_dir / "interventions.json", "r", encoding="utf-8") as f:
            interventions_records = json.load(f)
        print(f"  → {len(exploits_records)} exploits synced")
        print(f"  → {len(interventions_records)} interventions synced")
    else:
        print("Canonical infrastructure repo not found; falling back to local CSV generation.")

        print("Generating exploits.json...")
        exploits_records = generate_exploits_json()
        with open(WEB_DATA_DIR / "exploits.json", 'w', encoding='utf-8') as f:
            json.dump(exploits_records, f, indent=2, ensure_ascii=False)
        print(f"  → {len(exploits_records)} exploits written")

        print("Generating interventions.json...")
        interventions_records = generate_interventions_json()
        with open(WEB_DATA_DIR / "interventions.json", 'w', encoding='utf-8') as f:
            json.dump(interventions_records, f, indent=2, ensure_ascii=False)
        print(f"  → {len(interventions_records)} interventions written")

    # Summary stats
    total_loss = sum(i["loss_usd"] or 0 for i in interventions_records)
    total_saved = sum(i["loss_prevented_usd"] or 0 for i in interventions_records)
    dates = [i["date"] for i in interventions_records if i["date"]]
    min_year = min(dates)[:4] if dates else "N/A"
    max_year = max(dates)[:4] if dates else "N/A"
    
    print(f"\nSummary:")
    print(f"  Interventions: {len(interventions_records)} cases ({min_year}-{max_year})")
    print(f"  Total at risk: ${total_loss/1e9:.2f}B")
    print(f"  Total saved: ${total_saved/1e9:.2f}B")

if __name__ == "__main__":
    main()
