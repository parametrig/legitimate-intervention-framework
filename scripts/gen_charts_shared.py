"""Shared infrastructure for chart spec generation."""
import json, os
from pathlib import Path
import pandas as pd
import numpy as np

# ── Paths ───────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parents[1]
DATA  = BASE / "data" / "refined"
OUT   = BASE / "web" / "data" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

# ── Color palette (matches notebook COLORS dict) ───────────────────
C = {
    # Base Tones
    "slate":   "#475569",
    "gray":    "#6B7280",
    "lgray":   "#9CA3AF",
    "vlgray":  "#F1F5F9", # Lightest blue-gray for background/systemic
    "ink":     "#1E293B",
    # Authority / Role Colors (Cool)
    "blue":    "#2563EB",
    "teal":    "#0D9488",
    "purple":  "#7C3AED",
    "lblue":   "#60A5FA",
    # Scope / Impact Colors (Vivid)
    "red":     "#DC2626",
    "amber":   "#D97706",
    "indigo":  "#4F46E5",
    "pink":    "#DB2777",
    "green":   "#16A34A", # Characterstic LIF Green
    # Categorical / Subset Tones
    "emerald": "#059669",
    "orange":  "#EA580C",
}

# Authority (Operational roles)
AUTH_COLORS = {
    "Signer Set":     C["blue"],    # Core System
    "Delegated Body": C["teal"],    # Specialized/Council
    "Governance":     C["purple"],  # Heavy/Slow
    "Unknown":        C["gray"],
}

# Scope (Technical Impact Layer)
SCOPE_COLORS = {
    "Network":  C["red"],      # Critical Infrastructure
    "Protocol": C["amber"],    # Core Logic
    "Asset":    C["indigo"],   # Value Layer
    "Module":   C["pink"],     # Specialized Logic
    "Account":  C["emerald"],  # User-centric (Standard green)
}

# Subsets (Data Tiers)
SUBSET_COLORS = {
    "All Interventions":      C["slate"],   # Reference line
    "LIF-Relevant":           C["green"],   # Matches Chart 02 Target
    "High-Fidelity Metrics":  C["orange"],  # Technical subset
}

LOSS_COLORS = {
    "Incurred": C["red"],
    "Saved":    C["green"],
    "Prevented": C["green"], # Alias for Saved
}

SCOPE_ORDER     = ["Network", "Protocol", "Asset", "Account", "Module"]
AUTHORITY_ORDER = ["Signer Set", "Delegated Body", "Governance"]
AUTHORITY_MAP   = {"Protocol Team": "Signer Set", "Security Council": "Delegated Body"}

SUBSET_COLORS = {
    "All Interventions":      C["purple"],
    "LIF-Relevant":           C["green"],
    "High-Fidelity Metrics":  C["amber"],
}

# Helper to remove xAxis name (prevent bottom-right overlap on horizontal bars)
HIDE_X_NAME = {"name": "", "nameLocation": "middle", "nameGap": 0}

# ── Data loading ───────────────────────────────────────────────────
def load_data():
    exploits = pd.read_csv(DATA / "lif_exploits_final.csv")
    interventions = pd.read_csv(DATA / "lif_all_interventions.csv")
    metrics = pd.read_csv(DATA / "lif_intervention_metrics.csv")

    for df in [exploits, interventions, metrics]:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["year"] = df["date"].dt.year
        for col in ["loss_usd","loss_prevented_usd","time_to_detect_min",
                     "time_to_contain_min","containment_success_pct"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

    for df in [interventions, metrics]:
        df["authority_standardized"] = df["authority"].replace(AUTHORITY_MAP)

    # Combined (deduplicated)
    combined = pd.concat([interventions, metrics], ignore_index=True)
    combined["authority_standardized"] = combined["authority"].replace(AUTHORITY_MAP)
    combined = combined.drop_duplicates(subset=["incident_id"], keep="first")

    return exploits, interventions, metrics, combined


# ── Helpers ────────────────────────────────────────────────────────
def save(chart_id: str, option: dict):
    """Write {chart: option} JSON to the output dir."""
    path = OUT / f"{chart_id}.json"
    # Recursively clean NaNs/Infs before dumping
    cleaned = _clean_nans(option)
    with open(path, "w") as f:
        json.dump({"chart": cleaned}, f, indent=2, default=_ser)
    print(f"  ✓ {path.name}  ({os.path.getsize(path)} bytes)")

def _clean_nans(obj):
    if isinstance(obj, dict):
        return {k: _clean_nans(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_nans(v) for v in obj]
    if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
        return None
    if pd.isna(obj):
        return None
    return obj

def _ser(o):
    if pd.isna(o):                     return None
    if isinstance(o, (np.integer,)):   return int(o)
    if isinstance(o, (np.floating,)):  return round(float(o), 4)
    if isinstance(o, (np.bool_,)):     return bool(o)
    if isinstance(o, (pd.Timestamp,)): return o.isoformat()
    raise TypeError(f"Cannot serialize {type(o)}")

def fmt_usd(v):
    if abs(v) >= 1e9:  return f"${v/1e9:.1f}B"
    if abs(v) >= 1e6:  return f"${v/1e6:.0f}M"
    if abs(v) >= 1e3:  return f"${v/1e3:.0f}K"
    return f"${v:.0f}"

def top_n(series, n=10):
    return series.value_counts().head(n)
