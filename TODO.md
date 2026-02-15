# Legitimate Intervention Framework (LIF) — TODO Tracker

**Purpose**: Step-by-step execution checklist for completing the LIF website.
**Last updated**: Feb 15, 2026

---

## ✅ Completed Phases

### Phase 0: Core Infrastructure ✅
- [x] Website IA established (/, /summary, /research/, /research/<theme>/, /research/all/, /database.html, /about.html)
- [x] ECharts integration with 50 interactive charts
- [x] Dataset v1.0 finalized (705 exploits, 130 interventions, 52 metrics)
- [x] Static hosting compatibility (IPFS-ready, directory-based routing)
- [x] Deep-linking (database.html?search=, ?id=, research/?chart=)
- [x] Universal aesthetic standardization (680px column, Newsreader typography)
- [x] Mobile responsive design with dock optimization

### Content Integration Sprint ✅
- [x] Phase 1: Landing page expanded to 8 narrative sections
- [x] Phase 2: 50 chart descriptions enriched with ArXiv data
- [x] Phase 3: Summary page enriched with key metrics table
- [x] Phase 4: About page refresh (methodology, limitations, acknowledgements)
- [x] Phase 5: Research theme pages enriched (26 charts + 9 annotations)
- [x] Phase 6: Visual polish (8 transparent images)
- [x] Phase 7: Hero refinement (audio embed, IMDB link, ArXiv PDF link, button reorder)

---

## 🔄 Remaining Phases

### Phase 8: Persistent Audio Player & Dock ✅
> Goal: Audio continues playing across page navigation with a persistent mini-player dock.

- [x] **Cross-page audio persistence**: Implement a persistent audio player that survives page navigation
  - Option A: Service Worker + `<iframe>` shell (SPA-like wrapper)
  - Option B: `sessionStorage` + `currentTime` resume on each page load (Selected)
  - Option C: Lightweight SPA wrapper with `fetch` + `history.pushState` for page transitions
- [x] **Mini-player dock**: Floating dock (similar to mobile chart dock) with play/pause, forward/rewind, progress bar
  - Appears when user clicks "listen", persists at bottom of viewport
  - Dismissible via close button (stops playback)
  - Responsive: works on mobile and desktop
- [x] **Playback state**: Save `currentTime` to `sessionStorage` so refreshing the page resumes from where user left off
- [x] Ensure dock doesn't conflict with mobile chart dock or scroll navigator

### Phase 9: Database Verification & Deep Linking
> Goal: Ensure the database page uses the latest JSON data and all cross-linking works.

- [x] **Verify `exploits.json`**: Confirm it matches `lif_exploits_final.csv` (705 rows, correct fields)
- [x] **Verify `interventions.json`**: Confirm it matches `lif_all_interventions.csv` (130 rows)
- [x] **Deep linking audit**:
  - [x] `database.html?search=<term>` — filters correctly
  - [x] `database.html?id=<incident_id>` — opens correct modal
  - [x] Links from landing page, summary, theme pages → database cases work
  - [x] Links from database → research charts work
- [x] **Cross-page linking**: Verify all internal links across the site resolve correctly
  - [x] Landing page section links
  - [x] Research hub → theme page links
  - [x] Theme page chart → `/research/all/?chart=` links
  - [x] About page → database, ArXiv, IMDB links
- [x] **Modal/detail view**: Verify incident detail modal renders correctly with all fields

### Phase 10: Scroll Navigator & Visual Polish
> Goal: Enhance the scroll navigator on all pages and introduce alternating-line design.

- [x] **Scroll navigator audit**: Ensure `scroll_navigator.js` is loaded and functional on all pages:
  - [x] Landing (`index.html`) — 8 sections labeled
  - [x] Summary (`summary/index.html`)
  - [x] Research hub (`research/index.html`)
  - [x] All 4 theme pages (threat, intervention, efficiency, framework)
- [x] **Navigator detail**: Ensure each nav dot/label accurately reflects its section title
- [x] **Alternating-line styling**: Add subtle alternating background shading for section readability
  - [x] Landing page narrative sections
  - [x] Research theme pages (chart sections)
  - [x] All charts page (chart blocks)
  - [x] Summary page sections
- [x] Verify scroll navigator doesn't conflict with mobile navigation or back arrow

### Phase 11: Site-Wide Features ✅
> Goal: Add global UX elements across all pages.

- [x] **Dismissible banner**: "This site is under active development. Corrections welcome." on all pages
  - Dismiss state saved to `localStorage`
- [x] **Site-wide footer**: ~~Comprehensive footer~~ (CANCELLED per user request)

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

### Phase 13: Final QA, Cleanup & Launch Prep ✅
> Goal: Final pass before deployment.

- [x] **Cross-browser testing**: Chrome, Safari, Firefox (desktop + mobile)
- [x] **Performance audit**: Lighthouse scores, image optimization, lazy loading for charts
- [x] **Accessibility check**: Alt text, ARIA labels, keyboard navigation
- [x] **SEO verification**: Meta tags, Open Graph, Twitter Cards on all pages
- [x] **Dead link scan**: Verify zero broken links across the site
- [x] **Console error sweep**: Zero errors on all pages
- [x] **Git cleanup**: Remove tracked large files (`.m4a` in root), ensure `.gitignore` is complete
- [x] **Repository README update**: Reflect current site structure and features
- [x] **Update HANDOVER_CONTEXT.md** and **TODO.md** to "launch-ready" state
- [ ] **Deployment**: Push to production (Cloudflare Pages / Vercel / IPFS)
- [ ] **DNS / Domain**: Verify `legitimate-intervention.org` resolves correctly

---

## 🧹 OSS Launch Cleanup + Content Enrichment (Review-First)

### Phase 14: Archive Pass + Repo Hygiene (No deletions without explicit approval)
> Goal: Prepare repository structure for open-source launch by moving non-essential assets into `archive/` and tightening repo hygiene.

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

- [ ] **Create archive structure**
  - [ ] Add `archive/` top-level directory
  - [ ] Add `archive/internal/` (private project-management docs + internal references)
  - [ ] Add `archive/media/` (screenshots, large binaries, legacy visuals)
  - [ ] Add `archive/manuscript/` (older drafts / non-shipping writeups)

- [ ] **Move internal docs out of main tree (not public)**
  - [ ] Move `TODO.md` → `archive/internal/TODO.md`
  - [ ] Move `HANDOVER_CONTEXT.md` → `archive/internal/HANDOVER_CONTEXT.md`
  - [ ] Replace with minimal public-facing equivalents (TBD) only if needed for contributors (user preference: likely none)

- [ ] **Archive large / temporary assets**
  - [ ] Move website screenshots (e.g. `web/Screenshot*.png`, `web/screencapture-*.png`) → `archive/media/`
  - [ ] Ensure only one canonical audio file is shipped for the site (keep under `web/audio/`)
  - [ ] Move any duplicate/unused large audio files into `archive/media/`

- [ ] **Gnosis framework documents + their embedded images**
  - [ ] Move `manuscript/gnosis_framework_response*.md` into a dedicated directory (e.g. `archive/gnosis/`)
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

- [ ] **Fix horizontal scroll on mobile + iPad (site-wide)**
  - [ ] Identify overflowing element(s) via DevTools “Layout/Overflow” inspection
  - [ ] Likely root cause: `.alternating-sections` full-bleed CSS in `web/css/layout.css`
  - [ ] Implement a robust full-bleed background approach that does not widen layout (e.g. pseudo-element background), and/or apply overflow containment where appropriate
  - [ ] Verify on:
    - [ ] iPhone Safari
    - [ ] iPad Safari
    - [ ] Desktop responsive emulation

- [ ] **Remove “grey layer” artifact on landing page scroll**
  - [ ] Determine whether artifact is caused by alternating section backgrounds (`--bg-alt`) or by fixed/sticky overlays (chart dock, scroll navigator)
  - [ ] Fix by adjusting alternating background implementation and/or z-index/background rules
  - [ ] Regression check on summary + research pages

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

- [ ] **Proactive indicator UX**
  - [ ] Add a visible badge/label for proactive / metrics-only cases (`is_proactive = true`)
  - [ ] Add a filter toggle: “Include proactive cases” (default on) and/or “Only proactive”
  - [ ] Ensure proactive cases render cleanly even if exploit-linked fields are missing

- [ ] **Rationales UX**
  - [ ] In modal: show “Scope rationale” + “Authority rationale” blocks (if present)
  - [ ] In table: optionally add an icon or subtle hint that rationales exist (modal-only is acceptable)

- [ ] **Deep-link stability audit**
  - [ ] Preserve and re-test: `database.html?search=`, `database.html?id=`
  - [ ] Preserve and re-test inbound links from landing/research pages

- [ ] **Polish**
  - [ ] Loading/empty states: ensure they work across slow networks
  - [ ] Table overflow + mobile readability pass

### Phase 18: Content Consistency + Enrichment Sweep (Review-first)
> Goal: Tighten narrative consistency across pages (counts/claims/terminology) and add small high-leverage cross-links.

- [x] **Research hub (`/web/research/index.html`) consistency pass**
  - [x] Reconcile vector counts used in the theme hero blurbs with canonical chart data (e.g., Key Compromise count)
  - [ ] Add 1–2 deep links per theme blurb to the relevant charts (`/research/all/?chart=`)

- [x] **All-charts narrative (`/web/research/all/`) copy audit**
  - [x] Ensure intervention counts language is consistent (130 exploit-linked interventions; 7 proactive metrics-only are separate)
  - [x] Add a short “What to do next” block at Part boundaries with deep links (e.g., “open the database filtered to this theme”)

- [x] **Threat page (`/web/research/threat/`) vector-count alignment**
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

## 📋 Technical Notes

### Audio Player Architecture Decision
The persistent audio player needs to survive page navigation. Three approaches:

1. **SPA Wrapper** (Recommended): Wrap the site in a lightweight shell that loads pages via `fetch` + `history.pushState`, keeping the audio `<iframe>` or `<audio>` element persistent in the shell. This is the most seamless UX but requires refactoring navigation.

2. **sessionStorage Resume**: Save `currentTime` to `sessionStorage` on `beforeunload`, resume on next page's `DOMContentLoaded`. Simple but creates a brief silence gap during navigation.

3. **Service Worker**: Cache the audio and use a service worker to manage playback state. Complex but most robust for offline/PWA scenarios.

### Database JSON Sources
- `web/data/exploits.json` — Generated from `data/refined/lif_exploits_final.csv`
- `web/data/interventions.json` — Generated from `data/refined/lif_all_interventions.csv`
- `web/data/charts/*.json` — 50 ECharts specs
- `web/data/series/*.json` — 4 time series (cumulative, yearly, vector, four-layer)

### Scroll Navigator
- `web/js/scroll_navigator.js` (4.7KB) — Currently loaded on 7 pages
- Generates dot indicators from `<section>` elements with `data-section-label` attributes
