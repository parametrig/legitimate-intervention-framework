import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class ChartSpec:
    chart_id: str
    title: str
    option: Dict[str, Any]
    source_files: List[str]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_envelope(*, chart: Dict[str, Any], source_files: List[str]) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "source_files": source_files,
        "chart": chart,
    }


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def format_usd_short_js() -> str:
    return (
        "function(v){"
        "if(v===null||v===undefined||Number.isNaN(v))return '—';"
        "var n=Number(v);"
        "if(n>=1e12)return '$'+(n/1e12).toFixed(2)+'T';"
        "if(n>=1e9)return '$'+(n/1e9).toFixed(2)+'B';"
        "if(n>=1e6)return '$'+(n/1e6).toFixed(1)+'M';"
        "if(n>=1e3)return '$'+(n/1e3).toFixed(0)+'K';"
        "return '$'+n.toFixed(0);"
        "}"
    )


def js_func(expr: str) -> Dict[str, str]:
    return {"$fn": expr}


def resolve_js_functions(obj: Any) -> Any:
    if isinstance(obj, dict):
        if set(obj.keys()) == {"$fn"} and isinstance(obj["$fn"], str):
            return obj
        return {k: resolve_js_functions(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve_js_functions(v) for v in obj]
    return obj


def materialize_option(*, series_payload: Dict[str, Any], chart_id: str) -> Dict[str, Any]:
    fmt = js_func(format_usd_short_js())

    if chart_id == "chart01_annual_losses":
        yearly = (series_payload.get("series") or {}).get("yearly_loss_usd") or {}
        years = sorted(yearly.keys())
        values = [yearly[y] for y in years]
        return {
            "title": {"text": "Annual Exploit Losses"},
            "xAxis": {"type": "category", "data": years},
            "yAxis": {
                "type": "value",
                "axisLabel": {"formatter": fmt},
                "splitLine": {"lineStyle": {"color": "#f0f0f0"}},
            },
            "tooltip": {"trigger": "axis", "valueFormatter": fmt},
            "series": [
                {"type": "bar", "data": values, "itemStyle": {"opacity": 0.85}},
                {
                    "type": "line",
                    "data": values,
                    "smooth": True,
                    "symbol": "circle",
                    "symbolSize": 6,
                    "lineStyle": {"width": 3},
                },
            ],
            "dataZoom": [
                {"type": "inside"},
                {"type": "slider", "height": 18, "bottom": 12},
            ],
        }

    if chart_id == "chart02_cumulative_losses":
        cumulative = (series_payload.get("series") or {}).get("cumulative_loss_usd") or {}
        years = sorted(cumulative.keys())
        values = [cumulative[y] for y in years]
        return {
            "title": {"text": "Cumulative Exploit Losses"},
            "xAxis": {"type": "category", "data": years},
            "yAxis": {
                "type": "value",
                "axisLabel": {"formatter": fmt},
                "splitLine": {"lineStyle": {"color": "#f0f0f0"}},
            },
            "tooltip": {"trigger": "axis", "valueFormatter": fmt},
            "series": [
                {
                    "type": "line",
                    "data": values,
                    "smooth": True,
                    "areaStyle": {"opacity": 0.12},
                    "symbol": "none",
                    "lineStyle": {"width": 3},
                }
            ],
            "dataZoom": [
                {"type": "inside"},
                {"type": "slider", "height": 18, "bottom": 12},
            ],
        }

    if chart_id == "chart08_four_layer_timeline":
        series = series_payload.get("series") or {}
        years = [str(y) for y in (series.get("years") or [])]
        layers = series.get("layers") or {}

        intervened = layers.get("intervened_loss_usd") or []
        eligible_not = layers.get("eligible_not_intervened_loss_usd") or []
        other_non = layers.get("other_non_addressable_loss_usd") or []
        systemic = layers.get("systemic_loss_usd") or []

        return {
            "title": {"text": "Annual DeFi Losses by Category (Four-Layer)"},
            "legend": {"top": 28},
            "xAxis": {"type": "category", "data": years},
            "yAxis": {
                "type": "value",
                "axisLabel": {"formatter": fmt},
                "splitLine": {"lineStyle": {"color": "#f0f0f0"}},
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "valueFormatter": fmt,
            },
            "series": [
                {"name": "Actually Intervened", "type": "bar", "stack": "total", "data": intervened},
                {"name": "Eligible (Not Intervened)", "type": "bar", "stack": "total", "data": eligible_not},
                {"name": "Other Non-Addressable", "type": "bar", "stack": "total", "data": other_non},
                {"name": "Systemic Failures", "type": "bar", "stack": "total", "data": systemic},
            ],
            "dataZoom": [
                {"type": "inside"},
                {"type": "slider", "height": 18, "bottom": 12},
            ],
        }

    if chart_id == "chart09_vector_distribution":
        counts = (series_payload.get("series") or {}).get("vector_count") or {}
        rows = sorted(((k, v) for k, v in counts.items()), key=lambda kv: kv[1], reverse=True)[:12]
        labels = [k for k, _ in rows]
        values = [v for _, v in rows]

        return {
            "title": {"text": "Top Attack Vectors (Frequency)"},
            "xAxis": {"type": "value"},
            "yAxis": {"type": "category", "data": labels, "inverse": True},
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "series": [{"type": "bar", "data": values, "itemStyle": {"opacity": 0.9}}],
        }

    raise ValueError(f"Unsupported chart_id: {chart_id}")


def build_chart_specs(*, web_data_dir: Path) -> List[ChartSpec]:
    series_dir = web_data_dir / "series"

    yearly_totals = load_json(series_dir / "yearly_totals.json")
    cumulative_totals = load_json(series_dir / "cumulative_totals.json")
    four_layer = load_json(series_dir / "four_layer_yearly_losses.json")
    vectors = load_json(series_dir / "vector_distribution.json")

    return [
        ChartSpec(
            chart_id="chart01_annual_losses",
            title="Annual Exploit Losses",
            option=materialize_option(series_payload=yearly_totals, chart_id="chart01_annual_losses"),
            source_files=[str(Path("web/data/series/yearly_totals.json"))],
        ),
        ChartSpec(
            chart_id="chart02_cumulative_losses",
            title="Cumulative Exploit Losses",
            option=materialize_option(series_payload=cumulative_totals, chart_id="chart02_cumulative_losses"),
            source_files=[str(Path("web/data/series/cumulative_totals.json"))],
        ),
        ChartSpec(
            chart_id="chart08_four_layer_timeline",
            title="Annual DeFi Losses by Category (Four-Layer)",
            option=materialize_option(series_payload=four_layer, chart_id="chart08_four_layer_timeline"),
            source_files=[str(Path("web/data/series/four_layer_yearly_losses.json"))],
        ),
        ChartSpec(
            chart_id="chart09_vector_distribution",
            title="Top Attack Vectors (Frequency)",
            option=materialize_option(series_payload=vectors, chart_id="chart09_vector_distribution"),
            source_files=[str(Path("web/data/series/vector_distribution.json"))],
        ),
    ]


def dump_chart_json(spec: ChartSpec) -> Dict[str, Any]:
    chart = {
        "id": spec.chart_id,
        "title": spec.title,
        "option": resolve_js_functions(spec.option),
    }
    return build_envelope(chart=chart, source_files=spec.source_files)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate per-chart JSON specs for interactive ECharts rendering")
    parser.add_argument(
        "--web-data-dir",
        default=str(Path(__file__).resolve().parents[2] / "web" / "data"),
        help="Path to web/data directory",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output directory for chart specs (defaults to <web-data-dir>/charts)",
    )

    args = parser.parse_args(argv)

    web_data_dir = Path(args.web_data_dir).resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else (web_data_dir / "charts")

    specs = build_chart_specs(web_data_dir=web_data_dir)
    for spec in specs:
        out_path = out_dir / f"{spec.chart_id}.json"
        payload = dump_chart_json(spec)
        write_json(out_path, payload)

    print(f"Wrote {len(specs)} chart spec(s) to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
