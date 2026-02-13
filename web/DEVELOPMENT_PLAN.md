# Legitimate Overrides Website Development Plan

## Executive Summary
Transform the LIF website from a "project site" to a data platform for "Legitimate Overrides" — launching after arXiv preprint publication which has been done. This plan details the rebranding, data migration from the cleaned dataset, and expanded research presentation.

---

## Current State Assessment

### Existing Assets
- **Location:** `/Users/elemoghenekaro/Desktop/tasks/legitimate-intervention-framework/web/`
- **Charts:** 50 visualization charts in `/charts/` directory but they are old. And we need to confirm the new charts are accurate and espcially aligned with the paper notebook which is accurate /Users/elemoghenekaro/Desktop/tasks/legitimate-overrides-paper/notebooks/paper_analysis_complete.ipynb e.g. the four layer annual defi losses is not implemented as 3 layer in the lif notebook /Users/elemoghenekaro/Desktop/tasks/legitimate-intervention-framework/scripts/analysis/lif_charts_v1.ipynb cumulative losses so has to be corrected among others. While the paper focused on intervention more, here we focus on the whole dataset    
- **Pages:** `index.html`, `research.html`, `database.html`, `about.html`
- **Data:** `exploits.json`, `interventions.json` (requires regeneration from cleaned dataset)
- **CSS:** `base.css`, `layout.css`, `pages/home.css`, `pages/research.css`

### Cleaned Dataset (New Source of Truth)
- **File:** `/data/refined/lif_exploits_final.csv`
- **Statistics:** 693 incidents, $81.05B total losses, 402 LIF-relevant, 30 intervention cases (these are old numbers and need updating)
- **Columns:** incident metadata, loss data, intervention details, timing, success metrics -- i think these can be improved upon to create a better database 

---

## Phase 1: Rebranding & Content Updates

### 1.1 Homepage (`index.html`) Updates

#### Title & Metadata Changes
| Element | Current | New |
|---------|---------|-----|
| Page Title | "LIF Research \| Legitimate Intervention Framework" | "Legitimate Overrides \| Academic Research" |
| Meta Description | "A comprehensive research framework..." | "Academic research analyzing legitimate intervention mechanisms in decentralized protocols" |
| Keywords | "LIF, legitimate intervention framework..." | "legitimate overrides, crypto security research, academic paper, blockchain intervention" |
| OG Title | "LIF Research \| Legitimate Intervention Framework" | "Legitimate Overrides \| Academic Research Paper" |

#### Content Updates
- **Hero Title:** Change "Legitimate Intervention Framework" → "Legitimate Overrides"
- **Subtitle:** Add academic context: "An empirical analysis of intervention efficacy in decentralized protocols"
- **Statistics Update:** Refresh with new dataset numbers
- **Author Attribution:** Keep current (Elem Oghenekaro, Dr. Nimrod Talmon)
- **Publication Date:** Update to arXiv submission date (already done)
- **PDF/Listen/Watch Links:** Add arXiv preprint link to the pdf icon download

#### Chart Integration (Hero Scroller) -- see if this can be improved on
Current 7 hero charts remain but refresh data:
1. `chart02_cumulative_losses.png` - Cumulative Losses
2. `chart01_annual_losses.png` - Annual Losses  
3. `chart09_vector_distribution.png` - Attack Vectors
4. `chart03_top20_magnitude.png` - Top 20 Magnitude
5. `chart37_response_time.png` - Response Time Analysis
6. `chart40_success_timeline.png` - Success Timeline
7. `chart43_success_matrix.png` - Success Matrix

### 1.2 Research Page (`research.html`) Expansion -- we should have just all 50 charts and short analysis 
#### Title & Metadata
| Element | Current | New |
|---------|---------|-----|
| Page Title | "Research Report \| LIF" | "Research Paper \| Legitimate Overrides" |

#### Executive Summary Stats Update
```
Current → New
- 705 cases → 693 incidents
- $78.54B total losses → $81.05B total losses  
- $2.12B preventable → $2.77B prevented (verify from dataset)
- 120 interventions → 30 intervention cases
```

#### Expanded Chart Showcase (Beyond Current 8)

**Current 8 charts:**
- chart01_annual_losses.png
- chart04_relevance_pie.png
- chart09_vector_distribution.png
- chart15_timeline_heatmap_x_month.png
- chart18_intervention_timeline.png
- chart23_authority_effectiveness_all.png
- chart28_matrix_heatmap_combined.png
- chart32_prevented_vs_incurred_combined.png
- chart37_response_time.png
- chart38_success_vs_time.png
- chart47_comprehensive_lif_analysis.png

**Additional High-Value Charts to Integrate:**

**Section I: Threat Landscape (Add 3 charts)**
- `chart02_cumulative_losses.png` - Cumulative trajectory
- `chart05_loss_distribution.png` - Loss distribution histogram
- `chart06_loss_concentration_lorenz.png` - Pareto concentration
- `chart10_vector_losses.png` - Vector loss correlation
- `chart14_pattern_temporal.png` - Temporal attack patterns

**Section II: Intervention State (Add 3 charts)**
- `chart19_hacks_vs_interventions.png` - Comparative timeline
- `chart21_authority_performance.png` - Authority performance metrics
- `chart25_intervention_heatmap_combined.png` - Intervention density
- `chart26_scope_distribution_combined.png` - Scope distribution

**Section III: Effectiveness Gap (Add 3 charts)**
- `chart33_speed_scatter_metrics.png` - Speed correlation scatter
- `chart36_success_distribution.png` - Success rate distribution
- `chart39_risk_matrix_scatter.png` - Risk-adjusted analysis
- `chart41_success_timeline_case.png` - Case-level success timeline

**Section IV: Strategic Framework (Add 2 charts)**
- `chart42_detect_vs_contain_detailed.png` - Detection vs containment
- `chart44_success_matrix_enhanced.png` - Enhanced success matrix
- `chart45_effectiveness_leaderboard.png` - Effectiveness rankings
- `chart48_strategic_roi_rankings.png` - ROI strategic analysis
- `chart50_loss_prevented_vs_incurred.png` - Final prevented/incurred

**New Structure:** ~20-25 charts across 5 sections (vs current ~8)

### 1.3 Navigation & Global Updates

#### Header Navigation
Keep current structure but update active states:
- Summary (index.html)
- Research (research.html) ← expanded content
- Database (database.html) ← regenerate from new dataset
- About (about.html) ← update for academic focus

#### Footer/About Page Updates
- Reposition from "project" to "academic research"
- Add citation format (BibTeX)
- Link to arXiv preprint
- Add methodology documentation links

---

## Phase 2: Data Regeneration

### 2.1 Dataset Migration

**Source Files:**
- `/data/refined/lif_exploits_final.csv` (693 incidents)
- `/data/refined/lif_intervention_metrics.csv` (30 intervention cases)
- `/data/refined/lif_all_interventions.csv` (all intervention data)

**Target Files:**
- `/web/data/exploits.json`
- `/web/data/interventions.json`

### 2.2 JSON Schema Update

**exploits.json structure:**
```json
{
  "metadata": {
    "total_incidents": 693,
    "total_losses_usd": 81050000000,
    "lif_relevant_count": 402,
    "intervention_count": 30,
    "date_range": "2014-2026",
    "last_updated": "2026-02-09"
  },
  "incidents": [
    {
      "incident_id": "...",
      "date": "...",
      "protocol": "...",
      "chain": "...",
      "loss_usd": 0,
      "loss_prevented_usd": 0,
      "is_technical": true,
      "is_lif_relevant": true,
      "is_intervention": true,
      "vector_category": "...",
      "ecosystem": "...",
      "scope": "...",
      "authority": "...",
      "containment_success_pct": 0
    }
  ]
}
```

**interventions.json structure:**
```json
{
  "metadata": {
    "total_interventions": 30,
    "total_prevented_usd": 2770000000,
    "avg_success_rate": 0.825
  },
  "interventions": [...]
}
```

### 2.3 Database Page (`database.html`) Refresh

- Regenerate table from new JSON data
- Update search/filter functionality
- Add column: `confidence_level` (high/medium/low)
- Add column: `source_file` traceability
- Ensure all 693 records load efficiently

---

## Phase 3: Design & Academic Styling

### 3.1 Visual Identity Shifts

| Aspect | Current (Project) | New (Academic) |
|--------|-------------------|----------------|
| Tone | Solution/framework | Research/analysis |
| Color Palette | Keep existing (professional) | Subtle refinement |
| Typography | Newsreader (keep) | Newsreader (keep) |
| Layout | Story-scroller | Paper-style sections |
| Imagery | Charts dominant | Charts + methodology diagrams |

### 3.2 CSS Updates Required

**base.css:**
- Add `.academic-header` class for paper-style headers
- Add `.citation-box` class for BibTeX display
- Add `.arxiv-badge` class for preprint indicator

**layout.css:**
- Refine scroll-indicator for longer research page
- Add `.chart-grid-expanded` for 20+ chart layouts

**pages/research.css:**
- Add `.paper-abstract` styling
- Add `.methodology-section` styling
- Add `.figure-caption` academic formatting

### 3.3 Academic Elements to Add

**Abstract Section (research.html):**
```html
<div class="paper-abstract">
  <h2>Abstract</h2>
  <p>This paper presents the first comprehensive empirical analysis 
  of legitimate intervention mechanisms in decentralized protocols...</p>
</div>
```

**Citation Block:**
```html
<div class="citation-box">
  <h3>Cite This Paper</h3>
  <pre>@article{oghenekaro2026legitimate,
  title={Legitimate Overrides: An Empirical Analysis of Intervention Efficacy},
  author={Oghenekaro, Elem and Talmon, Nimrod},
  year={2026}
}</pre>
</div>
```

**arXiv Integration (placeholder):**
```html
<div class="arxiv-badge">
  <span>Preprint available on</span>
  <a href="[ARXIV_LINK_TBD]">arXiv</a>
</div>
```

---

## Phase 4: Chart Refresh (If Needed)

### 4.1 Chart Audit

Current 50 charts in `/web/charts/`:
- Verify all 50 render correctly with new data
- Check for outdated statistics in chart titles/annotations
- Confirm chart file sizes are web-optimized

### 4.2 New Chart Generation (Optional)

If new insights emerge from cleaned dataset:
- `chart51_methodology_flow.png` - Research methodology diagram
- `chart52_dataset_coverage.png` - Dataset coverage visualization
- `chart53_intervention_evolution.png` - Intervention mechanism evolution

---

## Phase 5: Launch Preparation

### 5.1 Pre-Launch Checklist

- [ ] All titles updated to "Legitimate Overrides"
- [ ] Metadata refreshed site-wide
- [ ] JSON data regenerated from cleaned CSV
- [ ] Database page loads all 693 records
- [ ] Research page displays 20+ charts
- [ ] Citation block added
- [ ] arXiv placeholder ready
- [ ] Mobile responsiveness verified
- [ ] Chart lazy-loading functional
- [ ] Scroll indicators working

### 5.2 arXiv Launch Sequence

**T-0 (arXiv Publication Day):**
1. Replace arXiv placeholder with actual link
2. Update publication date to match arXiv
3. Deploy updated site
4. Verify all links functional

**T+1 (Announcement Day):**
1. Social media announcement with arXiv link
2. Website analytics monitoring
3. Community engagement

---

## File Action Checklist

### High Priority (Must Update)
| File | Action | Complexity |
|------|--------|------------|
| `index.html` | Rebrand title, stats, arXiv placeholder | Medium |
| `research.html` | Expand charts, add abstract, citations | High |
| `web/data/exploits.json` | Regenerate from CSV | Medium |
| `web/data/interventions.json` | Regenerate from CSV | Medium |
| `database.html` | Refresh from new JSON | Medium |
| `about.html` | Academic repositioning | Low |

### Medium Priority (Should Update)
| File | Action | Complexity |
|------|--------|------------|
| `css/pages/research.css` | Academic styling additions | Medium |
| `css/base.css` | Citation/arxiv classes | Low |
| `js/main.js` | Verify chart switching | Low |

### Low Priority (Nice to Have)
| File | Action | Complexity |
|------|--------|------------|
| `favicon.svg` | Consider refresh | Low |
| `css/layout.css` | Grid refinements | Low |

---

## Statistics Summary (From Cleaned Dataset)

### Key Metrics for Website
```
Total Incidents:              693
Total Losses:                 $81.05B
LIF-Relevant Incidents:       402
Intervention Cases:           30
Prevented via Intervention:   $2.77B (verify)
Date Range:                   2014-2026
```

### Intervention Breakdown (30 cases)
- By Authority: Signer Set / Delegated Body / Governance
- By Scope: Protocol / Account / Network
- By Success: Full (100%) / Partial (1-99%) / Reactive (0%)

---

## Success Criteria

- ✅ All page titles read "Legitimate Overrides"
- ✅ Research page showcases 20+ charts (not just 8)
- ✅ Data regenerated from cleaned 693-incident dataset
- ✅ Academic styling implemented (abstract, citations)
- ✅ arXiv integration ready for preprint link
- ✅ Professional scholarly presentation achieved
- ✅ Ready for post-arXiv launch

---

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Rebranding | 2-3 hours | None |
| Phase 2: Data Regeneration | 1-2 hours | CSV ready |
| Phase 3: Design Updates | 2-3 hours | Phase 1 complete |
| Phase 4: Chart Audit | 1 hour | Phase 2 complete |
| Phase 5: Testing & Launch | 1-2 hours | All above |
| **Total** | **7-11 hours** | - |

---

## Next Steps

1. **Confirm arXiv timeline** - When will preprint be submitted?
2. **Verify dataset statistics** - Confirm $2.77B prevented figure
3. **Prioritize Phase 1** - Begin with `index.html` and `research.html` updates
4. **Generate JSON data** - Create `/scripts/generate_web_data.py` refresh
5. **Test chart loading** - Verify all 50 charts display correctly

---

*Plan created: 2026-02-09*
*Dataset: lif_exploits_final.csv (693 incidents)*
*Target launch: Post-arXiv publication*
