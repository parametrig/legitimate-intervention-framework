#!/usr/bin/env python3
"""
Master runner for LIF chart generation.
Executes batch scripts 0 through 6 to generate all 50 chart specs.
"""

import subprocess
import sys
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
BATCHES = [
    "gen_charts_batch0.py",
    "gen_charts_batch1.py",
    "gen_charts_batch2.py",
    "gen_charts_batch3.py",
    "gen_charts_batch4.py",
    "gen_charts_batch5.py",
    "gen_charts_batch6.py",
]

def run_batch(script_name):
    script_path = BASE_DIR / script_name
    print(f"Running {script_name}...")
    try:
        # Use sys.executable to ensure we use the same python interpreter
        result = subprocess.run([sys.executable, str(script_path)], 
                               cwd=BASE_DIR, 
                               check=False, 
                               capture_output=True, 
                               text=True)
        if result.stdout:
            print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Error in {script_name}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"💥 Failed to execute {script_name}: {str(e)}")
        return False
    return True

def main():
    print("🚀 Starting Global LIF Chart Regeneration (50 Charts)\n")
    success_count = 0
    
    for batch in BATCHES:
        if run_batch(batch):
            success_count += 1
        else:
            print(f"⚠️ Warning: Batch {batch} failed to complete successfully.")
            
    print(f"\n✨ Completed {success_count}/{len(BATCHES)} batches.")
    print("📂 Check web/data/charts/ for updated JSON specs.")

if __name__ == "__main__":
    main()
