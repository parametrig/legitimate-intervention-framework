from gen_charts_shared import *

exploits, interventions, metrics, combined = load_data()

print(f"Loaded {len(metrics)} intervention metrics for Batch 4")

# ── Chart 37: Response Time (box/bar) ──────────────────────────
sc37 = metrics[["authority", "time_to_contain_min"]].dropna()
# Simple mean bar for now as per previous version
stats37 = sc37.groupby("authority")["time_to_contain_min"].mean()
save("chart37_response_time", {
    "title": {"text": "Mean Response Time by Authority"},
    "tooltip": {"trigger": "axis", "valueFormatter": "{value} min"},
    "xAxis": {"type": "category", "data": [a for a in AUTHORITY_ORDER if a in stats37]},
    "yAxis": {"type": "log", "name": "Minutes (Log)"},
    "series": [{
        "type": "bar",
        "data": [{"value": round(float(stats37[a]), 1),
                  "itemStyle": {"color": AUTH_COLORS.get(a, C["gray"])}}
                 for a in AUTHORITY_ORDER if a in stats37]
    }]
})

# ── Chart 38: Success Rate vs Response Time (scatter) ──────────
sc38 = metrics[["time_to_contain_min","containment_success_pct","authority"]].dropna()
series38 = []
for auth in sc38["authority"].unique():
    ad = sc38[sc38["authority"] == auth]
    series38.append({
        "name": auth, "type": "scatter", "symbolSize": 14,
        "data": [[max(1.0, float(r["time_to_contain_min"])), float(r["containment_success_pct"])] 
                 for _, r in ad.iterrows()],
        "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}
    })
save("chart38_success_vs_time", {
    "title": {"text": "Success Rate vs. Response Time"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "log", "name": "Response Time (min)"},
    "yAxis": {"type": "value", "name": "Success Rate (%)", "max": 110},
    "series": series38
})

# ── Chart 39: Risk Matrix Scatter (loss × time × success) ────────
sc39 = metrics[["time_to_contain_min","loss_usd","containment_success_pct","authority","incident_id"]].dropna()
series39 = []
for auth in sc39["authority"].unique():
    ad = sc39[sc39["authority"]==auth]
    series39.append({
        "name": auth, "type": "scatter", "symbolSize": 16,
        "data": [[max(1.0, float(r["time_to_contain_min"])), 
                  max(1.0, float(r["loss_usd"])),
                  float(r["containment_success_pct"]),
                  r["incident_id"]]
                 for _, r in ad.iterrows()],
        "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}
    })
save("chart39_risk_matrix_scatter", {
    "title": {"text": "Risk Matrix: Severity vs Response Time"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "log", "name": "Response Time (min)"},
    "yAxis": {"type": "log", "name": "Loss ($)"},
    "series": series39
})

# ── Chart 40: Success Rate Timeline (line) ─────────────────────
daily_success = metrics.groupby("date")["containment_success_pct"].mean().rolling(window=5, min_periods=1).mean()
save("chart40_success_timeline", {
    "title": {"text": "Intervention Success Reliability"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "time"},
    "yAxis": {"type": "value", "name": "Success Rate (%)", "min": 0, "max": 100},
    "series": [{
        "name": "5-Incident Moving Avg",
        "type": "line",
        "data": [[pd.to_datetime(d).strftime("%Y-%m-%d"), round(float(v), 1)] for d, v in daily_success.items() if not pd.isna(v)],
        "smooth": True,
        "lineStyle": {"width": 3, "color": C["blue"]},
        "areaStyle": {"opacity": 0.1}
    }]
})

# ── Chart 41: Case-by-Case Reliability (scatter) ───────────────
series41 = []
for auth in metrics["authority"].unique():
    ad = metrics[metrics["authority"] == auth]
    series41.append({
        "name": auth, "type": "scatter", "symbolSize": 10,
        "data": [[r["date"], float(r["containment_success_pct"])] for _, r in ad.iterrows()],
        "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}
    })
save("chart41_success_timeline_case", {
    "title": {"text": "Case-by-Case Outcome Reliability"},
    "xAxis": {"type": "time"},
    "yAxis": {"type": "value", "name": "Success Rate (%)"},
    "series": series41
})

# ── Chart 42: Efficiency Granularity (scatter) ──────────────────
sc42 = metrics[["time_to_detect_min","time_to_contain_min","authority","incident_id"]].dropna()
series42 = []
for auth in sc42["authority"].unique():
    ad = sc42[sc42["authority"] == auth]
    series42.append({
        "name": auth, "type": "scatter", "symbolSize": 14,
        "data": [[max(1.0, float(r["time_to_detect_min"])), 
                  max(1.0, float(r["time_to_contain_min"])), 
                  r["incident_id"]] 
                 for _, r in ad.iterrows()],
        "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}
    })
save("chart42_detect_vs_contain_detailed", {
    "title": {"text": "Efficiency Granularity"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "log", "name": "Detection (min)"},
    "yAxis": {"type": "log", "name": "Containment (min)"},
    "legend": {"bottom": 0},
    "series": series42
})

print("\n✅ Batch 4 complete (charts 37-41, 42)")
