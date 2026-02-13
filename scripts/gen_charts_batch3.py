"""Batch 3: Charts 28-35 (Taxonomy matrices & effectiveness)."""
from gen_charts_shared import *

exploits, interventions, metrics, combined = load_data()

# ── Chart 28: Scope × Authority Matrix Heatmap ────────────────────
mx = combined.pivot_table(index="scope", columns="authority",
    values="incident_id", aggfunc="count", fill_value=0)
mx = mx.reindex(index=SCOPE_ORDER, columns=AUTHORITY_ORDER, fill_value=0)
save("chart28_matrix_heatmap_combined", {
    "title": {"text": "LIF Matrix: Scope × Authority"},
    "tooltip": {"position": "top"},
    "xAxis": {"type": "category", "data": AUTHORITY_ORDER, "splitArea": {"show": True}},
    "yAxis": {"type": "category", "data": SCOPE_ORDER, "splitArea": {"show": True}},
    "visualMap": {"min": 0, "max": int(mx.values.max()), "calculable": True,
                  "orient": "horizontal", "left": "center", "bottom": 0,
                  "inRange": {"color": ["#f0fdf4","#bbf7d0","#4ade80","#16a34a","#166534"]}},
    "series": [{"type": "heatmap",
        "data": [[AUTHORITY_ORDER.index(a), SCOPE_ORDER.index(s), int(mx.loc[s,a])]
                 for s in SCOPE_ORDER for a in AUTHORITY_ORDER if a in mx.columns],
        "label": {"show": True}, "emphasis": {"itemStyle": {"shadowBlur": 10}}}]
})

# ── Chart 29: Intervention Value by Scope (strip → scatter) ──────
save("chart29_intervention_value_combined", {
    "title": {"text": "Prevented Value by Intervention Scope"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "category", "data": SCOPE_ORDER},
    "yAxis": {"type": "log", "name": "Loss Prevented (USD)",
              "axisLabel": {"formatter": "${value}"}},
    "series": [{
        "type": "scatter", "symbolSize": 10,
        "data": [{"value": [r["scope"], float(r["loss_prevented_usd"])],
                  "itemStyle": {"color": AUTH_COLORS.get(r.get("authority_standardized",""), C["gray"])}}
                 for _, r in combined[combined["loss_prevented_usd"] > 0].iterrows()
                 if r["scope"] in SCOPE_ORDER]
    }]
})

# ── Chart 30: Scope vs Loss (boxplot → simplified) ────────────────
box_data = []
for scope in SCOPE_ORDER:
    vals = interventions[interventions["scope"] == scope]["loss_usd"].dropna()
    if len(vals) > 0:
        q = vals.quantile([0, 0.25, 0.5, 0.75, 1]).tolist()
        box_data.append([round(v, 0) for v in q])
    else:
        box_data.append([0,0,0,0,0])
save("chart30_scope_loss", {
    "title": {"text": "Loss Distribution by Scope"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "category", "data": SCOPE_ORDER},
    "yAxis": {"type": "log", "name": "Loss (USD)", "min": 1000},
    "series": [{"type": "boxplot", "data": box_data,
                "itemStyle": {"color": C["blue"], "borderColor": C["slate"]}}]
})

# ── Chart 31: Scope Evolution Heatmap ──────────────────────────────
se = combined.pivot_table(index="scope", columns="year",
    values="incident_id", aggfunc="count", fill_value=0)
se = se.reindex(SCOPE_ORDER, fill_value=0)
yrs31 = sorted([int(y) for y in se.columns])
save("chart31_scope_evolution_combined", {
    "title": {"text": "Precision Evolution (Scope Over Time)"},
    "tooltip": {"position": "top"},
    "xAxis": {"type": "category", "data": yrs31, "splitArea": {"show": True}},
    "yAxis": {"type": "category", "data": SCOPE_ORDER, "splitArea": {"show": True}},
    "visualMap": {"min": 0, "max": int(se.values.max()), "calculable": True,
                  "orient": "horizontal", "left": "center", "bottom": 0,
                  "inRange": {"color": ["#eff6ff","#bfdbfe","#60a5fa","#2563eb","#1e40af"]}},
    "series": [{"type": "heatmap",
        "data": [[yrs31.index(int(y)), SCOPE_ORDER.index(s), int(se.loc[s,y])]
                 for s in SCOPE_ORDER for y in se.columns],
        "label": {"show": True}}]
})

# ── Chart 32: Prevented vs Incurred Scatter ────────────────────────
sc32 = combined[(combined["loss_usd"] > 0) & (combined["loss_prevented_usd"] > 0)]
save("chart32_prevented_vs_incurred_combined", {
    "title": {"text": "Loss Incurred vs. Loss Prevented"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "log", "name": "Loss Incurred (USD)"},
    "yAxis": {"type": "log", "name": "Loss Prevented (USD)"},
    "series": [
        {"name": auth, "type": "scatter", "symbolSize": 14,
         "data": [[float(r["loss_usd"]), float(r["loss_prevented_usd"])]
                  for _, r in sc32[sc32["authority_standardized"]==auth].iterrows()],
         "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}}
        for auth in sc32["authority_standardized"].unique()
    ]
})

# ── Chart 33: Detection vs Containment Scatter ────────────────────
sc33 = metrics[(metrics["time_to_detect_min"] > 0) & (metrics["time_to_contain_min"] > 0)]
save("chart33_speed_scatter_metrics", {
    "title": {"text": "Detection vs. Containment Time"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "log", "name": "Detection (min)"},
    "yAxis": {"type": "log", "name": "Containment (min)"},
    "series": [
        {"name": auth, "type": "scatter", "symbolSize": 14,
         "data": [[float(r["time_to_detect_min"]), float(r["time_to_contain_min"])]
                  for _, r in sc33[sc33["authority"]==auth].iterrows()],
         "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}}
        for auth in sc33["authority"].unique()
    ]
})

# ── Chart 34: Incurred Loss by Authority (bar) ────────────────────
al = combined.groupby("authority")["loss_usd"].sum().sort_values(ascending=False) / 1e9
save("chart34_incurred_loss_by_authority_combined", {
    "title": {"text": "Total Incurred Loss by Authority"},
    "tooltip": {"trigger": "axis", "valueFormatter": "${value}B"},
    "xAxis": {"type": "category", "data": al.index.tolist()},
    "yAxis": {"type": "value", "name": "Loss ($B)"},
    "series": [{
        "type": "bar",
        "data": [{"value": round(float(v), 2),
                  "itemStyle": {"color": AUTH_COLORS.get(a, C["gray"])}}
                 for a, v in al.items()],
        "label": {"show": True, "position": "top", "formatter": "${c}B"}
    }]
})

# ── Chart 35: Prevented Loss by Authority (stacked bar) ──────────
flow_id = "Flow Blockchain_2025-12-27"
base = combined[combined["incident_id"] != flow_id].groupby("authority")["loss_prevented_usd"].sum().sort_values(ascending=False) / 1e9
flow_case = combined[combined["incident_id"] == flow_id]
flow_val = float(flow_case["loss_prevented_usd"].iloc[0] / 1e9) if not flow_case.empty else 0
auths35 = base.index.tolist()
save("chart35_prevented_loss", {
    "title": {"text": "Prevented Loss by Authority"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["Realizable Market","Flow Outlier"], "bottom": 0},
    "xAxis": {"type": "category", "data": auths35},
    "yAxis": {"type": "value", "name": "Capital Saved ($B)"},
    "series": [
        {"name": "Realizable Market", "type": "bar", "stack": "total",
         "data": [{"value": round(float(base[a]), 2),
                   "itemStyle": {"color": AUTH_COLORS.get(a, C["gray"])}}
                  for a in auths35]},
        {"name": "Flow Outlier", "type": "bar", "stack": "total",
         "data": [round(flow_val, 2) if a == "Delegated Body" else 0 for a in auths35],
         "itemStyle": {"color": C["red"], "opacity": 0.3}}
    ]
})

print("\n✅ Batch 3 complete (charts 28-35)")
