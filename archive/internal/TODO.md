# Legitimate Intervention Framework (LIF) — TODO Tracker

**Purpose**: Step-by-step execution checklist for completing the LIF website.
**Last updated**: Feb 16, 2026

---

## 🎯 Now (Launch Blockers + High-Leverage)

- [ ] **Deployment**: Push to production (Cloudflare Pages / Vercel / IPFS)
- [ ] **DNS / Domain**: Verify `legitimate-intervention.org` resolves correctly

- [ ] **Parameterize base domain at deploy time**
  - [ ] Avoid hardcoding `https://legitimate-intervention.org` in OG/Twitter image URLs where possible

- [x] **Per-page social cards (stable `og:image` + `twitter:image`)**
  - [x] Add OG/Twitter tags to pages that currently lack them (summary + research pages)
  - [x] Assign a **representative chart per page theme** (and keep it stable):
    - [x] Landing (`/`) → chart19
    - [x] Summary (`/summary/`) → chart02
    - [x] Research hub (`/research/`) → chart28
    - [x] Research All (`/research/all/`) → chart08
    - [x] Threat (`/research/threat/`) → chart10
    - [x] Intervention (`/research/intervention/`) → chart21
    - [x] Efficiency (`/research/efficiency/`) → chart38
    - [x] Framework (`/research/framework/`) → chart28
    - [x] Database (`/database.html`) → chart19
    - [x] About (`/about.html`) → chart19
  - [x] Ensure OG/Twitter descriptions avoid brittle numbers
  - [x] Use white-background `_social` versions of chart PNGs for better Twitter rendering

- [ ] **Chart dock titles + captions**
  - [x] Ensure chart dock header shows human titles (not raw chart ids)
  - [x] Add missing title mappings for charts used on landing (chart19, chart40, chart41, vector evolution chart)

- [x] **Sticky chart transitions**
  - [x] Verify scroll-to-scroll chart changes do not flash fallback PNGs (desktop + mobile)
  - [x] If any chart still flashes, tune the fallback delay and/or add a “latest request wins” guard

## ✅ Completed Phases

### Summary ✅ (compressed)
- [x] IA + 50 interactive charts + dataset v1.0 wired to web exports
- [x] Landing/Summary/About/Research pages populated and styled
- [x] Deep links + scroll navigator + mobile dock + audio dock
- [x] Baseline QA + SEO tags
- [x] Feb 16: sticky chart sizing/typography tweaks + reduced fallback flash during swaps

---

## 🔄 Remaining Work

### Phase 12: Design System & CSS Cleanup (Deferred)
> Goal: Consolidate CSS into a proper design system.

- [ ] Create `web/css/tokens.css` with design tokens:
  - Authority colors (Blue / Green / Purple)
  - Accent color (Cyan)
  - Typography scale
  - Spacing scale
- [ ] Restructure CSS directory:
  ```
  web/css/
  ├── tokens.css
  ├── base.css
  ├── layout.css
  ├── components/
  │   ├── header.css
  │   ├── charts.css
  │   └── tables.css
  └── pages/
      ├── landing.css
      ├── narrative.css
      ├── about.css
      ├── database.css
      ├── research.css
      └── summary.css
  ```
- [ ] Refactor `base.css` and `layout.css` to consume `tokens.css`
- [ ] Update `echarts_runtime.js` to use `getComputedStyle()` for theme colors
- [ ] Delete `style.css.bak` and any unused CSS


---

## 🧹 Later (Post-launch / Review-first)

- [ ] **OSS cleanup / archive pass** (Phase 14+)
- [ ] **Mobile/iPad layout regression checks** (Phase 15)
- [ ] **Research/all overview UX** (grid toggle + overview dashboard)

legitimate-intervention-framework/
├── data/                  # refined datasets (csv/json)
├── scripts/               # generators (charts, web exports)
├── web/                   # the static site
├── manuscript/            # research writing sources
├── methodology/           # data dictionary/provenance
├── visualizations/        # research figures (only if needed)
├── docs/                  # OSS docs (contributing, governance, media)
├── archive/               # historical assets you want to keep but not ship
├── README.md
├── LICENSE
└── requirements.txt

- [x] **Create archive structure**
  - [x] Add `archive/` top-level directory
  - [x] Add `archive/internal/` (private project-management docs + internal references)
  - [x] Add `archive/media/` (screenshots, large binaries, legacy visuals)
  - [x] Add `archive/manuscript/` (older drafts / non-shipping writeups)

- [x] **Move internal docs out of main tree (not public)**
  - [x] Move `TODO.md` → `archive/internal/TODO.md`
  - [x] Move `HANDOVER_CONTEXT.md` → `archive/internal/HANDOVER_CONTEXT.md`
  - [ ] Replace with minimal public-facing equivalents (TBD) only if needed for contributors (user preference: likely none)

- [x] **Archive large / temporary assets**
  - [x] Move website screenshots (e.g. `web/Screenshot*.png`, `web/screencapture-*.png`) → `archive/media/`
  - [x] Ensure only one canonical audio file is shipped for the site (keep under `web/audio/`)
  - [ ] Move any duplicate/unused large audio files into `archive/media/`

- [ ] **Gnosis framework documents + their embedded images**
  - [x] Move `manuscript/gnosis_framework_response*.md` into a dedicated directory (e.g. `archive/gnosis/`)
  - [ ] Move referenced images from `visualizations/archived/v0_legacy/` into a stable archive location (e.g. `archive/gnosis/visuals/`)
  - [ ] Update image links inside the moved docs so they still render

- [ ] **Treat `visualizations/` as build artifact (non-canonical)**
  - [ ] Document that `visualizations/` can be regenerated and is not authoritative
  - [ ] Confirm website runtime does not depend on `visualizations/` paths

- [ ] **Git hygiene**
  - [ ] Update `.gitignore` to include `venv/` (in addition to `.venv/`)
  - [ ] Remove any tracked `.DS_Store` files from git index
  - [ ] Re-check for tracked large binaries and confirm archive placement

### Phase 15: Mobile/iPad Layout Bugs (Horizontal Scroll + “Grey Layer”)
> Goal: Ensure there is no horizontal scrolling on mobile/iPad and remove the grey scroll artifact.

- [x] **Fix horizontal scroll on mobile + iPad (site-wide)**
  - [x] Identify overflowing element(s) via DevTools “Layout/Overflow” inspection
  - [x] Likely root cause: `.alternating-sections` full-bleed CSS in `web/css/layout.css`
  - [x] Implement a robust full-bleed background approach that does not widen layout (e.g. pseudo-element background), and/or apply overflow containment where appropriate
  - [x] Verify on:
    - [x] iPhone Safari
    - [x] iPad Safari
    - [x] Desktop responsive emulation

- [x] **Remove “grey layer” artifact on landing page scroll**
  - [x] Determine whether artifact is caused by alternating section backgrounds (`--bg-alt`) or by fixed/sticky overlays (chart dock, scroll navigator)
  - [x] Fix by adjusting alternating background implementation and/or z-index/background rules
  - [x] Regression check on summary + research pages

### Phase 16: Content Enrichment (Website)
> Goal: Incorporate the best “paper primitives” into the website (research-first), and surface rationales in the database UX.

- [x] **Decision Framework block (model + predictions)**
  - [x] Add a “Decision Framework” section on Research pages that explains:
    - [x] cost model (standing centralization cost + time × damage rate + blast radius)
    - [x] three predictions and what the dataset shows
  - [x] Decide placement (preferred: `research/framework/` and/or `research/all/`)

- [x] **Framework page rewrite pass (`/research/framework/`)**
  - [x] Make the cost model explicit (define each term, not just the equation)
  - [x] Add the three predictions as scannable bullets and tie each to a chart reference
  - [x] Add a short “how to use this” checklist for protocol designers

- [x] **Taxonomy explainer (Scope × Authority) in Research**
  - [x] Add a dedicated taxonomy explainer module/section under Research (preferred over Summary)
  - [x] Include clear definitions + a small set of example cells
  - [x] Add 2–4 canonical examples with deep links into the database (`database.html?id=` or `?search=`)

- [x] **Database: show classification rationales**
  - [x] Audit how `interventions.json` is used in `database.html` modal
  - [x] Display “Scope rationale” and “Authority rationale” (where available) in the incident detail view
  - [x] Confirm any proactive-only cases are handled gracefully

- [x] **Consistency pass: links + counts**
  - [x] Standardize NotebookLM link to: https://notebooklm.google.com/notebook/98177ced-1daf-468f-8e89-81f018a5d25c
  - [x] Ensure all docs/site copy consistently reflects:
    - [x] `lif_all_interventions.csv`: 130 rows
    - [x] `lif_intervention_metrics.csv`: 52 rows
    - [x] Metrics set includes 7 incident_ids not present in `lif_all_interventions.csv` (proactive / non-exploit responses)

### Phase 17: Database Publish-Ready UX (Defer implementation until review)
> Goal: Make the database page feel “finished” for public launch while preserving the deep-link contract.

- [x] **Proactive indicator UX**
  - [x] Add a visible badge/label for proactive / metrics-only cases (`is_proactive = true`)
  - [x] Add a filter toggle: “Include proactive cases” (default on) and/or “Only proactive”
  - [x] Ensure proactive cases render cleanly even if exploit-linked fields are missing

- [x] **Rationales UX**
  - [x] In modal: show “Scope rationale” + “Authority rationale” blocks (if present)
  - [x] In table: optionally add an icon or subtle hint that rationales exist (modal-only is acceptable)

- [x] **Deep-link stability audit**
  - [x] Preserve and re-test: `database.html?search=`, `database.html?id=`
  - [x] Preserve and re-test inbound links from landing/research pages

- [x] **Polish**
  - [x] Loading/empty states: ensure they work across slow networks
  - [x] Table overflow + mobile readability pass

### Phase 18: Content Consistency + Enrichment Sweep (Review-first)
> Goal: Tighten narrative consistency across pages (counts/claims/terminology) and add small high-leverage cross-links.

- [x] **Research hub (`/web/research/index.html`) consistency pass**
  - [x] Reconcile vector counts used in the theme hero blurbs with canonical chart data (e.g., Key Compromise count)
  - [ ] Add 1–2 deep links per theme blurb to the relevant charts (`/research/all/?chart=`)

- [x] **All-charts narrative (`/web/research/all/`) copy audit**
  - [x] Ensure intervention counts language is consistent (130 exploit-linked interventions; 7 proactive metrics-only are separate)
  - [x] Add a short “What to do next” block at Part boundaries with deep links (e.g., “open the database filtered to this theme”)

- [x] **Threat page (`/web/research/threat/`) vector-count alignment**

### Phase 22: Positioning + Share Cards + Research/All UX
> Goal: Keep the site intervention-forward (legitimacy + effectiveness), avoid brittle hard-coded numbers, improve share previews, and add a fast overview mode for the 50-chart narrative.

- [ ] **Landing positioning refresh (`/web/index.html`)**
  - [ ] Add an intervention-forward paragraph aligned with paper abstract/intro (Option A: immediately after hero)
  - [x] Add inline intervention charts: chart19 (sticky dock), chart40/chart41 (inline figures)
  - [ ] Keep author line on landing only
  - [ ] Remove brittle hard-coded counts/totals from landing lead copy
  - [ ] Replace Top Attack Vectors chart with Vector Evolution chart in sticky dock

- [ ] **Chart dock titles + captions**
  - [x] Ensure chart dock header shows human titles (not raw chart ids)
  - [x] Add missing title mappings for charts used on landing (chart19, chart40, chart41, vector evolution chart)

- [ ] **Research/all overview UX**
  - [ ] Prereq: push current state to GitHub before starting UX build
  - [ ] Add an “overview dashboard” section at top for series charts
  - [ ] Implement grid toggle:
    - [ ] Grid mode: fast thumbnail/cards that jump to chart sections
    - [ ] Dense mode: existing narrative scroll experience
  - [x] Verify all vector counts in the lead paragraphs match the dataset used for Chart 09/10
  - [x] Standardize terminology between “Key Compromise”, “Access Control / Key Compromise”, and related labels

- [x] **Landing page (`/web/index.html`) cross-link enrichment**
  - [x] Add deep links from each section to the relevant Research chart and/or Database filtered view
  - [x] Add a single sentence clarifying that “Documented interventions” refers to exploit-linked cases (130) and that the web export includes 7 proactive metrics-only records

- [x] **Summary page (`/web/summary/`) dataset nuance**
  - [x] Add a one-line note near “Documented interventions” clarifying 130 exploit-linked vs 7 proactive metrics-only cases
  - [x] Add a deep link to the Database interventions view and a deep link to the Framework page’s Decision Framework section

- [x] **Framework page styling consistency**
  - [x] Refactor “Three predictions”, “How to use this”, and “Taxonomy” sections to use theme-info/theme-description/theme-link structure for consistent spacing and CTA styling

---

### Scroll Navigator
- `web/js/scroll_navigator.js` (4.7KB) — Currently loaded on 7 pages
- Generates dot indicators from `<section>` elements with `data-section-label` attributes
