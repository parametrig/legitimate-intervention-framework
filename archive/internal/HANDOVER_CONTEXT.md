# Handover Context: Project LIF & Web Development

**Date:** Feb 15, 2026
**Status:** ArXiv Published (2602.12260), Conference Applications Submitted, Content Sprint Complete
**Current Focus:** OSS launch cleanup (archive-first), mobile/iPad horizontal scroll fix, “grey layer” scroll artifact, and research-page content enrichment

---

## 🚀 Completed Work

### Academic & Research Milestones
1. **ArXiv Publication:** [arXiv:2602.12260](https://arxiv.org/pdf/2602.12260)
2. **Conference Circuit:** D² (Academic), TERSE (Governance), Rekt Summit (Security)
3. **TheDAO Fund:** EOI drafted

### Technical Infrastructure ✅
1. **Dataset v1.0:** 705 exploits (601 LIF-relevant), $78.805B losses, 130 interventions, 52 metrics
2. **Website IA:** 7 page types with directory-based routing
3. **50 Interactive Charts:** ECharts 5 with JSON spec pipeline
4. **Deep Linking:** database search/modal, research chart links
5. **Universal Aesthetics:** 680px column, Newsreader typography, mobile dock

### Dataset Reality Check (From `data/refined/`)
- `data/refined/lif_exploits_final.csv`: **705** rows
- `data/refined/lif_all_interventions.csv`: **130** rows
- `data/refined/lif_intervention_metrics.csv`: **52** rows
- The 52 “high-fidelity metrics” set includes **7** `incident_id`s that do not appear in `lif_all_interventions.csv` (these appear to be proactive / non-exploit responses, and should be explained consistently across docs and website copy).

### Content Integration Sprint (Phases 1-7) ✅
- 8-section landing page with inline figures and media links
- 50 chart descriptions enriched with ArXiv paper data
- Summary page with key metrics table
- About page with methodology, limitations, acknowledgements
- 4 theme pages enriched (26 charts + 9 annotations)
- 8 transparent images for landing page
- Hero section: masked audio player, corrected IMDB/ArXiv links, reordered actions

---

## 🎯 Current Sprint: Phases 8-13

See [`TODO.md`](./TODO.md) for the full phased plan.

| Phase | Focus | Status |
|-------|-------|--------|
| 8 | Persistent Audio Player & Dock | ✅ |
| 9 | Database Verification & Deep Linking | ✅ |
| 10 | Scroll Navigator & Visual Polish | ✅ |
| 11 | Site-Wide Features (Banner, Footer) | ✅ |
| 12 | Design System & CSS Cleanup | ⬜ |
| 13 | Final QA, Cleanup & Launch | ✅ |

---

## 🧹 New Sprint: OSS Launch Cleanup + Content Enrichment (Review-First)

See `TODO.md` Phase 14–16 for the detailed phased plan.

Key decisions:
- Internal docs (project-management) are **not public** and should move to `archive/internal/`.
- PDFs: keep the concise/main PDFs committed (descriptive naming preferred).
- Anything not needed for the main tree should be **moved into `archive/`** (not deleted) until final review.

---

## 📁 Critical Files

### Core Data & Analysis
- `data/refined/lif_exploits_final.csv` — 705 rows
- `data/refined/lif_all_interventions.csv` — 130 rows
- `data/refined/lif_intervention_metrics.csv` — 52 rows
- `data/refined/lif_stats.json` — Standardized stats

### Web Frontend
- `web/js/echarts_runtime.js` — Chart loading, rendering, theming
- `web/js/main.js` — Primary page logic
- `web/js/narrative_runtime.js` — Page interactivity, dock
- `web/js/scroll_navigator.js` — Side TOC (loaded on 7 pages)
- `web/data/exploits.json` — Database source (exploits)
- `web/data/interventions.json` — Database source (interventions)
- `web/data/charts/*.json` — 50 chart specs
- `web/audio/code_is_law_vs_kill_switch.m4a` — Documentary audio

### CSS
- `web/css/base.css` — Base styles
- `web/css/layout.css` — Grid system & containers
- `web/css/pages/` — Page-specific styles (6 files)
- `web/css/style.css.bak` — Legacy backup (to be deleted in Phase 12)

### Documentation
- `TODO.md` — Phased execution checklist
- `HANDOVER_CONTEXT.md` — This file

---

*Last updated: Feb 15, 2026 — OSS cleanup + mobile layout bugs + content enrichment phased plan added to TODO*
