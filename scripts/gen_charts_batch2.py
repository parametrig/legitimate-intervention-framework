"""Batch 2: Charts 19-25 (Intervention evolution & authority analysis)."""
from gen_charts_shared import *

exploits, interventions, metrics, combined = load_data()

# ── Chart 19: Hacks vs Interventions by Year ───────────────────────
yh = exploits[exploits["year"] >= 2016].groupby("year").size()
yi = interventions.groupby("year").size().reindex(yh.index, fill_value=0)
rate = (yi / yh * 100).round(1).fillna(0)
yrs = [int(y) for y in yh.index]
save("chart19_hacks_vs_interventions", {
    "title": {"text": "Exploits vs Intervention Rate"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["Exploits","Interventions","Rate (%)"], "bottom": 0},
    "xAxis": {"type": "category", "data": yrs},
    "yAxis": [
        {"type": "value", "name": "Count"},
        {"type": "value", "name": "Rate (%)", "max": 100,
         "axisLabel": {"formatter": "{value}%"}}
    ],
    "series": [
        {"name": "Exploits", "type": "bar", "data": yh.values.tolist(),
         "itemStyle": {"color": C["slate"], "opacity": 0.4}},
        {"name": "Interventions", "type": "bar", "data": yi.values.tolist(),
         "itemStyle": {"color": C["green"]}},
        {"name": "Rate (%)", "type": "line", "yAxisIndex": 1,
         "data": rate.values.tolist(), "symbol": "circle", "symbolSize": 8,
         "lineStyle": {"color": C["blue"]}, "itemStyle": {"color": C["blue"]}}
    ]
})

# ── Chart 20: Success Rate Timeline (dual metrics) ────────────────
ys = metrics.groupby("year")["containment_success_pct"].mean().dropna()
yc = interventions.groupby("year").agg(
    prev=("loss_prevented_usd","sum"), loss=("loss_usd","sum"))
cap = (yc["prev"] / (yc["prev"] + yc["loss"]) * 100).fillna(0)
common = sorted(set(ys.index) | set(cap.index))
save("chart20_success_timeline_dual", {
    "title": {"text": "Containment vs Capital Preservation Rate"},
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
    "legend": {"data": ["Containment Success","Capital Preservation"], "bottom": 0},
    "xAxis": {"type": "category", "data": [int(y) for y in common]},
    "yAxis": {"type": "value", "name": "Rate (%)", "max": 105,
              "axisLabel": {"formatter": "{value}%"}},
    "series": [
        {"name": "Containment Success", "type": "line",
         "data": [round(float(ys.get(y, 0)),1) for y in common],
         "areaStyle": {"opacity": 0.15}, "symbol": "circle", "symbolSize": 8,
         "itemStyle": {"color": C["green"]}},
        {"name": "Capital Preservation", "type": "line",
         "data": [round(float(cap.get(y, 0)),1) for y in common],
         "areaStyle": {"opacity": 0.15}, "symbol": "diamond", "symbolSize": 8,
         "itemStyle": {"color": C["blue"]}}
    ]
})

# ── Chart 21: Authority Performance (bars + time labels) ──────────
astats = {}
for auth in metrics["authority"].unique():
    ad = metrics[metrics["authority"] == auth]
    if auth == "Governance":
        ad = ad[ad["protocol"] != "Ethereum DAO Fork"]
    if len(ad) > 0:
        astats[auth] = {
            "success": round(float(ad["containment_success_pct"].mean()), 1),
            "time": round(float(ad["time_to_contain_min"].mean()), 0)
        }
auths = list(astats.keys())
bar_data = []
for a in auths:
    t = astats[a]["time"]
    if t > 1440: lbl = f"{t/1440:.0f}d"
    elif t > 60: lbl = f"{t/60:.0f}h"
    else: lbl = f"{t:.0f}m"
    bar_data.append({
        "value": astats[a]["success"],
        "itemStyle": {"color": AUTH_COLORS.get(a, C["gray"])},
        "label": {"show": True, "position": "top",
                  "formatter": f"{astats[a]['success']}% ({lbl})"}
    })
save("chart21_authority_performance", {
    "title": {"text": "Authority: Success Rate vs Response Time"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": auths},
    "yAxis": {"type": "value", "name": "Success (%)", "max": 110},
    "series": [{"type": "bar", "data": bar_data}]
})

# ── Chart 22: Loss Magnitude Histograms ────────────────────────────
all_log = np.log10(exploits[exploits["loss_usd"] > 0]["loss_usd"]).dropna()
int_log = np.log10(interventions[interventions["loss_usd"] > 0]["loss_usd"]).dropna()
def make_hist(vals, nbins=15):
    counts, edges = np.histogram(vals, bins=nbins)
    return [round(float(e),2) for e in edges], counts.tolist()
ae, ac = make_hist(all_log, 20)
ie, ic = make_hist(int_log, 15)

save("chart22_loss_magnitude", {
    "title": {"text": "Loss Magnitude Distribution (Log Scale)"},
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["All Exploits","Interventions"], "bottom": 0},
    "xAxis": {"type": "category",
              "data": [f"10^{e:.0f}" for e in ae[:-1]],
              "name": "USD Magnitude"},
    "yAxis": {"type": "value", "name": "Frequency"},
    "series": [
        {"name": "All Exploits", "type": "bar", "data": ac,
         "itemStyle": {"color": C["slate"], "opacity": 0.7}},
        {"name": "Interventions", "type": "bar", "data": ic + [0]*(len(ac)-len(ic)),
         "itemStyle": {"color": C["blue"], "opacity": 0.7}}
    ]
})

# ── Chart 23: Authority Effectiveness Bubbles (all interventions) ──
am = interventions.groupby("authority").agg(
    success=("containment_success_pct","mean"),
    detect=("time_to_detect_min","median"),
    saved=("loss_prevented_usd","sum"),
    n=("incident_id","count")).fillna(0)
save("chart23_authority_effectiveness_all", {
    "title": {"text": "Authority Effectiveness (All Interventions)"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "category", "data": am.index.tolist()},
    "yAxis": {"type": "value", "name": "Avg Success (%)", "max": 110},
    "series": [{
        "type": "scatter", "symbolSize": 30,
        "data": [{"value": [i, round(float(r["success"]),1)],
                  "itemStyle": {"color": AUTH_COLORS.get(idx, C["gray"])},
                  "label": {"show": True, "position": "top",
                            "formatter": f"${r['saved']/1e6:.0f}M (n={int(r['n'])})"}}
                 for i, (idx, r) in enumerate(am.iterrows())]
    }]
})

# ── Chart 24: Authority Effectiveness (metrics subset) ────────────
mm = metrics.groupby("authority").agg(
    success=("containment_success_pct","mean"),
    detect=("time_to_detect_min","median"),
    saved=("loss_prevented_usd","sum"),
    n=("incident_id","count")).fillna(0)
save("chart24_authority_effectiveness_metrics", {
    "title": {"text": "Authority Effectiveness (High-Confidence)"},
    "tooltip": {"trigger": "item"},
    "xAxis": {"type": "category", "data": mm.index.tolist()},
    "yAxis": {"type": "value", "name": "Avg Success (%)", "max": 110},
    "series": [{
        "type": "scatter", "symbolSize": 30,
        "data": [{"value": [i, round(float(r["success"]),1)],
                  "itemStyle": {"color": AUTH_COLORS.get(idx, C["gray"])},
                  "label": {"show": True, "position": "top",
                            "formatter": f"${r['saved']/1e6:.0f}M (n={int(r['n'])})"}}
                 for i, (idx, r) in enumerate(mm.iterrows())]
    }]
})

# ── Chart 25: Intervention Heatmap (year × authority) ─────────────
ht = combined.groupby(["year","authority"]).size().unstack(fill_value=0)
yrs25 = sorted(ht.index.tolist())
auths25 = [a for a in AUTHORITY_ORDER if a in ht.columns] + \
          [a for a in ht.columns if a not in AUTHORITY_ORDER]
ht = ht.reindex(columns=auths25, fill_value=0)
save("chart25_intervention_heatmap_combined", {
    "title": {"text": "Intervention Volume: Year × Authority"},
    "tooltip": {"position": "top"},
    "xAxis": {"type": "category", "data": [int(y) for y in yrs25],
              "splitArea": {"show": True}},
    "yAxis": {"type": "category", "data": auths25,
              "splitArea": {"show": True}},
    "visualMap": {"min": 0, "max": int(ht.values.max()),
                  "calculable": True, "orient": "horizontal",
                  "left": "center", "bottom": 0,
                  "inRange": {"color": ["#eff6ff","#bfdbfe","#60a5fa","#2563eb","#1e40af"]}},
    "series": [{
        "type": "heatmap",
        "data": [[yrs25.index(y), auths25.index(a), int(ht.loc[y,a])]
                 for y in yrs25 for a in auths25],
        "label": {"show": True}, "emphasis": {"itemStyle": {"shadowBlur": 10}}
    }]
})

print("\n✅ Batch 2 complete (charts 19-25)")
