"""Batch 4: Charts 37-42 (Speed, success, and timing analysis)."""
from gen_charts_shared import *

exploits, interventions, metrics, combined = load_data()

# ── Chart 37: Response Time by Authority (bar, log scale) ─────────
resp = metrics.groupby("authority")["time_to_contain_min"].median().reindex(AUTHORITY_ORDER)
colors37 = [C["blue"], C["green"], C["purple"]]
save("chart37_response_time", {
    "title": {"text": "Median Response Time by Authority"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": AUTHORITY_ORDER},
    "yAxis": {"type": "log", "name": "Minutes (Log)", "min": 1},
    "series": [{
        "type": "bar",
        "data": [{"value": round(float(resp[a]),0) if not pd.isna(resp.get(a)) else 0,
                  "itemStyle": {"color": colors37[i]},
                  "label": {"show": True, "position": "top",
                            "formatter": f"{float(resp[a]):.0f} min" if not pd.isna(resp.get(a)) else "N/A"}}
                 for i, a in enumerate(AUTHORITY_ORDER)]
    }]
})

# ── Chart 38: Success vs Response Time (scatter + regression) ─────
sc38 = metrics[["time_to_contain_min","containment_success_pct","authority"]].dropna()
save("chart38_success_vs_time", {
    "title": {"text": "Success Rate vs. Response Time"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "log", "name": "Response Time (min)"},
    "yAxis": {"type": "value", "name": "Success Rate (%)", "max": 110},
    "series": [
        {"name": auth, "type": "scatter", "symbolSize": 14,
         "data": [[float(r["time_to_contain_min"]), float(r["containment_success_pct"])]
                  for _, r in sc38[sc38["authority"]==auth].iterrows()],
         "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}}
        for auth in sc38["authority"].unique()
    ]
})

# ── Chart 39: Risk Matrix Scatter (loss × time × success) ────────
sc39 = metrics[["time_to_contain_min","loss_usd","containment_success_pct","authority"]].dropna()
series39 = []
for auth in sc39["authority"].unique():
    ad = sc39[sc39["authority"]==auth]
    series39.append({
        "name": auth, "type": "scatter", "symbolSize": 16,
        "data": [[float(r["time_to_contain_min"]), float(r["loss_usd"]),
                  float(r["containment_success_pct"])]
                 for _, r in ad.iterrows()],
        "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}
    })
save("chart39_risk_matrix_scatter", {
    "title": {"text": "Risk Matrix: Severity vs Response Time"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "log", "name": "Response Time (min)"},
    "yAxis": {"type": "log", "name": "Loss (USD)"},
    "series": series39
})

# ── Chart 40: Success Rate Timeline (line + crisis shading) ──────
sby = metrics.groupby("year")["containment_success_pct"].mean()
cnt = metrics.groupby("year").size()
save("chart40_success_timeline", {
    "title": {"text": "Intervention Success Rate Evolution"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": [int(y) for y in sby.index]},
    "yAxis": {"type": "value", "name": "Success (%)", "max": 110},
    "series": [{
        "type": "line", "symbol": "circle", "symbolSize": 10,
        "lineStyle": {"color": C["green"], "width": 3},
        "itemStyle": {"color": C["green"]},
        "areaStyle": {"color": C["green"], "opacity": 0.1},
        "data": [round(float(v), 1) for v in sby.values],
        "label": {"show": True, "position": "top",
                  "formatter": "{c}%"}
    }],
    "markArea": {"data": [
        [{"xAxis": "2022", "itemStyle": {"color": C["red"], "opacity": 0.08}},
         {"xAxis": "2024"}],
        [{"xAxis": "2025", "itemStyle": {"color": C["green"], "opacity": 0.08}},
         {"xAxis": "2025"}]
    ]} if False else None  # markArea goes in series
})
# Rebuild with markArea inside the series
save("chart40_success_timeline", {
    "title": {"text": "Intervention Success Rate Evolution"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": [int(y) for y in sby.index]},
    "yAxis": {"type": "value", "name": "Success (%)", "max": 110},
    "series": [{
        "type": "line", "symbol": "circle", "symbolSize": 10,
        "lineStyle": {"color": C["green"], "width": 3},
        "itemStyle": {"color": C["green"]},
        "areaStyle": {"color": C["green"], "opacity": 0.1},
        "data": [round(float(v), 1) for v in sby.values],
        "label": {"show": True, "position": "top", "formatter": "{c}%"},
        "markArea": {"data": []}
    }]
})

# ── Chart 41: Success Timeline by Case (scatter w/ annotations) ──
ms = metrics.sort_values("date")
series41 = []
for auth in ms["authority"].unique():
    ad = ms[ms["authority"] == auth]
    series41.append({
        "name": f"{auth} (n={len(ad)})", "type": "scatter", "symbolSize": 12,
        "data": [[r["date"].isoformat(), float(r["containment_success_pct"]),
                  r.get("incident_id","")]
                 for _, r in ad.iterrows()],
        "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}
    })
save("chart41_success_timeline_case", {
    "title": {"text": "Case-Level Success Timeline by Authority"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "time"},
    "yAxis": {"type": "value", "name": "Success (%)", "min": -5, "max": 115},
    "series": series41
})

# ── Chart 42: Detection vs Containment Detailed (scatter) ────────
sc42 = metrics[["time_to_detect_min","time_to_contain_min","authority","incident_id"]].dropna()
series42 = []
for auth in sc42["authority"].unique():
    ad = sc42[sc42["authority"] == auth]
    series42.append({
        "name": auth, "type": "scatter", "symbolSize": 14,
        "data": [[float(r["time_to_detect_min"]), float(r["time_to_contain_min"]),
                  r["incident_id"]]
                 for _, r in ad.iterrows()],
        "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}
    })
save("chart42_detect_vs_contain_detailed", {
    "title": {"text": "Detection vs Containment Time Analysis"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "log", "name": "Detection (min)"},
    "yAxis": {"type": "log", "name": "Containment (min)"},
    "series": series42
})

print("\n✅ Batch 4 complete (charts 37-42)")
