# Legitimate Intervention Framework (LIF) — TODO Tracker

**Purpose**: This file is the step-by-step execution checklist for bringing the LIF repo + website into a consistent, accurate, and web-interactive state.

**Source of Truth (Dataset v1.0)**
- `data/refined/lif_exploits_final.csv`: **705 rows**
- LIF-relevant exploits: **601**
- Total losses: **$78.805B** (sum of `loss_usd`)
- `data/refined/lif_all_interventions.csv`: **130 rows**
- `data/refined/lif_intervention_metrics.csv`: **52 rows**

**Hard requirements**
- Standardize stats output to **`data/refined/lif_stats.json`** (single file).
- Static hosting compatible (Cloudflare/Vercel **and** IPFS).
  - Research subpages must be directory-based: `web/research/<theme>/index.html`.
- Website IA inspired by `ai-2027.com`:
  - `/summary` becomes the paper summary (concise-version inspired)
  - `/research` becomes an index of themes
  - `/research/<theme>` pages provide focused narrative + relevant charts
  - `/research/all` provides the full 50-chart narrative view (single column) with a toggle to grid/multi-column
  - `/about` includes a collapsible changelog section
- Deep-linking support:
  - `database.html?search=...` (filter)
  - `database.html?id=<incident_id>` (open modal)
  - research deep links use query params for consistency:
    - `research/<theme>/?chart=<chart_id>`
    - `research/all/?chart=<chart_id>`
- Navbar research link includes a dropdown for themes (quick access).
- Include a dismissible site-wide banner indicating the site is under active development and welcoming corrections.
- Site-wide footer includes a research/disclaimer statement and links such as Terms, Privacy, Request Correction, and a tip/correction contact.

---

## 0) Website + repo audit (confirm current state)
- [ ] Inventory existing web routes/pages and decide final IA mappings (home vs summary vs index)
- [x] Confirm chart library choice for interactivity (Chart.js vs ECharts)
- [x] Confirm deep-link URL conventions for research charts using query params (e.g. `?chart=chart08`)
- [x] Confirm IPFS constraints are met (no server routing assumptions)

## 1) Fix stale stats references + standardize stats file
- [x] Decide final schema for `data/refined/lif_stats.json` (fields used by web + docs)
- [x] Update/merge scripts so exactly one generator writes `lif_stats.json`
- [x] Remove/stop generating `lif_stats_v1.0.json` (or mark deprecated)
- [x] Ensure notebook and any web copy refer to `lif_stats.json`

## 2) Regenerate web data exports (and make them interactivity-ready)
- [x] Update `scripts/core/generate_web_data.py` schema for:
  - [x] `web/data/exploits.json`
  - [x] `web/data/interventions.json`
- [x] Add aggregated series exports for interactive charts (location TBD, e.g. `web/data/series/*.json`)
  - [x] yearly totals
  - [x] 4-layer yearly losses (paper-aligned)
  - [x] vector distribution
  - [x] cumulative totals
- [x] Regenerate JSON outputs and replace old ones safely
- [x] Ensure `web/js/main.js` remains compatible (or update it with backward compatibility)

## 3) Website information architecture + layout refactor (ai-2027-inspired)
### 3.1 Global nav + routes
- [x] Add a dedicated `/summary` page
- [x] Make current `index.html` serve as landing/home (or redirect to summary — decide)
- [x] Implement `/research` as theme index
- [x] Implement `/research/<theme>` pages
- [x] Implement `/research/all` for the full 50-chart narrative

### 3.2 Make charts bigger (2-column layouts)
- [x] Redesign landing/home into 2-column layout where the chart area is wider
- [x] Redesign summary similarly (large interactive chart area)
- [x] Keep mobile responsive behavior

### 3.4 Chart UX regressions + layout polish (landing + mobile)
- [x] Landing sticky chart: caption must be under chart (no side-by-side)
- [x] Landing sticky chart: remove in-chart title (use caption below chart only)
- [x] Landing sticky chart: move sticky chart down to align with author line
- [x] Landing mobile: fix layout regression where text is pushed/narrow
- [x] Square sticky charts: add smart y-axis label fitting so labels never clip
- [x] Mobile Dock: Center charts, move title to top-left, close button to top-right.

### 3.5 Chart theming (site consistency)
- [x] Define single site chart palette (Newsreader look; limited colors)
- [x] Enforce palette across JSON-spec charts and registry charts

### 3.3 Copy rewrite (tone aligned with paper)
- [ ] Rewrite landing copy to be neutral and evidence-first
- [ ] Ensure all numerical claims match dataset + `lif_stats.json`

## 4) Research pages: thematic + per-chart narrative
- [ ] Extract/update short insights per chart (seed from `manuscript/analysis_insights.md`)
- [x] Build theme index on `/research`
- [x] Theme pages: narrative + subset of charts + references/notes
- [x] `/research/all`: 50-chart single-column narrative with:
  - [ ] per-chart anchor
  - [ ] short insight block
  - [ ] toggle to grid/multi-column
  - [ ] query-param deep link support (`?chart=<chart_id>`) that scrolls to the chart

## 4.1) Content plan (paper-first)
- [ ] Landing page: host the full paper (`paper/main.tex`) as the primary narrative, with as many charts in the chart by the side as possible
  - [ ] Include the 7 paper charts that do not overlap with the LIF-50 chart set
- [ ] Summary page: derive content from the concise paper wrapper (`paper/main_concise.tex`)
- [ ] Research pages: use `manuscript/analysis_insights.md` for short per-chart insights across `/research/all` and theme pages

## 5) Deep-linking improvements
- [x] Database: implement `?id=<incident_id>` deep link to open modal
- [x] Research: implement deep-link scroll to theme section / chart
- [ ] Ensure deep links are stable across refactors

## 6) Notebook review + chart correctness (paper alignment)
- [x] Audit `scripts/analysis/lif_charts_v1.ipynb` for outdated logic
- [x] Update notebook markdown narrative as needed during the audit
- [x] Implement **4-layer annual loss** figure aligned with `paper/figures/lof02_four_layer_timeline.png`
- [x] Ensure chart outputs used on web are regenerated from the corrected notebook
- [x] Export aggregated series JSON for interactive charts

### 6.1 Accuracy-first interactive chart audit (Option 2)
- [x] Batch 1: verify charts 01, 02, 08, 09 match notebook/data and lock specs
- [ ] Continue chart-by-chart audit through chart50 (no placeholders)
- [ ] Verify each chart is interactive (no silent PNG fallback)

## 7) Documentation + reports consistency sweep
- [x] Update repo `README.md` stats and “Last Updated”
- [x] Update `methodology/*.md` stats
- [x] Update manuscript reports that embed old numbers
- [x] Update `web/DEVELOPMENT_PLAN.md` to reflect the new IA + pipeline + accurate metrics

## 8) Old DB/build artifacts cleanup
- [ ] Identify any database/cache/build artifacts created from old data
- [ ] Decide what to delete vs regenerate
- [ ] Document reproducible rebuild steps

## 9) About page changelog
- [ ] Add collapsible changelog section after data sources
- [ ] Add entries for major updates (dataset update, chart pipeline, IA refactor)

## 10) Site-wide banner + footer
- [ ] Add dismissible "active development" banner to all pages
- [ ] Create reusable footer with:
  - [ ] data/disclaimer text (research + educational; may contain errors/omissions; independently verify)
  - [ ] links (Terms, Privacy, Request Correction)
  - [ ] correction/tip contact method

## 11) Final Polish & Typography
- [x] Standardize navigation links to use Phosphor icons (IPFS compatibility)
- [x] Optimize navigation bar for mobile (fix back arrow visibility & dropdown cutoff)
- [x] Unify desktop/mobile navigation layout (arrow-left, links-right)
- [x] Increase typography scale for navigation and metadata for better readability

---

## Done Log
- [x] Confirm dataset source-of-truth stats (705/601/$78.805B; 130; 52)
- [x] Formalize prevented definitions in `lif_stats.json` (`definitions.prevented_usd`) + methodology note; rerun notebook to regenerate outputs
- [x] Prevented definitions formalization, notebook markdown sweep, and regenerated lif_stats.json
- [x] Implement directory-based routes (`/summary/`, `/research/`, `/research/all/`) and make `index.html` the narrative landing page
- [x] Implement ai-2027-style sticky chart column + mobile bottom dock (close + reopen)
- [x] Remove Lucide icon dependency; use inline SVG (Phosphor-style) for IPFS safety
- [x] Clone Phosphor icons homepage repo for reference (`/Users/elemoghenekaro/Desktop/tasks/parametrig/veil/research/homepage`)
- [x] Run Option A chart-spec generator to produce initial `web/data/charts/*.json`
- [x] Fix chart resize on page switch (ResizeObserver + force resize)
- [x] Fix Y-axis label truncation (use breakAll with width: 140px)
- [x] Reduce chart vertical height from 100vh to 66vh for compact layout
- [x] Generate all 50 chart JSON specs in `web/data/charts/`
