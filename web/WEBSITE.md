# LIF Website — Developer Documentation

> Comprehensive guide to the Legitimate Intervention Framework website:
> architecture, design system, chart pipeline, and deployment.

---

## Table of Contents

1. [Architecture](#architecture)
2. [Design System](#design-system)
3. [Chart Pipeline](#chart-pipeline)
4. [Color Reference](#color-reference)
5. [Typography](#typography)
6. [Development](#development)
7. [Deployment](#deployment)

---

## Architecture

### Directory Structure

```
web/
├── index.html              # Landing page (hero, inline charts, CTAs)
├── about.html              # About, key findings, collapsible sections
├── database.html           # Searchable exploit database
├── research.html           # Research hub redirect
├── research/
│   ├── index.html          # Research themes overview
│   ├── all/index.html      # All charts consolidated
│   ├── threat/index.html   # Threat landscape narrative
│   ├── intervention/index.html
│   ├── efficiency/index.html
│   └── framework/index.html
├── css/
│   ├── tokens.css          # Design tokens (single source of truth)
│   ├── base.css            # Reset, grid, layout primitives
│   ├── layout.css          # Navigation, footer, banner, responsive
│   ├── components/
│   │   └── audio-player.css
│   └── pages/
│       ├── home.css        # Landing page styles
│       ├── about.css       # About page styles
│       ├── database.css    # Database page styles
│       ├── narrative.css   # Narrative/research page styles
│       ├── research.css    # Research theme styles
│       └── research-index.css
├── js/
│   ├── main.js             # Navigation, search, database logic
│   ├── echarts_runtime.js  # Chart rendering engine + theme
│   ├── narrative_runtime.js # Scroll-synced narrative charts
│   ├── audio_player.js     # Podcast player
│   ├── banner.js           # Development banner
│   └── scroll_navigator.js # Section scroll tracking
├── ../functions/
│   └── api/risk/[resource].js # Cloudflare Pages proxy for database datasets
├── data/
│   ├── charts/             # 50+ ECharts JSON specs (generated)
│   ├── exploits.json       # Local-dev fallback only; normalized to match infrastructure canonical JSON
│   └── interventions.json  # Local-dev fallback only; normalized to match infrastructure canonical JSON
└── favicon.svg
```

### CSS Load Order

Every HTML page loads stylesheets in this order:

```html
<link rel="stylesheet" href="/css/tokens.css">   <!-- 1. Tokens -->
<link rel="stylesheet" href="/css/base.css">      <!-- 2. Base/Reset -->
<link rel="stylesheet" href="/css/layout.css">    <!-- 3. Layout -->
<link rel="stylesheet" href="/css/pages/X.css">   <!-- 4. Page-specific -->
```

`tokens.css` is **always first** — all other CSS files reference its variables.

### JavaScript Architecture

| File | Purpose | Loaded On |
|------|---------|-----------|
| `echarts_runtime.js` | Chart rendering, theme, data loading | All pages with charts |
| `main.js` | Navigation, database search, filters | All pages |
| `narrative_runtime.js` | Scroll-synced chart/annotation flow | Narrative pages |
| `audio_player.js` | Podcast player widget | Landing page |
| `scroll_navigator.js` | Active section tracking | Narrative pages |
| `banner.js` | Development banner dismiss | All pages |

Database data-loading model:

- production: same-origin Cloudflare Pages Function proxy at `/api/risk/exploits` and `/api/risk/interventions`
- local static dev: falls back to `web/data/*.json` when the proxy is unavailable on `localhost`
- charts: still read static `web/data/charts/*.json` and `web/data/series/*.json`
- local fallback files are expected to follow the same normalized raw-data structure as the infrastructure repo, not the older metadata-envelope export shape

---

## Design System

### Token Architecture

All visual values are defined as CSS custom properties in `tokens.css`:

#### Backgrounds
| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg` | `#faf9f6` | Page background (warm cream) |
| `--color-bg-alt` | `#f4f4f2` | Alternating sections |
| `--color-bg-surface` | `#f9f9f9` | Cards, code blocks |
| `--color-bg-hover` | `rgba(0,0,0,0.04)` | Interactive hover |

#### Text
| Token | Value | Usage |
|-------|-------|-------|
| `--color-text` | `#1a1a1a` | Primary — body, headings |
| `--color-text-secondary` | `#666666` | Metadata, captions, nav |
| `--color-text-tertiary` | `#999999` | Muted labels, timestamps |
| `--color-text-inverse` | `#ffffff` | Text on dark backgrounds |

#### Borders
| Token | Value | Usage |
|-------|-------|-------|
| `--color-border` | `#e5e5e5` | Standard dividers |
| `--color-border-light` | `#eeeeee` | Subtle separators |
| `--color-border-strong` | `#d4d4d4` | Heavy dividers |

### CSS Class Conventions

| Pattern | Example | Usage |
|---------|---------|-------|
| `.theme-*` | `.theme-quicklinks` | Reusable themed components |
| `.landing-*` | `.landing-action-btn` | Landing page components |
| `.key-findings` | `.key-findings table` | About page key findings |
| `.collapsible-*` | `.collapsible-group` | Expandable section wrappers |
| `.text-small` | — | Small body text (0.875rem) |
| `.metadata-bar` | — | Inline metadata (date, authors) |

---

## Chart Pipeline

### Overview

```
data/refined/*.csv
    ↓ (Python reads CSVs)
scripts/gen_charts_shared.py   ← Color palette, data loading
scripts/gen_charts_batch0.py   ← Charts 01-11
scripts/gen_charts_batch1.py   ← Charts 12-17
scripts/gen_charts_batch2.py   ← Charts 19-25
scripts/gen_charts_batch3.py   ← Charts 28-35
scripts/gen_charts_batch4.py   ← Charts 37-42
scripts/gen_charts_batch5.py   ← Charts 44-49
scripts/gen_charts_batch6.py   ← Charts 18, 26-27, 36, 43, 47, 50
    ↓ (JSON output)
web/data/charts/chartNN_name.json
    ↓ (Browser fetches JSON)
web/js/echarts_runtime.js      ← Registers theme, renders charts
```

### How It Works

1. **`gen_charts_shared.py`** defines the `C` color palette, semantic color maps (`AUTH_COLORS`, `SCOPE_COLORS`, `LOSS_COLORS`), data loading, and JSON helpers.

2. **Batch scripts** import `from gen_charts_shared import *`, query the CSV data with pandas, and build ECharts option objects with `itemStyle.color` referencing `C["blue"]`, `C["green"]`, etc. Each chart is saved as `{chart: optionObject}` JSON.

3. **`echarts_runtime.js`** at runtime:
   - Reads CSS variables from `tokens.css` via `getComputedStyle()` 
   - Registers these as `LIF_COLORS` (matching the same keys as the Python `C` dict)
   - Applies the `LIF` ECharts theme (font, grid, tooltip defaults)
   - Fetches chart JSON specs and renders them into `<div>` containers

### Regenerating Charts

```bash
# From repo root:
.venv/bin/python3 scripts/generate_all_charts.py

# Output: web/data/charts/*.json (50+ files)
# All 7 batches should complete with ✓ marks.
```

### Adding a New Chart

1. Choose the appropriate batch script (by chart number range)
2. Use the shared palette: `C["blue"]`, `C["green"]`, `C["red"]`, etc.
3. Use semantic maps for authority/scope: `AUTH_COLORS["Signer Set"]`
4. Call `save("chartNN_name", { ... })` with an ECharts option dict
5. Add the chart container to the appropriate HTML page
6. Register the chart in `echarts_runtime.js` if needed for narrative pages

---

## Color Reference

### Core Palette (11 Colors)

All colors are shared identically between `tokens.css`, `echarts_runtime.js`, and `gen_charts_shared.py`.

| Name | Hex | CSS Variable | Usage |
|------|-----|-------------|-------|
| **blue** | `#2563EB` | `--authority-blue` | Signer Set authority |
| **green** | `#16A34A` | `--authority-green` | Delegated Body authority, success |
| **purple** | `#7C3AED` | `--authority-purple` | Governance authority |
| **red** | `#DC2626` | `--color-danger` | Losses, errors |
| **amber** | `#D97706` | `--color-warning` | Cautions, warnings |
| **slate** | `#475569` | `--chart-slate` | Neutral chart series |
| **gray** | `#6B7280` | `--chart-gray` | Unknown categories |
| **lgray** | `#9CA3AF` | `--chart-gray-light` | Light neutral |
| **lblue** | `#60A5FA` | `--chart-blue-light` | Light blue variant |
| **ink** | `#1E293B` | `--chart-ink` | Dark emphasis |
| **accent** | `#B8860B` | `--color-accent` | Hover highlights (CSS-only) |

### Semantic Color Maps

#### Authority Colors
| Authority | Color | Hex |
|-----------|-------|-----|
| Signer Set | blue | `#2563EB` |
| Delegated Body | green | `#16A34A` |
| Governance | purple | `#7C3AED` |
| Unknown | gray | `#6B7280` |

#### Scope Colors
| Scope | Color | Hex |
|-------|-------|-----|
| Network | red | `#DC2626` |
| Protocol | amber | `#D97706` |
| Asset | purple | `#7C3AED` |
| Module | lblue | `#60A5FA` |
| Account | green | `#16A34A` |

#### Loss Colors
| Category | Color | Hex |
|----------|-------|-----|
| Incurred / Lost | red | `#DC2626` |
| Saved / Prevented | green | `#16A34A` |

---

## Typography

### Font Stack
| Token | Value | Usage |
|-------|-------|-------|
| `--font-serif` | `Newsreader, Georgia, serif` | Body text, headings, charts |
| `--font-sans` | `system-ui, -apple-system, sans-serif` | UI elements |
| `--font-mono` | `ui-monospace, SFMono-Regular, Menlo...` | Code blocks |

### Type Scale
| Token | Size | Usage |
|-------|------|-------|
| `--fs-h1` | 3rem (48px) | Hero headings |
| `--fs-h2` | 2rem (32px) | Section headers |
| `--fs-h3` | 1.5rem (24px) | Subheaders |
| `--fs-h4` | 1.125rem (18px) | Small headers |
| `--fs-p` | 1.125rem (18px) | Body text |
| `--fs-lead` | 1.25rem (20px) | Lead paragraphs |
| `--fs-small` | 0.875rem (14px) | Small text |
| `--fs-tiny` | 0.75rem (12px) | Tags, timestamps |

### Chart Typography
All charts use `Newsreader, Georgia, serif` via the `LIF` ECharts theme. Title size: 24px. Legend size: 8.25px.

---

## Development

### Prerequisites
- Python 3.11+ with pandas, numpy
- Any local HTTP server (e.g., `python3 -m http.server`)

### Running Locally

```bash
# Start dev server from web/ directory:
cd web && python3 -m http.server 8888

# Open http://localhost:8888
```

### Full Rebuild

```bash
# 1. Regenerate chart JSON specs:
.venv/bin/python3 scripts/generate_all_charts.py

# 2. Verify locally:
cd web && python3 -m http.server 8888
```

### Style Changes

1. **Colors/spacing** — Edit `css/tokens.css` (all CSS references update automatically)
2. **Chart colors** — Edit `scripts/gen_charts_shared.py` `C` dict, then regenerate charts
3. **Runtime theme** — `LIF_COLORS` in `echarts_runtime.js` reads from CSS variables at load time
4. **Page styles** — Edit the relevant file in `css/pages/`

---

## Deployment

### Hosting Compatibility

The site is a **static site** (HTML + CSS + JS) with no server-side rendering or build step. It is compatible with:

| Platform | Notes |
|----------|-------|
| **Vercel** | Deploy the `web/` directory; no build command needed |
| **Cloudflare Pages** | Point to `web/` as output directory and keep `functions/` at repo root for the database proxy |
| **IPFS** | All paths are relative; works with any gateway |
| **GitHub Pages** | Serve from `web/` directory |

### Key Compatibility Notes

- **No build step required** — all files are production-ready as-is
- **Relative paths** — all asset and data references use relative paths for IPFS compatibility
- **Pages Functions optional but now used in production** — the Database view proxies raw dataset reads through `functions/api/risk/[resource].js`
- **Chart payloads remain static** — `web/data/charts/` and `web/data/series/` are still served as generated static JSON
- **Font loading** — `Newsreader` loaded from Google Fonts CDN; works on all platforms
- **ECharts** — loaded from CDN (`cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js`)

