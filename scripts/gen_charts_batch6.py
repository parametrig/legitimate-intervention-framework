"""Batch 6: Charts 18, 26, 27, 36, 43, 47, 50 (Remaining charts)."""
from gen_charts_shared import *
import numpy as np

exploits, interventions, metrics, combined = load_data()

# ── Chart 18: Intervention Timeline ───────────────────────────────
# Scatter: Date vs Prevented Value (log), colored by Authority
# Line: Cumulative Prevented Value (linear/log)
# Logic: interventions sorted by date.
interventions["date"] = pd.to_datetime(interventions["date"])
df18 = interventions.sort_values("date").copy()
df18["cumulative_saved"] = df18["loss_prevented_usd"].cumsum()

# ECharts Scatter + Line
series18 = []
# Scatter series for each authority
for auth in AUTHORITY_ORDER:
    sub = df18[df18["authority"] == auth]
    if sub.empty: continue
    data_pts = []
    for _, row in sub.iterrows():
        data_pts.append({
            "value": [
                row["date"].strftime("%Y-%m-%d"),
                row["loss_prevented_usd"] if row["loss_prevented_usd"] > 0 else None,
                row["loss_usd"] # size proxy
            ],
            "itemStyle": {"color": AUTH_COLORS.get(auth, C["slate"])}
        })
    series18.append({
        "name": auth,
        "type": "scatter",
        "symbolSize": 10, # dynamic size in ECharts needs callback or visualMap, keeping simple for now or use function
        # For simplicity in JSON, fixed size or simple mapping if possible.
        # Let's use a fixed decent size or slightly vary if 'symbolSize' can accept value. 
        # Actually ECharts symbolSize can be a function, but we can't serialize that easily.
        # We'll use a visualMap or just fixed size. Let's use fixed size for cleanliness.
        "symbolSize": 10, 
        "data": data_pts,
        "z": 10
    })

# Line series: Cumulative Saved
line_data = [[row["date"].strftime("%Y-%m-%d"), round(row["cumulative_saved"]/1e6, 2)] 
             for _, row in df18.iterrows()]

series18.append({
    "name": "Cumulative Saved ($M)",
    "type": "line",
    "yAxisIndex": 1,
    "showSymbol": False,
    "lineStyle": {"color": C["amber"], "width": 3},
    "data": line_data,
    "z": 5
})

save("chart18_intervention_timeline", {
    "title": {"text": "Intervention Intensity & Growth"},
    "tooltip": {"trigger": "axis"},
    "legend": {"bottom": 0},
    "xAxis": {"type": "time"},
    "yAxis": [
        {"type": "value", "name": "Incident Value ($)", "axisLabel": {"formatter": "${value}"}},
        {"type": "value", "name": "Cumulative Saved ($M)", "axisLabel": {"formatter": "${value}M"}}
    ],
    "series": series18
})

# ── Chart 26: Scope Distribution (Combined) ───────────────────────
sc = combined["scope"].value_counts().reindex(SCOPE_ORDER).fillna(0)
save("chart26_scope_distribution_combined", {
    "title": {"text": "Interventions by Scope"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": sc.index.tolist()},
    "yAxis": {"type": "value", "name": "Count"},
    "series": [{
        "type": "bar",
        "data": [{"value": int(v), "itemStyle": {"color": C["blue"]}} for v in sc.values],
        "label": {"show": True, "position": "top"}
    }]
})

# ── Chart 27: Authority Distribution (Combined) ───────────────────
ac = combined["authority"].value_counts().reindex(AUTHORITY_ORDER).fillna(0)
save("chart27_authority_distribution_combined", {
    "title": {"text": "Interventions by Authority"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": ac.index.tolist()},
    "yAxis": {"type": "value", "name": "Count"},
    "series": [{
        "type": "bar",
        "data": [{"value": int(v), "itemStyle": {"color": C["amber"]}} for v in ac.values],
        "label": {"show": True, "position": "top"}
    }]
})

# ── Chart 36: Success Distribution (Histogram) ────────────────────
# Bins for success rate 0-100
counts, edges = np.histogram(metrics["containment_success_pct"].dropna(), bins=10, range=(0,100))
bin_centers = [(edges[i] + edges[i+1])/2 for i in range(len(counts))]

save("chart36_success_distribution", {
    "title": {"text": "Distribution of Success Rates"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": [f"{int(e)}%" for e in bin_centers]},
    "yAxis": {"type": "value", "name": "Count"},
    "series": [{
        "type": "bar",
        "data": [int(c) for c in counts],
        "itemStyle": {"color": C["green"]},
        "barWidth": "90%"
    }]
})

# ── Chart 43: Success Matrix (Heatmap) ────────────────────────────
sm = metrics.pivot_table(index="scope", columns="authority",
    values="containment_success_pct", aggfunc="mean")
sm = sm.reindex(index=SCOPE_ORDER, columns=AUTHORITY_ORDER)

data43 = []
for i, scope in enumerate(SCOPE_ORDER):
    for j, auth in enumerate(AUTHORITY_ORDER):
        val = sm.loc[scope, auth]
        if not np.isnan(val):
            data43.append([j, i, round(val, 1)])

save("chart43_success_matrix", {
    "title": {"text": "Success Rate Matrix"},
    "tooltip": {"position": "top", "formatter": "{b}: {c}%"},
    "visualMap": {"min": 0, "max": 100, "calculable": True, "orient": "horizontal", "left": "center", "bottom": "0%", "inRange": {"color": [C["red"], C["amber"], C["green"]]}},
    "xAxis": {"type": "category", "data": AUTHORITY_ORDER},
    "yAxis": {"type": "category", "data": SCOPE_ORDER},
    "series": [{
        "type": "heatmap",
        "data": data43,
        "label": {"show": True, "formatter": "{@[2]}%"}
    }]
})

# ── Chart 47: Comprehensive LIF Market Analysis ───────────────────
# Stacked bar: Incurred (No Int) | Incurred (With Int) | Prevented
lif_df = exploits[exploits["is_lif_relevant"] == True]
total_prevented = combined["loss_prevented_usd"].sum()
loss_with_int = combined["loss_usd"].sum()
loss_overall = lif_df["loss_usd"].sum()
# Note: Logic from notebook:
# loss_overall is total loss of LIF-relevant exploits.
# combined includes metrics + interventions.
# loss_without_intervention = max(0, loss_overall - loss_with_intervention)
# Actually, notebook logic: "loss_without_intervention = max(0, loss_overall - loss_with_intervention)"
# This assumes 'loss_overall' includes the losses from intervention cases? Yes, exploits df has valid cases.
loss_without_int = max(0, loss_overall - loss_with_int)

vals = [loss_without_int, loss_with_int, total_prevented]
names = ["Incurred (No Intervention)", "Incurred (Despite Intervention)", "Successfully Prevented"]
colors = [C["amber"], C["red"], C["green"]]

save("chart47_comprehensive_lif_analysis", {
    "title": {"text": "Comprehensive LIF Market Analysis"},
    "tooltip": {"trigger": "item", "valueFormatter": "${value}B"},
    "legend": {"data": names, "bottom": 0},
    "xAxis": {"type": "category", "data": ["LIF Market"]},
    "yAxis": {"type": "value", "name": "Value ($B)", "axisLabel": {"formatter": "${value}B"}},
    "series": [
        {"name": names[0], "type": "bar", "stack": "total", "data": [round(vals[0]/1e9, 2)], "itemStyle": {"color": colors[0]}, "label": {"show": True, "formatter": "${c}B"}},
        {"name": names[1], "type": "bar", "stack": "total", "data": [round(vals[1]/1e9, 2)], "itemStyle": {"color": colors[1]}, "label": {"show": True, "formatter": "${c}B"}},
        {"name": names[2], "type": "bar", "stack": "total", "data": [round(vals[2]/1e9, 2)], "itemStyle": {"color": colors[2]}, "label": {"show": True, "formatter": "${c}B"}}
    ]
})

# ── Chart 50: Loss Prevented vs Incurred by Authority ─────────────
# Grouped bar
astats = combined.groupby("authority").agg({
    "loss_usd": "sum",
    "loss_prevented_usd": "sum"
}).sort_values("loss_usd", ascending=False)
cats50 = astats.index.tolist()
v_inc = (astats["loss_usd"] / 1e6).round(1).tolist()
v_prev = (astats["loss_prevented_usd"] / 1e6).round(1).tolist()

save("chart50_loss_prevented_vs_incurred", {
    "title": {"text": "Loss Prevented vs Incurred by Authority"},
    "tooltip": {"trigger": "axis", "valueFormatter": "${value}M"},
    "legend": {"data": ["Loss Incurred", "Loss Prevented"], "bottom": 0},
    "xAxis": {"type": "category", "data": cats50},
    "yAxis": {"type": "value", "name": "Value ($M)", "axisLabel": {"formatter": "${value}M"}},
    "series": [
        {"name": "Loss Incurred", "type": "bar", "data": v_inc, "itemStyle": {"color": LOSS_COLORS["Incurred"]}, "label": {"show": True, "position": "top", "formatter": "${c}M"}},
        {"name": "Loss Prevented", "type": "bar", "data": v_prev, "itemStyle": {"color": LOSS_COLORS["Saved"]}, "label": {"show": True, "position": "top", "formatter": "${c}M"}}
    ]
})

print("\n✅ Batch 6 complete (charts 18, 26, 27, 36, 43, 47, 50)")
