"""Batch 5: Charts 44-46, 48-49 (Strategic intelligence)."""
from gen_charts_shared import *

exploits, interventions, metrics, combined = load_data()

# ── Chart 44: Enhanced Success Matrix (4-panel → simplified) ──────
# Combined: success rates by scope×authority
sm_comb = combined.pivot_table(index="scope", columns="authority",
    values="containment_success_pct", aggfunc="mean")
sm_comb = sm_comb.reindex(index=SCOPE_ORDER, columns=AUTHORITY_ORDER)
# Count matrix
cm_comb = combined.pivot_table(index="scope", columns="authority",
    values="incident_id", aggfunc="count", fill_value=0)
cm_comb = cm_comb.reindex(index=SCOPE_ORDER, columns=AUTHORITY_ORDER, fill_value=0)

# Build a combined heatmap with annotations showing "rate% (n=count)"
heat_data = []
for si, s in enumerate(SCOPE_ORDER):
    for ai, a in enumerate(AUTHORITY_ORDER):
        rate = sm_comb.loc[s, a] if not pd.isna(sm_comb.loc[s, a]) else -1
        count = int(cm_comb.loc[s, a]) if not pd.isna(cm_comb.loc[s, a]) else 0
        heat_data.append([ai, si, round(float(rate), 1) if rate >= 0 else None, count])

save("chart44_success_matrix_enhanced", {
    "title": {"text": "Success Rate Matrix (All Interventions)"},
    "tooltip": {"position": "top"},
    "xAxis": {"type": "category", "data": AUTHORITY_ORDER, "splitArea": {"show": True}},
    "yAxis": {"type": "category", "data": SCOPE_ORDER, "splitArea": {"show": True}},
    "visualMap": {"min": 0, "max": 100, "calculable": True,
                  "orient": "horizontal", "left": "center", "bottom": 0,
                  "inRange": {"color": ["#fecaca","#fde68a","#bbf7d0","#4ade80","#16a34a"]}},
    "series": [{"type": "heatmap",
        "data": [[d[0], d[1], d[2]] for d in heat_data if d[2] is not None],
        "label": {"show": True, "formatter": "{c}%"},
        "emphasis": {"itemStyle": {"shadowBlur": 10}}}]
})

# ── Chart 45: Effectiveness Leaderboard ───────────────────────────
lb = metrics.groupby("authority").agg(
    avg_success=("containment_success_pct", "mean"),
    avg_speed=("time_to_contain_min", "median"),
    cases=("incident_id", "count"))
lb["speed_score"] = 100 * (1 - lb["avg_speed"] / lb["avg_speed"].max())
lb["composite"] = (lb["avg_success"] * 0.7) + (lb["speed_score"] * 0.3)
lb = lb.sort_values("composite", ascending=True)  # ascending for horizontal bar
save("chart45_effectiveness_leaderboard", {
    "title": {"text": "Effectiveness Leaderboard\n(70% Success + 30% Speed)"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "value", "max": 85, **HIDE_X_NAME},
    "yAxis": {"type": "category", "data": lb.index.tolist()},
    "series": [{
        "type": "bar",
        "data": [{"value": round(float(lb.loc[a, "composite"]), 1),
                  "itemStyle": {"color": AUTH_COLORS.get(a, C["gray"])}}
                 for a in lb.index],
        "label": {"show": True, "position": "right", "formatter": "{c}"}
    }]
})

# ── Chart 46: Risk-Adjusted Performance (scatter) ────────────────
sc46 = metrics[["loss_usd","containment_success_pct","loss_prevented_usd","authority"]].dropna()
series46 = []
for auth in sc46["authority"].unique():
    ad = sc46[sc46["authority"] == auth]
    series46.append({
        "name": auth, "type": "scatter", "symbolSize": 16,
        "data": [[max(1.0, float(r["loss_usd"])), float(r["containment_success_pct"]),
                  float(r.get("loss_prevented_usd", 0))]
                 for _, r in ad.iterrows()],
        "itemStyle": {"color": AUTH_COLORS.get(auth, C["gray"])}
    })
save("chart46_risk_adjusted_performance", {
    "title": {"text": "Performance Under Pressure"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "log", "name": "Value at Risk (USD)"},
    "yAxis": {"type": "value", "name": "Success Rate (%)", "max": 110},
    "series": series46
})

# ── Chart 48: Strategic ROI Rankings (bar) ────────────────────────
roi = {
    "Delegated Body": {"success": 48.6, "speed_hr": 0.87, "cost": 3, "coverage": 80.6},
    "Signer Set":     {"success": 41.2, "speed_hr": 1.57, "cost": 2, "coverage": 80.6},
    "Governance":     {"success": 77.0, "speed_hr": 12.0, "cost": 5, "coverage": 80.6},
    "Automated":      {"success": 0,    "speed_hr": 0.1,  "cost": 4, "coverage": 85.0},
}
max_speed = max(d["speed_hr"] for d in roi.values())
max_cost = max(d["cost"] for d in roi.values())
for d in roi.values():
    d["speed_score"] = 100 * (1 - d["speed_hr"] / max_speed)
    d["cost_score"] = 100 * (1 - d["cost"] / max_cost)
    d["roi"] = d["success"]*0.5 + d["speed_score"]*0.2 + d["cost_score"]*0.2 + d["coverage"]*0.1
sorted_roi = sorted(roi.items(), key=lambda x: x[1]["roi"])  # ascending for hbar
save("chart48_strategic_roi_rankings", {
    "title": {"text": "Strategic ROI Rankings"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "value", "max": 80, **HIDE_X_NAME},
    "yAxis": {"type": "category", "data": [k for k,v in sorted_roi]},
    "series": [{
        "type": "bar",
        "data": [{"value": round(v["roi"], 1),
                  "itemStyle": {"color": AUTH_COLORS.get(k, C["amber"])}}
                 for k, v in sorted_roi],
        "label": {"show": True, "position": "right", "formatter": "{c}"}
    }]
})

# ── Chart 49: ROI by Authority × Scope (bar) ─────────────────────
roi49 = combined.groupby(["authority","scope"]).agg(
    saved=("loss_prevented_usd","sum"), n=("incident_id","count")).reset_index()
roi49["model"] = roi49["authority"] + " × " + roi49["scope"]
roi49 = roi49.sort_values("saved", ascending=True).tail(8)
roi49["saved_m"] = roi49["saved"] / 1e6
save("chart49_roi_magnitude", {
    "title": {"text": "Capital Saved by Intervention Model"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "value", **HIDE_X_NAME},
    "yAxis": {"type": "category", "data": roi49["model"].tolist()},
    "series": [{
        "type": "bar",
        "data": [{"value": round(float(r["saved_m"]), 0),
                  "itemStyle": {"color": AUTH_COLORS.get(r["authority"], C["gray"])},
                  "label": {"show": True, "position": "right",
                            "formatter": f"${r['saved_m']:.0f}M ({int(r['n'])} cases)"}}
                 for _, r in roi49.iterrows()]
    }]
})

print("\n✅ Batch 5 complete (charts 44-46, 48-49)")
