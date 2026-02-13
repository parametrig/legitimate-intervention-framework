#!/usr/bin/env python3
"""Generate aggregated series JSON files for interactive web charts.

This script is intentionally separate from the analysis notebook so it can be
run headlessly and remain the reproducible source for web-consumable time series.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = REPO_ROOT / "data" / "refined"
WEB_DATA_DIR = REPO_ROOT / "web" / "data"
WEB_SERIES_DIR = WEB_DATA_DIR / "series"

SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class SourceFiles:
    exploits: Path
    all_interventions: Path
    metrics: Path


def build_envelope(*, series: dict, source_files: dict) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_files": source_files,
        "series": series,
    }


def _to_rel_str(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def _normalize_bool(s: object) -> bool:
    if s is None:
        return False
    if isinstance(s, bool):
        return s
    return str(s).strip().lower() in {"true", "1", "yes", "y"}


def load_exploits(exploits_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(exploits_csv)

    df["date"] = pd.to_datetime(df.get("date"), errors="coerce")
    df["year"] = df["date"].dt.year

    if "loss_usd" in df.columns:
        df["loss_usd"] = pd.to_numeric(df["loss_usd"], errors="coerce").fillna(0.0)
    else:
        df["loss_usd"] = 0.0

    if "vector_category" not in df.columns:
        df["vector_category"] = ""
    df["vector_category"] = df["vector_category"].fillna("")

    if "is_lif_relevant" in df.columns:
        df["is_lif_relevant"] = df["is_lif_relevant"].apply(_normalize_bool)
    else:
        df["is_lif_relevant"] = False

    if "is_intervention" in df.columns:
        df["is_intervention"] = df["is_intervention"].apply(_normalize_bool)
    else:
        df["is_intervention"] = False

    return df


def build_yearly_totals(exploits_df: pd.DataFrame) -> dict:
    yearly = exploits_df.groupby("year")["loss_usd"].sum().sort_index()
    yearly = yearly.dropna()
    return {str(int(year)): float(val) for year, val in yearly.items() if pd.notna(year)}


def build_cumulative_totals(yearly_loss_usd: dict) -> dict:
    running = 0.0
    cumulative: dict[str, float] = {}
    for year in sorted(yearly_loss_usd.keys()):
        running += float(yearly_loss_usd[year])
        cumulative[year] = float(running)
    return cumulative


def build_vector_distribution(exploits_df: pd.DataFrame) -> dict:
    vectors = exploits_df.copy()
    vectors["vector_category"] = vectors["vector_category"].replace({"": "Unknown"})

    counts = vectors["vector_category"].value_counts(dropna=False)
    loss_by_vector = vectors.groupby("vector_category")["loss_usd"].sum().sort_values(ascending=False)

    return {
        "vector_count": {str(k): int(v) for k, v in counts.to_dict().items()},
        "vector_loss_usd": {str(k): float(v) for k, v in loss_by_vector.to_dict().items()},
    }


def build_four_layer_yearly(exploits_df: pd.DataFrame) -> dict:
    eligible = exploits_df[exploits_df["is_lif_relevant"] == True].copy()

    systemic_mask = (
        (exploits_df["is_lif_relevant"] == False)
        & (exploits_df["vector_category"].str.contains("Systemic|Economic", case=False, na=False))
    )
    systemic = exploits_df[systemic_mask].copy()

    other_non_addressable = exploits_df[(exploits_df["is_lif_relevant"] == False) & (~systemic_mask)].copy()

    intervened = eligible[eligible["is_intervention"] == True].copy()

    eligible_yearly = eligible.groupby("year")["loss_usd"].sum()
    intervened_yearly = intervened.groupby("year")["loss_usd"].sum()
    other_yearly = other_non_addressable.groupby("year")["loss_usd"].sum()
    systemic_yearly = systemic.groupby("year")["loss_usd"].sum()

    years = sorted(
        {
            *[int(y) for y in eligible_yearly.index.dropna().tolist()],
            *[int(y) for y in intervened_yearly.index.dropna().tolist()],
            *[int(y) for y in other_yearly.index.dropna().tolist()],
            *[int(y) for y in systemic_yearly.index.dropna().tolist()],
        }
    )

    def v(series: pd.Series) -> list[float]:
        aligned = series.reindex(years, fill_value=0.0)
        return [float(aligned.loc[y]) for y in years]

    eligible_vals = v(eligible_yearly)
    intervened_vals = v(intervened_yearly)
    other_vals = v(other_yearly)
    systemic_vals = v(systemic_yearly)

    eligible_not_intervened_vals = [float(e - i) for e, i in zip(eligible_vals, intervened_vals)]

    return {
        "years": years,
        "layers": {
            "intervened_loss_usd": intervened_vals,
            "eligible_not_intervened_loss_usd": eligible_not_intervened_vals,
            "other_non_addressable_loss_usd": other_vals,
            "systemic_loss_usd": systemic_vals,
        },
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def main() -> None:
    sources = SourceFiles(
        exploits=DATA_DIR / "lif_exploits_final.csv",
        all_interventions=DATA_DIR / "lif_all_interventions.csv",
        metrics=DATA_DIR / "lif_intervention_metrics.csv",
    )

    exploits_df = load_exploits(sources.exploits)

    yearly_loss_usd = build_yearly_totals(exploits_df)
    cumulative_loss_usd = build_cumulative_totals(yearly_loss_usd)
    vector_dist = build_vector_distribution(exploits_df)
    four_layer = build_four_layer_yearly(exploits_df)

    source_files_payload = {
        "exploits": _to_rel_str(sources.exploits),
        "all_interventions": _to_rel_str(sources.all_interventions),
        "metrics": _to_rel_str(sources.metrics),
    }

    write_json(
        WEB_SERIES_DIR / "yearly_totals.json",
        build_envelope(series={"yearly_loss_usd": yearly_loss_usd}, source_files=source_files_payload),
    )
    write_json(
        WEB_SERIES_DIR / "cumulative_totals.json",
        build_envelope(series={"cumulative_loss_usd": cumulative_loss_usd}, source_files=source_files_payload),
    )
    write_json(
        WEB_SERIES_DIR / "vector_distribution.json",
        build_envelope(series=vector_dist, source_files=source_files_payload),
    )
    write_json(
        WEB_SERIES_DIR / "four_layer_yearly_losses.json",
        build_envelope(series=four_layer, source_files=source_files_payload),
    )

    print("Generated web series JSON:")
    print(f"  → {WEB_SERIES_DIR / 'yearly_totals.json'}")
    print(f"  → {WEB_SERIES_DIR / 'cumulative_totals.json'}")
    print(f"  → {WEB_SERIES_DIR / 'vector_distribution.json'}")
    print(f"  → {WEB_SERIES_DIR / 'four_layer_yearly_losses.json'}")


if __name__ == "__main__":
    main()
