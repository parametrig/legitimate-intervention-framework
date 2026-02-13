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
    "blue":    "#2563EB",
    "green":   "#16A34A",
    "purple":  "#7C3AED",
    "amber":   "#D97706",
    "red":     "#DC2626",
    "slate":   "#475569",
    "gray":    "#6B7280",
    "lgray":   "#9CA3AF",
    "lblue":   "#60A5FA",
    "ink":     "#1E293B",
}

AUTH_COLORS = {
    "Signer Set":     C["blue"],
    "Delegated Body": C["green"],
    "Governance":     C["purple"],
    "Unknown":        C["gray"],
}

SCOPE_ORDER     = ["Asset", "Account", "Protocol", "Network", "Module"]
AUTHORITY_ORDER = ["Signer Set", "Delegated Body", "Governance"]
AUTHORITY_MAP   = {"Protocol Team": "Signer Set", "Security Council": "Delegated Body"}

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
    with open(path, "w") as f:
        json.dump({"chart": option}, f, indent=2, default=_ser)
    print(f"  ✓ {path.name}  ({os.path.getsize(path)} bytes)")

def _ser(o):
    if isinstance(o, (np.integer,)):   return int(o)
    if isinstance(o, (np.floating,)):  return round(float(o), 4)
    if isinstance(o, (np.bool_,)):     return bool(o)
    if isinstance(o, (pd.Timestamp,)): return o.isoformat()
    if pd.isna(o):                     return None
    raise TypeError(f"Cannot serialize {type(o)}")

def fmt_usd(v):
    if abs(v) >= 1e9:  return f"${v/1e9:.1f}B"
    if abs(v) >= 1e6:  return f"${v/1e6:.0f}M"
    if abs(v) >= 1e3:  return f"${v/1e3:.0f}K"
    return f"${v:.0f}"

def top_n(series, n=10):
    return series.value_counts().head(n)
