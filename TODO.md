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

## ✅ Completed Work (Phase 1 & 2)

### Core Infrastructure ✅
- [x] Website IA established (/, /summary/, /research/, /research/<theme>/, /research/all/, /database.html, /about.html)
- [x] ECharts integration with 50 interactive charts
- [x] Dataset v1.0 finalized with standardized stats in `lif_stats.json`
- [x] Static hosting compatibility (IPFS-ready)
- [x] Deep-linking implementation for database and research charts

### Design & UX ✅
- [x] Universal aesthetic standardization (680px column width, consistent navigation)
- [x] Mobile responsive design with dock optimization
- [x] Chart styling consistency across all 50 charts
- [x] Font size optimization for mobile and desktop
- [x] About page with collapsible changelog section

### Content & Data ✅
- [x] All numerical claims updated to match current dataset (705 incidents, $78.8B losses, 130 interventions)
- [x] Chart generation scripts updated and all charts regenerated
- [x] Documentation synchronized (TODO.md, HANDOVER_CONTEXT.md)

---

## 🔄 Remaining Tasks (Phase 3)

### Site-wide Features
- [ ] Add dismissible "active development" banner to all pages
- [ ] Create comprehensive footer with disclaimer, Terms, Privacy, Request Correction links
- [ ] Add correction/tip contact method

### Design System Foundation (CSS Restructure)
- [ ] Create `web/css/tokens.css` with Authority (Blue/Green/Purple) & Accent (Cyan) colors
- [ ] Restructure `web/css/` directory (tokens/, base/, components/, pages/)
- [ ] Refactor `base.css` and `layout.css` to consume `tokens.css`
- [ ] Update `echarts_runtime.js` to use `getComputedStyle` for theme injection
- [ ] Clean up legacy CSS (remove `style.css.bak`, consolidate `pages/` styles)

### Page Architecture Restructure
- [ ] **Landing Page (`index.html`)**: Strip old charts, implement "Concise Paper" flow
- [ ] **The Atlas (`research/index.html`)**: Host all 50 charts (migrate from `research/all`)
- [ ] Implement **Detailed Scroll Navigator** (Side TOC) for Atlas
- [ ] Implement Lazy Loading for charts
- [ ] **Summary Page (`summary/index.html`)**: Update to purely Narrative Summary
- [ ] **Cleanup**: Delete `web/research/all/` directory

### Content Enhancement
- [ ] Extract short insights per chart from `manuscript/analysis_insights.md`
- [ ] Add per-chart insight blocks to `/research/all`
- [ ] Implement toggle to grid/multi-column view for research pages
- [ ] Update theme pages with enhanced narrative content
- [ ] Map `LIF_FINAL_REPORT.md` narrative to Summary page
- [ ] Ensure "Research" navbar link points to `/research/` (The Atlas)
- [ ] Verify standard color usage across all 50 charts
- [ ] Verify Mobile Responsiveness of the new Atlas view

### Research Pages Polish
- [ ] `/research`: Theme index alignment and navigation improvements
- [ ] `/research/*`: Individual theme pages refinement (Threat, Intervention, Efficiency, Framework)
- [ ] `/summary`: Concise summary cleanup
- [ ] `/database.html`: Final touches and UX improvements

### Advanced Features
- [ ] Landing page: Integrate full paper narrative with side charts
- [ ] Include 7 paper charts that don't overlap with LIF-50 set
- [ ] Summary page: Derive content from concise paper wrapper

### Paper Integration
- [ ] Landing page: host the full paper (`paper/main.tex`) as the primary narrative
- [ ] Summary page: derive content from the concise paper wrapper (`paper/main_concise.tex`)
- [ ] Research pages: use `manuscript/analysis_insights.md` for short per-chart insights

---

## 📋 Technical Debt & Cleanup
- [ ] Identify and clean any old database/cache/build artifacts
- [ ] Decide what to delete vs regenerate
- [ ] Document reproducible rebuild steps
- [ ] Final performance optimization audit

---

## 🏗️ Proposed CSS Structure
```text
web/css/
├── tokens.css       # [NEW] Single source of truth for variables
├── base/
│   ├── main.css     # Renamed from base.css
│   └── layout.css   # Grid system & containers
├── components/
│   ├── header.css   # Nav & Metadata bars
│   ├── charts.css   # ECharts containers & controls
│   └── tables.css   # Data tables (Database page)
└── pages/
    ├── landing.css
    ├── atlas.css    # (The compiled research css)
    └── narrative.css # Shared for About/Summary
```
