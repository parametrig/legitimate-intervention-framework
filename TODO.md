# Legitimate Intervention Framework (LIF) — TODO Tracker

**Purpose**: Step-by-step execution checklist for completing the LIF website.
**Last updated**: Feb 14, 2026

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

- [ ] **Verify `exploits.json`**: Confirm it matches `lif_exploits_final.csv` (705 rows, correct fields)
- [ ] **Verify `interventions.json`**: Confirm it matches `lif_all_interventions.csv` (130 rows)
- [ ] **Deep linking audit**:
  - [ ] `database.html?search=<term>` — filters correctly
  - [ ] `database.html?id=<incident_id>` — opens correct modal
  - [ ] Links from landing page, summary, theme pages → database cases work
  - [ ] Links from database → research charts work
- [ ] **Cross-page linking**: Verify all internal links across the site resolve correctly
  - [ ] Landing page section links
  - [ ] Research hub → theme page links
  - [ ] Theme page chart → `/research/all/?chart=` links
  - [ ] About page → database, ArXiv, IMDB links
- [ ] **Modal/detail view**: Verify incident detail modal renders correctly with all fields

### Phase 10: Scroll Navigator & Visual Polish
> Goal: Enhance the scroll navigator on all pages and introduce alternating-line design.

- [ ] **Scroll navigator audit**: Ensure `scroll_navigator.js` is loaded and functional on all pages:
  - [ ] Landing (`index.html`) — 8 sections labeled
  - [ ] Summary (`summary/index.html`)
  - [ ] Research hub (`research/index.html`)
  - [ ] All 4 theme pages (threat, intervention, efficiency, framework)
  - [ ] All charts (`research/all/index.html`) — 50 chart labels
- [ ] **Navigator detail**: Ensure each nav dot/label accurately reflects its section title
- [ ] **Alternating-line styling**: Add subtle alternating background shading for section readability
  - [ ] Landing page narrative sections
  - [ ] Research theme pages (chart sections)
  - [ ] All charts page (chart blocks)
  - [ ] Summary page sections
- [ ] Verify scroll navigator doesn't conflict with mobile navigation or back arrow

### Phase 11: Site-Wide Features
> Goal: Add global UX elements across all pages.

- [ ] **Dismissible banner**: "This site is under active development. Corrections welcome." on all pages
  - Dismiss state saved to `localStorage`
- [ ] **Site-wide footer**: Comprehensive footer with:
  - Research disclaimer statement
  - Links: Terms, Privacy, Request Correction, GitHub, ArXiv
  - Contact: karo@parametrig.com
  - Tip/donation address (parametrig.eth)
- [ ] **Correction contact**: Add "Report an error" link/method accessible from every page

### Phase 12: Design System & CSS Cleanup
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

### Phase 13: Final QA, Cleanup & Launch Prep
> Goal: Final pass before deployment.

- [ ] **Cross-browser testing**: Chrome, Safari, Firefox (desktop + mobile)
- [ ] **Performance audit**: Lighthouse scores, image optimization, lazy loading for charts
- [ ] **Accessibility check**: Alt text, ARIA labels, keyboard navigation
- [ ] **SEO verification**: Meta tags, Open Graph, Twitter Cards on all pages
- [ ] **Dead link scan**: Verify zero broken links across the site
- [ ] **Console error sweep**: Zero errors on all pages
- [ ] **Git cleanup**: Remove tracked large files (`.m4a` in root), ensure `.gitignore` is complete
- [ ] **Repository README update**: Reflect current site structure and features
- [ ] **Update HANDOVER_CONTEXT.md** and **TODO.md** to "launch-ready" state
- [ ] **Deployment**: Push to production (Cloudflare Pages / Vercel / IPFS)
- [ ] **DNS / Domain**: Verify `legitimate-intervention.org` resolves correctly

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
