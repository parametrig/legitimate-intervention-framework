"""Batch 1: Charts 12-17 (Attack Anatomy advanced charts)."""
from gen_charts_shared import *

exploits, interventions, metrics, combined = load_data()
exploits["vector_category"] = exploits["vector_category"].fillna("")

# ── Chart 12: Vector Evolution (stacked area) ──────────────────────
top5 = exploits["vector_category"].value_counts().head(5).index.tolist()
evo = (exploits[exploits["vector_category"].isin(top5)]
       .groupby(["year","vector_category"]).size().unstack(fill_value=0)
       .sort_index())
evo = evo[evo.index >= 2018]
colors = [C["blue"], C["purple"], C["green"], C["amber"], C["red"]]
save("chart12_vector_evolution", {
    "title": {"text": "Evolution of Top 5 Attack Vectors"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": top5, "bottom": 0},
    "xAxis": {"type": "category", "data": [int(y) for y in evo.index]},
    "yAxis": {"type": "value", "name": "Incidents"},
    "series": [
        {"name": v, "type": "line", "stack": "total", "areaStyle": {"opacity": 0.6},
         "data": evo[v].tolist(), "itemStyle": {"color": colors[i]}}
        for i, v in enumerate(top5) if v in evo.columns
    ]
})

# ── Chart 13: Macro Timeline (monthly frequency line) ──────────────
monthly = exploits.groupby("date").size().resample("ME").sum()
save("chart13_macro_timeline", {
    "title": {"text": "Monthly Exploit Frequency (2011–2025)"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category",
              "data": [d.strftime("%Y-%m") for d in monthly.index],
              "axisLabel": {"interval": 11}},
    "yAxis": {"type": "value", "name": "Incidents / Month"},
    "series": [{
        "type": "line", "data": monthly.values.tolist(),
        "areaStyle": {"color": C["lblue"], "opacity": 0.3},
        "lineStyle": {"color": C["blue"], "width": 2},
        "itemStyle": {"color": C["blue"]}, "symbol": "none"
    }]
})

# ── Chart 14: Seasonal Patterns (dual-axis month chart) ────────────
noTerra = exploits[~exploits["protocol"].str.contains("Terra", case=False, na=False)]
mp = noTerra.groupby(noTerra["date"].dt.month).agg(
    count=("loss_usd","count"), total_loss=("loss_usd","sum")).reset_index()
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
save("chart14_pattern_temporal", {
    "title": {"text": "Seasonal Patterns (Excl. Terra/Luna)"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["Exploit Count", "Total Loss ($B)"], "bottom": 0},
    "xAxis": {"type": "category", "data": months},
    "yAxis": [
        {"type": "value", "name": "Count", "position": "left"},
        {"type": "value", "name": "Loss ($B)", "position": "right",
         "axisLabel": {"formatter": "${value}B"}}
    ],
    "series": [
        {"name": "Exploit Count", "type": "line", "data": mp["count"].tolist(),
         "itemStyle": {"color": C["blue"]}, "symbol": "circle", "symbolSize": 8},
        {"name": "Total Loss ($B)", "type": "bar", "yAxisIndex": 1,
         "data": (mp["total_loss"]/1e9).round(2).tolist(),
         "itemStyle": {"color": C["red"], "opacity": 0.3}}
    ]
})

# ── Chart 15: Timeline Heatmap (year × month) ─────────────────────
hd = exploits[exploits["date"].notna()].copy()
hd["month"] = hd["date"].dt.month
ht = hd[hd["year"] >= 2017].pivot_table(
    index="year", columns="month", values="protocol", aggfunc="count", fill_value=0)
ht = ht.reindex(columns=range(1,13), fill_value=0)
years_list = sorted(ht.index.tolist())
save("chart15_timeline_heatmap_x_month", {
    "title": {"text": "Exploit Density: Month × Year (2017+)"},
    "tooltip": {"position": "top"},
    "xAxis": {"type": "category", "data": months, "splitArea": {"show": True}},
    "yAxis": {"type": "category", "data": [int(y) for y in years_list],
              "splitArea": {"show": True}},
    "visualMap": {"min": 0, "max": int(ht.values.max()),
                  "calculable": True, "orient": "horizontal",
                  "left": "center", "bottom": 0,
                  "inRange": {"color": ["#fff5f5","#fee2e2","#fca5a5","#f87171","#ef4444","#dc2626","#991b1b"]}},
    "series": [{
        "type": "heatmap",
        "data": [[m-1, years_list.index(y), int(ht.loc[y,m])]
                 for y in years_list for m in range(1,13)],
        "label": {"show": True}, "emphasis": {"itemStyle": {"shadowBlur": 10}}
    }]
})

# ── Chart 16: Sophistication Timeline (major exploits scatter) ─────
big = exploits[exploits["loss_usd"] > 100_000_000].sort_values("date").tail(15)
save("chart16_sophistication_timeline", {
    "title": {"text": "Major Exploits (>$100M) Timeline"},
    "tooltip": {"trigger": "item",
                "formatter": "{b}: ${c}"},
    "xAxis": {"type": "time"},
    "yAxis": {"type": "log", "name": "Loss USD (Log)",
              "axisLabel": {"formatter": "${value}"}},
    "series": [{
        "type": "scatter", "symbolSize": 18,
        "data": [[r["date"].isoformat(), float(r["loss_usd"]), r["protocol"]]
                 for _, r in big.iterrows()],
        "itemStyle": {"color": C["amber"]},
        "label": {"show": True, "formatter": "{@[2]}", "position": "top", "fontSize": 9}
    }]
})

# ── Chart 17: Risk Matrix (frequency × severity scatter) ──────────
vs = exploits.groupby("vector_category").agg(
    freq=("protocol","count"), avg_sev=("loss_usd","mean")).reset_index()
vs = vs[vs["freq"] > 0]
save("chart17_risk_matrix", {
    "title": {"text": "Risk Matrix: Frequency vs. Severity"},
    "tooltip": {"trigger": "item",
                "formatter": "{b}<br/>Frequency: {@[0]}<br/>Avg Loss: ${@[1]}"},
    "xAxis": {"type": "log", "name": "Frequency", "min": 1},
    "yAxis": {"type": "log", "name": "Avg Severity (USD)", "min": 10000,
              "axisLabel": {"formatter": "${value}"}},
    "series": [{
        "type": "scatter",
        "data": [[int(r["freq"]), float(r["avg_sev"]), r["vector_category"].split("/")[0].strip()]
                 for _, r in vs.iterrows()],
        "symbolSize": 20,
        "itemStyle": {"color": C["amber"]},
        "label": {"show": True, "formatter": "{@[2]}", "position": "right", "fontSize": 9}
    }]
})

print("\n✅ Batch 1 complete (charts 12-17)")
