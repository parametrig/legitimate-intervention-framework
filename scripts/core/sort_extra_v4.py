import re
import datetime
import os

# Resolve file path relative to this script's location (scripts/core/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
REKT_FILE = os.path.join(BASE_DIR, "data/raw/rekt_news_extra.txt")

def parse_rekt_date(content):
    match = re.search(r'Date: (.*)', content)
    if not match:
        return datetime.date.min
    date_str = match.group(1).strip()
    try:
        # Try YYYY-MM-DD
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        try:
            # Try Month DD, YYYY
            return datetime.datetime.strptime(date_str, '%b %d, %Y').date()
        except ValueError:
            try:
                # Try Month DD YYYY
                return datetime.datetime.strptime(date_str, '%B %d, %Y').date()
            except ValueError:
                return datetime.date.min

with open(REKT_FILE, 'r') as f:
    text = f.read()

entries = text.split('\n---\n')
# Filter out empty entries
entries = [e.strip() for e in entries if e.strip()]

# Sort entries based on extracted date
entries.sort(key=lambda x: parse_rekt_date(x))

with open(REKT_FILE, 'w') as f:
    f.write('\n\n---\n'.join(entries))
    f.write('\n')

print(f"Sorted {len(entries)} entries chronologically.")
