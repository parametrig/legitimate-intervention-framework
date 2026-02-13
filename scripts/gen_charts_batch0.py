"""Batch 0: Charts 01-11 (Market overview & attack anatomy)."""
from gen_charts_shared import *
import numpy as np

exploits, interventions, metrics, combined = load_data()
exploits["vector_category"] = exploits["vector_category"].fillna("")

# ── Chart 01: Annual Exploit Losses ───────────────────────────────
yl = exploits.groupby("year")["loss_usd"].sum().sort_index() / 1e9
save("chart01_annual_losses", {
    "title": {"text": "Annual Exploit Losses"},
    "tooltip": {"trigger": "axis", "valueFormatter": "${value}B"},
    "xAxis": {"type": "category", "data": [int(y) for y in yl.index]},
    "yAxis": {"type": "value", "name": "Loss ($B)",
              "axisLabel": {"formatter": "${value}B"}},
    "series": [{
        "type": "bar",
        "data": [{"value": round(float(v), 2),
                  "itemStyle": {"color": C["lblue"]}} for v in yl.values],
        "label": {"show": True, "position": "top", "formatter": "${c}B"}
    }, {
        "type": "line",
        "data": [round(float(v), 2) for v in yl.values],
        "symbol": "circle", "symbolSize": 8,
        "lineStyle": {"color": C["blue"], "width": 2},
        "itemStyle": {"color": C["blue"]}
    }]
})

# ── Chart 02: Cumulative Losses (Total / Technical / LIF) ─────────
def get_cum(df):
    return df.groupby("year")["loss_usd"].sum().sort_index().cumsum() / 1e9

cum_tot = get_cum(exploits)
cum_tech = get_cum(exploits[~exploits["vector_category"].str.contains("Systemic|Economic", case=False)])
cum_lif = get_cum(exploits[exploits["is_lif_relevant"] == True])

years = sorted(list(set(cum_tot.index) | set(cum_tech.index) | set(cum_lif.index)))
# reindex/fill
cum_tot = cum_tot.reindex(years).ffill().fillna(0)
cum_tech = cum_tech.reindex(years).ffill().fillna(0)
cum_lif = cum_lif.reindex(years).ffill().fillna(0)

save("chart02_cumulative_losses", {
    "title": {"text": "Cumulative Exploit Losses"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["Total Market", "Technical Addressable", "LIF-Relevant"], "bottom": 0},
    "xAxis": {"type": "category", "data": [int(y) for y in years]},
    "yAxis": {"type": "value", "name": "Cumulative ($B)",
              "axisLabel": {"formatter": "${value}B"}},
    "series": [
        {"name": "Total Market", "type": "line", "stack": "x", "areaStyle": {},
         "data": [round(float(v), 2) for v in cum_tot.values],
         "itemStyle": {"color": C["blue"], "opacity": 0.2}},
        {"name": "Technical Addressable", "type": "line", "stack": "x", "areaStyle": {}, # actually layers are distinct, not stacked in val
         # Matplotlib code implies they are overlaid (z-ordered), not stacked. ECharts areaStyle behavior:
         # To overlay, do NOT use 'stack'.
         "data": [round(float(v), 2) for v in cum_tech.values],
         "itemStyle": {"color": C["amber"], "opacity": 0.4}},
        {"name": "LIF-Relevant", "type": "line", "areaStyle": {},
         "data": [round(float(v), 2) for v in cum_lif.values],
         "itemStyle": {"color": C["green"], "opacity": 0.6}}
    ]
})
# Fix: chart02 series types should NOT have 'stack' if we want overlay. 
# Re-save with stack removed for overlay effect.
save("chart02_cumulative_losses", {
    "title": {"text": "Cumulative Exploit Losses"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["Total Market", "Technical Addressable", "LIF-Relevant"], "bottom": 0},
    "xAxis": {"type": "category", "data": [int(y) for y in years]},
    "yAxis": {"type": "value", "name": "Cumulative ($B)",
              "axisLabel": {"formatter": "${value}B"}},
    "series": [
        {"name": "Total Market", "type": "line", "areaStyle": {},
         "data": [round(float(v), 2) for v in cum_tot.values],
         "itemStyle": {"color": C["blue"]}, "lineStyle": {"width": 0}, "areaStyle": {"opacity": 0.15}},
        {"name": "Technical Addressable", "type": "line", "areaStyle": {},
         "data": [round(float(v), 2) for v in cum_tech.values],
         "itemStyle": {"color": C["amber"]}, "lineStyle": {"width": 0}, "areaStyle": {"opacity": 0.3}},
        {"name": "LIF-Relevant", "type": "line", "areaStyle": {},
         "data": [round(float(v), 2) for v in cum_lif.values],
         "itemStyle": {"color": C["green"]}, "lineStyle": {"width": 2}, "areaStyle": {"opacity": 0.5}}
    ]
})

# ── Chart 03: Top 20 Losses (Magnitude) ───────────────────────────
top20 = exploits.nlargest(20, "loss_usd").sort_values("loss_usd", ascending=True)
save("chart03_top20_magnitude", {
    "title": {"text": "Top 20 Historical Losses"},
    "tooltip": {"trigger": "axis", "valueFormatter": "${value}B"},
    "xAxis": {"type": "value", "name": "Loss ($B)"},
    "yAxis": {"type": "category", "data": top20["protocol"].tolist()},
    "series": [{
        "type": "bar",
        "data": [{"value": round(float(x/1e9), 2),
                  "itemStyle": {"color": C["red"] if i==len(top20)-1 else C["slate"]}}
                 for i, x in enumerate(top20["loss_usd"])],
        "label": {"show": True, "position": "right", "formatter": "${c}B"}
    }]
})

# ── Chart 04: Relevance Pie Charts ────────────────────────────────
# For ECharts, we can do 2 series (nested or side-by-side using center/radius)
# or just separate charts. Let's do 2 pie series in one chart (side-by-side).
total_val = exploits["loss_usd"].sum()
lif_val = exploits[exploits["is_lif_relevant"] == True]["loss_usd"].sum()
tech_val = exploits[~exploits["vector_category"].str.contains("Systemic|Economic", case=False)]["loss_usd"].sum()
# Breakdown: LIF vs Potential (Tech-LIF) vs Non-Addressable (Total-Tech)
v_lif = lif_val
v_pot = tech_val - lif_val
v_non = total_val - tech_val

c_total = len(exploits)
c_lif = len(exploits[exploits["is_lif_relevant"] == True])
c_tech = len(exploits[~exploits["vector_category"].str.contains("Systemic|Economic", case=False)])
c_pot = c_tech - c_lif
c_non = c_total - c_tech

colors04 = [C["green"], C["amber"], C["slate"]] # LIF, Potential, Systemic

save("chart04_relevance_pie", {
    "title": [
        {"text": "By Count", "left": "25%", "top": "5%", "textAlign": "center"},
        {"text": "By Value", "left": "75%", "top": "5%", "textAlign": "center"}
    ],
    "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
    "legend": {"bottom": 0, "data": ["LIF-Relevant", "Potential Technical", "Systemic/Social"]},
    "series": [
        {
            "type": "pie", "radius": "50%", "center": ["25%", "55%"],
            "data": [
                {"value": int(c_lif), "name": "LIF-Relevant", "itemStyle": {"color": colors04[0]}},
                {"value": int(c_pot), "name": "Potential Technical", "itemStyle": {"color": colors04[1]}},
                {"value": int(c_non), "name": "Systemic/Social", "itemStyle": {"color": colors04[2]}},
            ],
            "label": {"formatter": "{b}\n{c} ({d}%)"}
        },
        {
            "type": "pie", "radius": "50%", "center": ["75%", "55%"],
            "data": [
                {"value": round(v_lif/1e9, 1), "name": "LIF-Relevant", "itemStyle": {"color": colors04[0]}},
                {"value": round(v_pot/1e9, 1), "name": "Potential Technical", "itemStyle": {"color": colors04[1]}},
                {"value": round(v_non/1e9, 1), "name": "Systemic/Social", "itemStyle": {"color": colors04[2]}},
            ],
             "label": {"formatter": "{b}\n${c}B ({d}%)"}
        }
    ]
})

# ── Chart 05: Loss Distribution (Histogram) ───────────────────────
# ECharts doesn't compute histograms; we prepare bins.
vals = np.log10(exploits[exploits["loss_usd"]>0]["loss_usd"])
counts, edges = np.histogram(vals, bins=30)
# edges are 10^x
bin_labels = [f"10^{x:.1f}" for x in edges[:-1]]

save("chart05_loss_distribution", {
    "title": {"text": "Loss Distribution (Log Scale)"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": bin_labels, "name": "Log Loss (USD)"},
    "yAxis": {"type": "value", "name": "Count"},
    "series": [{
        "type": "bar",
        "data": [int(x) for x in counts],
        "itemStyle": {"color": C["purple"], "opacity": 0.7},
        "markPoint": {
            "data": [{"coord": [25, counts[25]], "value": "Pareto Zone"}]
        } # approximate
    }]
})

# ── Chart 06: Lorenz Curve ────────────────────────────────────────
def get_lorenz(df):
    s = df["loss_usd"].sort_values(ascending=False).values
    cum_loss_pct = np.cumsum(s) / s.sum() * 100
    cum_inc_pct = np.arange(1, len(s)+1) / len(s) * 100
    # Downsample for web
    indices = np.linspace(0, len(s)-1, 100, dtype=int)
    return [[round(cum_inc_pct[i],1), round(cum_loss_pct[i],1)] for i in indices]

l_tot = get_lorenz(exploits)
l_tech = get_lorenz(exploits[~exploits["vector_category"].str.contains("Systemic|Economic", case=False)])

save("chart06_loss_concentration_lorenz", {
    "title": {"text": "Loss Concentration (Lorenz Curve)"},
    "tooltip": {"trigger": "axis"},
    "legend": {"bottom": 0, "data": ["Total Market", "Technical Only"]},
    "xAxis": {"type": "value", "name": "% of Incidents", "max": 100},
    "yAxis": {"type": "value", "name": "% of Total Loss", "max": 100},
    "series": [
        {"name": "Total Market", "type": "line", "data": l_tot,
         "showSymbol": False, "itemStyle": {"color": C["slate"]}, "lineStyle": {"width": 3}},
        {"name": "Technical Only", "type": "line", "data": l_tech,
         "showSymbol": False, "itemStyle": {"color": C["purple"]}, "lineStyle": {"width": 3}},
        { # Reference lines 80/20
          "type": "line", "markLine": {
              "data": [{"yAxis": 80, "label": {"formatter": "80% Loss"}}]
          }
        }
    ]
})

# ── Chart 07: Median Loss Comparison ──────────────────────────────
meds = [
    {"name": "All Interventions", "val": interventions["loss_usd"].median()},
    {"name": "LIF-Relevant", "val": exploits[exploits["is_lif_relevant"]]["loss_usd"].median()},
    {"name": "High-Fidelity Metrics", "val": metrics["loss_usd"].median()},
]
save("chart07_median_loss", {
    "title": {"text": "Median Loss by Subset"},
    "tooltip": {"trigger": "axis", "valueFormatter": "${value}M"},
    "xAxis": {"type": "category", "data": [d["name"] for d in meds]},
    "yAxis": {"type": "value", "name": "Median Loss (USD)"},
    "series": [{
        "type": "bar",
        "data": [{"value": round(d["val"]/1e6, 2),
                  "itemStyle": {"color": C["purple"]}} for d in meds],
        "label": {"show": True, "position": "top", "formatter": "${c}M"}
    }]
})

# ── Chart 08: Four Layer Timeline ─────────────────────────────────
# Stacked area: Intervened -> Eligible-Not -> Other -> Systemic
groups = []
years08 = sorted(exploits["year"].unique())
for y in years08:
    sub = exploits[exploits["year"] == y]
    # Layer 1: Actually Intervened
    l1 = sub[(sub["is_lif_relevant"]) & (sub.get("is_intervention",False))]["loss_usd"].sum()
    # Layer 2: Eligible Not Intervened
    l2 = sub[(sub["is_lif_relevant"]) & (~sub.get("is_intervention",False))]["loss_usd"].sum()
    # Layer 3: Other Non-Addressable
    l3 = sub[(~sub["is_lif_relevant"]) & (~sub["vector_category"].str.contains("Systemic", case=False))]["loss_usd"].sum()
    # Layer 4: Systemic
    l4 = sub[(~sub["is_lif_relevant"]) & (sub["vector_category"].str.contains("Systemic", case=False))]["loss_usd"].sum()
    groups.append([l1, l2, l3, l4])

garr = np.array(groups) / 1e9
layer_names = ["Actually Intervened", "Eligible (Missed)", "Other Non-Addressable", "Systemic Failures"]
layer_colors = [C["green"], C["blue"], C["lgray"], C["slate"]]

save("chart08_four_layer_timeline", {
    "title": {"text": "Annual DeFi Losses by Category"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": layer_names[::-1], "bottom": 0}, # reverse for visual order
    "xAxis": {"type": "category", "data": [int(y) for y in years08]},
    "yAxis": {"type": "value", "name": "Loss ($B)"},
    "series": [
        {"name": name, "type": "line", "stack": "total", "areaStyle": {},
         "itemStyle": {"color": layer_colors[i]},
         "data": [round(v,2) for v in garr[:,i]]}
        for i, name in enumerate(layer_names)
    ]
})

# ── Chart 09: Vector Distribution (Count) ─────────────────────────
vc = exploits["vector_category"].value_counts().head(10)
save("chart09_vector_distribution", {
    "title": {"text": "Top 10 Attack Vectors (Frequency)"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "value", "name": "Count"},
    "yAxis": {"type": "category", "data": vc.index.tolist(), "inverse": True},
    "series": [{
        "type": "bar",
        "data": [{"value": int(v), "itemStyle": {"color": C["blue"] if i==0 else C["slate"]}}
                 for i, v in enumerate(vc.values)],
        "label": {"show": True, "position": "right"}
    }]
})

# ── Chart 10: Vector Losses (Value) ───────────────────────────────
# Special handling for Terra in 'Economic/Systemic'
vl = exploits.groupby("vector_category")["loss_usd"].sum().sort_values(ascending=False).head(10) / 1e9
# Split Terra/Luna manually for visual (simple approach: just stacked bar for that cat)
terra_cat = "Economic / Systemic Failure"
terra_val = 40.0
series10 = []
cats10 = vl.index.tolist()
# Setup 2 series: Base and Terra-Overlay
base_data = []
terra_data = []

for c in cats10:
    val = vl[c]
    if c == terra_cat and val >= terra_val:
        base_data.append(round(val - terra_val, 2))
        terra_data.append(terra_val)
    else:
        base_data.append(round(val, 2))
        terra_data.append(0)

save("chart10_vector_losses", {
    "title": {"text": "Top Attack Vectors (Total Loss)"},
    "tooltip": {"trigger": "axis", "valueFormatter": "${value}B"},
    "legend": {"data": ["Standard Loss", "Terra/Luna Outlier"], "bottom": 0},
    "xAxis": {"type": "value", "name": "Loss ($B)"},
    "yAxis": {"type": "category", "data": cats10, "inverse": True},
    "series": [
        {"name": "Standard Loss", "type": "bar", "stack": "total",
         "data": base_data, "itemStyle": {"color": C["slate"]}},
        {"name": "Terra/Luna Outlier", "type": "bar", "stack": "total",
         "data": terra_data, "itemStyle": {"color": C["red"]}}
    ]
})

# ── Chart 11: Chain Losses ────────────────────────────────────────
cl = exploits.groupby("chain")["loss_usd"].sum().sort_values(ascending=False).head(5) / 1e9
cats11 = cl.index.tolist()
base11 = []
terra11 = []
for c in cats11:
    val = cl[c]
    if c == "Terra":
        base11.append(round(val - terra_val, 2))
        terra11.append(terra_val)
    else:
        base11.append(round(val, 2))
        terra11.append(0)

save("chart11_chain_distribution", {
    "title": {"text": "Losses by Chain"},
    "tooltip": {"trigger": "axis", "valueFormatter": "${value}B"},
    "xAxis": {"type": "value", "name": "Loss ($B)"},
    "yAxis": {"type": "category", "data": cats11, "inverse": True},
    "series": [
        {"name": "Standard Loss", "type": "bar", "stack": "total",
         "data": base11, "itemStyle": {"color": C["slate"]}},
        {"name": "Terra/Luna Outlier", "type": "bar", "stack": "total",
         "data": terra11, "itemStyle": {"color": C["red"]}}
    ]
})

print("\n✅ Batch 0 complete (charts 01-11)")
