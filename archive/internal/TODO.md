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

- [x] **Chart dock titles + captions**
  - [x] Ensure chart dock header shows human titles (not raw chart ids)
  - [x] Add missing title mappings for charts used on landing (chart19, chart40, chart41, vector evolution chart)

- [x] **Sticky chart transitions**
  - [x] Verify scroll-to-scroll chart changes do not flash fallback PNGs (desktop + mobile)
  - [x] If any chart still flashes, tune the fallback delay and/or add a “latest request wins” guard

## ✅ Completed Phases

### Phase 22: Positioning + Share Cards + Research/All UX ✅
- [x] Landing positioning refresh (intervention-forward paragraph, inline charts, author line)
- [x] Chart dock titles + captions (human titles, missing mappings)
- [x] Landing page cross-link enrichment (deep links to research/database)
- [x] Summary page dataset nuance (130 vs 7 cases clarification)
- [x] Framework page styling consistency (theme-info structure)
- [x] Per-page social cards (stable og:image + twitter:image)
- [x] Research hub consistency pass (vector counts, deep links)
- [x] All-charts narrative copy audit (intervention counts, what to do next)
- [x] Threat page vector-count alignment

### Phase 18: Content Consistency + Enrichment Sweep ✅
- [x] Research hub consistency pass (vector counts, deep links)
- [x] All-charts narrative copy audit (intervention counts, what to do next)
- [x] Threat page vector-count alignment

### Phase 17: Database Publish-Ready UX ✅
- [x] Proactive indicator UX (badges, filter toggle)
- [x] Rationales UX (scope + authority in modal)
- [x] Deep-link stability audit (search, id parameters)
- [x] Polish (loading states, mobile readability)

### Phase 16: Content Enrichment (Website) ✅
- [x] Decision Framework block (model + predictions)
- [x] Framework page rewrite pass (cost model, predictions, checklist)
- [x] Taxonomy explainer (Scope × Authority)
- [x] Database: show classification rationales
- [x] Consistency pass: links + counts

### Phase 15: Mobile/iPad Layout Bugs ✅
- [x] Fix horizontal scroll on mobile + iPad (site-wide)
- [x] Remove "grey layer" artifact on landing page scroll

### Phase 14: Archive + Git Hygiene ✅
- [x] Create archive structure
- [x] Move internal docs out of main tree
- [x] Archive large / temporary assets
- [x] Gnosis framework documents + embedded images
- [x] Treat visualizations/ as build artifact
- [x] Git hygiene

### Summary ✅ (compressed)
- [x] IA + 50 interactive charts + dataset v1.0 wired to web exports
- [x] Landing/Summary/About/Research pages populated and styled
- [x] Deep links + scroll navigator + mobile dock + audio dock
- [x] Baseline QA + SEO tags
- [x] Feb 16: sticky chart sizing/typography tweaks + reduced fallback flash during swaps

---

## 🔄 Remaining Work

### Phase 23: Design System & Typography Cleanup (Next Sprint)
> Goal: Consolidate CSS into proper design system, fix typography consistency, and refine visual hierarchy.

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
- [ ] Create `web/css/tokens.css` with design tokens:
  - Authority colors (Blue / Green / Purple)
  - Accent color (Cyan)
  - Typography scale
  - Spacing scale
- [ ] Restructure CSS directory for maintainability
- [ ] Refactor `base.css` and `layout.css` to consume `tokens.css`
- [ ] Update `echarts_runtime.js` to use `getComputedStyle()` for theme colors
- [ ] Delete `style.css.bak` and any unused CSS
- [ ] Typography consistency pass across all pages
- [ ] Color system audit and standardization
- [ ] Component library cleanup

### Phase 22: Research/all Overview UX (Deferred)
> Goal: Add fast overview mode for the 50-chart narrative.

- [ ] **Research/all overview UX** (Deferred)
  - [x] Prereq: push current state to GitHub before starting UX build
  - [ ] Add an "overview dashboard" section at top for series charts
  - [ ] Implement grid toggle:
    - [ ] Grid mode: fast thumbnail/cards that jump to chart sections
    - [ ] Dense mode: existing narrative scroll experience
  - [x] Verify all vector counts in the lead paragraphs match the dataset used for Chart 09/10
  - [x] Standardize terminology between "Key Compromise", "Access Control / Key Compromise", and related labels


---

### Scroll Navigator
- `web/js/scroll_navigator.js` (4.7KB) — Currently loaded on 7 pages
- Generates dot indicators from `<section>` elements with `data-section-label` attributes
