const LIF_COLORS = {
    blue: '#2563EB',
    green: '#16A34A',
    purple: '#7C3AED',
    amber: '#D97706',
    red: '#DC2626',
    slate: '#475569',
    gray: '#6B7280',
    lgray: '#9CA3AF',
    lblue: '#60A5FA',
    ink: '#1E293B',
};

const AUTHORITY_COLORS = {
    'Signer Set': LIF_COLORS.blue,
    'Delegated Body': LIF_COLORS.green,
    'Governance': LIF_COLORS.purple,
    'Unknown': LIF_COLORS.gray,
};

let __lifDataCache = null;

async function loadJson(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`);
    return res.json();
}

async function loadJsonOptional(path) {
    const res = await fetch(path);
    if (res.status === 404) return null;
    if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`);
    return res.json();
}

function unwrapEnvelope(payload) {
    if (Array.isArray(payload)) return payload;
    if (payload && Array.isArray(payload.records)) return payload.records;
    return payload;
}

function reviveFns(obj) {
    if (obj && typeof obj === 'object' && !Array.isArray(obj)) {
        if (Object.keys(obj).length === 1 && typeof obj.$fn === 'string') {
            // Some environments use SES lockdown, which disallows dynamic code evaluation.
            // Treat function placeholders as non-executable and let sanitizers handle common cases.
            return null;
        }
        const out = {};
        for (const [k, v] of Object.entries(obj)) {
            out[k] = reviveFns(v);
        }
        return out;
    }

    if (Array.isArray(obj)) {
        return obj.map(v => reviveFns(v));
    }

    return obj;
}

function __lifAbbreviateValue(v) {
    if (v === null || v === undefined || Number.isNaN(v)) return '—';
    const absV = Math.abs(v);

    // If the value is tiny (e.g. 1.5) but the context is billions, 
    // we shouldn't abbreviate further. 
    // However, if the value is large (e.g. 1,500,000,000), we certainly should.

    if (absV >= 1e9) return (v / 1e9).toFixed(1).replace(/\.0$/, '') + 'B';
    if (absV >= 1e6) return (v / 1e6).toFixed(1).replace(/\.0$/, '') + 'M';
    if (absV >= 1e3) return (v / 1e3).toFixed(1).replace(/\.0$/, '') + 'K';

    // Precision for small numbers
    if (absV < 10 && absV > 0) return v.toFixed(2).replace(/\.?0+$/, '');
    return String(v);
}

function __lifCoerceDollarValueFormatterString(s) {
    if (typeof s !== 'string') return null;

    const hasJsTemplate = s.includes('${value}');
    const hasEchartsTemplate = s.includes('{value}');
    if (!hasJsTemplate && !hasEchartsTemplate) return null;

    return (v) => {
        if (v === null || v === undefined || Number.isNaN(v)) return '—';

        // If the template is JUST the value placeholder, we abbreviate.
        // If it includes other characters (like a suffix 'B' or 'M'), we assume 
        // the value is already pre-scaled and we just replace.
        const isPurePlaceholder = s.trim() === '${value}' || s.trim() === '{value}';
        const isPureDollarPlaceholder = s.trim() === '$${value}' || s.trim() === '${value}' && s.startsWith('$');

        let valStr;
        if (isPurePlaceholder || isPureDollarPlaceholder) {
            valStr = __lifAbbreviateValue(v);
        } else {
            valStr = String(v);
        }

        let out = s;
        // Handle JS template format from some of our Python generators
        out = out.replace(/\$\{value\}/g, valStr);
        // Handle ECharts native template format
        out = out.replace(/\{value\}/g, valStr);

        // Refined currency prefixing: 
        if (!out.startsWith('$') && /^\s*-?\d/.test(out)) {
            const hasCurrencySuffix = /\d\s*[BMKGT]$/.test(out);
            const templateImpliesCurrency = s.startsWith('$');
            if (hasCurrencySuffix || templateImpliesCurrency) return `$${out}`;
        }
        return out;
    };
}

function sanitizeEchartsOption(option) {
    if (!option || typeof option !== 'object') return option;

    const LEGACY_PALETTE = new Set(['#2563EB', '#64748B', '#16A34A', '#D97706', '#93C5FD', '#9CA3AF']);
    const isMobile = window.innerWidth < 768;

    const fixup = (node) => {
        if (!node || typeof node !== 'object') return;

        // Force titles to middle to avoid overlap with labels, unless explicitly specified
        if (node.title) {
            const titles = Array.isArray(node.title) ? node.title : [node.title];
            for (const t of titles) {
                if (!t.left && !t.right) t.left = 'center';
                if (!t.textStyle) t.textStyle = {};
                if (!t.textStyle.fontSize) t.textStyle.fontSize = isMobile ? 9 : 11;
                if (!t.textStyle.fontWeight) t.textStyle.fontWeight = 500;
            }
        }

        // Standardize Legends
        if (node.legend) {
            const legends = Array.isArray(node.legend) ? node.legend : [node.legend];
            for (const leg of legends) {
                if (leg.bottom === undefined) leg.bottom = 0;
                if (!leg.left && !leg.right) leg.left = 'center';
                if (!leg.orient) leg.orient = 'horizontal';
                if (!leg.type && isMobile) leg.type = 'scroll';
                if (!leg.textStyle) leg.textStyle = {};
                if (!leg.textStyle.fontSize) leg.textStyle.fontSize = isMobile ? 8 : 10;
            }
        }

        // tooltip.valueFormatter must be a function
        if (node.tooltip && typeof node.tooltip === 'object') {
            if (typeof node.tooltip.valueFormatter === 'string') {
                const fn = __lifCoerceDollarValueFormatterString(node.tooltip.valueFormatter);
                node.tooltip.valueFormatter = fn || ((v) => String(v));
            }
            if (isMobile && node.tooltip.trigger === 'axis') {
                node.tooltip.confine = true;
            }
        }

        // axisLabel and grid adjustments
        for (const axisKey of ['xAxis', 'yAxis']) {
            const axis = node[axisKey];
            const axes = Array.isArray(axis) ? axis : (axis ? [axis] : []);
            for (const ax of axes) {
                const name = ax.name || '';
                if (name.includes('$') || name.toLowerCase().includes('usd')) {
                    if (!ax.axisLabel) ax.axisLabel = { show: true };
                    if (!ax.axisLabel.formatter) ax.axisLabel.formatter = '{value}';
                }

                if (ax.axisLabel && typeof ax.axisLabel === 'object') {
                    if (typeof ax.axisLabel.formatter === 'string') {
                        const fn = __lifCoerceDollarValueFormatterString(ax.axisLabel.formatter);
                        if (fn) ax.axisLabel.formatter = fn;
                    }

                    // Enforce mobile font sizing
                    ax.axisLabel.fontSize = isMobile ? 7 : 10;
                    ax.axisLabel.fontWeight = 400; // No bold

                    if (ax.axisLabel.overflow === 'breakAll') {
                        ax.axisLabel.overflow = 'break';
                    }

                    const data = Array.isArray(ax.data) ? ax.data : [];
                    const hasSlashLabels = data.some(v => typeof v === 'string' && v.includes(' / '));
                    if (hasSlashLabels) {
                        const w = Number(ax.axisLabel.width || 0);
                        if (!Number.isFinite(w) || w < 170) ax.axisLabel.width = isMobile ? 120 : 180;
                        if (typeof ax.axisLabel.lineHeight !== 'number') ax.axisLabel.lineHeight = isMobile ? 11 : 14;
                    }
                }
            }
        }

        // Series refinements
        if (Array.isArray(node.series)) {
            for (const s of node.series) {
                if (!s || typeof s !== 'object') continue;

                // Hide labels globally, rely on tooltips
                if (!s.label) s.label = {};
                s.label.show = false;

                // Normalize line weights
                if (s.type === 'line') {
                    if (!s.lineStyle) s.lineStyle = {};
                    s.lineStyle.width = 2; // Normal, not bold
                }

                // Map Authority Colors
                if (s.name && AUTHORITY_COLORS[s.name]) {
                    if (!s.itemStyle) s.itemStyle = {};
                    s.itemStyle.color = AUTHORITY_COLORS[s.name];
                }

                // Data point mapping (for pie/custom series)
                if (Array.isArray(s.data)) {
                    for (const d of s.data) {
                        if (d && d.name && AUTHORITY_COLORS[d.name]) {
                            if (!d.itemStyle) d.itemStyle = {};
                            d.itemStyle.color = AUTHORITY_COLORS[d.name];
                        }
                    }
                }

                // Cleanup legacy colors
                if (s.itemStyle && typeof s.itemStyle.color === 'string') {
                    if (LEGACY_PALETTE.has(s.itemStyle.color)) delete s.itemStyle.color;
                }
                if (s.lineStyle && typeof s.lineStyle.color === 'string') {
                    if (LEGACY_PALETTE.has(s.lineStyle.color)) delete s.lineStyle.color;
                }
            }
        }

        for (const v of Object.values(node)) {
            if (Array.isArray(v)) {
                v.forEach(fixup);
            } else if (v && typeof v === 'object') {
                if (v !== node) fixup(v);
            }
        }
    };

    fixup(option);

    // Dynamic grid based on device
    if (!option.grid || typeof option.grid !== 'object' || Array.isArray(option.grid)) {
        option.grid = {
            left: isMobile ? 45 : 65,
            right: 25,
            top: 60,
            bottom: isMobile ? 65 : 55,
            containLabel: true
        };
    } else {
        if (isMobile) {
            option.grid.left = Math.max(Number(option.grid.left || 0), 45);
            option.grid.bottom = Math.max(Number(option.grid.bottom || 0), 65);
        } else {
            option.grid.left = Math.max(Number(option.grid.left || 0), 65);
            option.grid.bottom = Math.max(Number(option.grid.bottom || 0), 55);
        }
    }

    return option;
}

function __lifIsLandingStickyChartDom(chartEl) {
    if (!chartEl) return false;
    if (chartEl.id !== 'interactiveChart') return false;
    return document.body && document.body.classList.contains('page-home');
}

function __lifEstimateTextWidthPx(text, fontSizePx = 12) {
    // Rough estimate to avoid canvas measurement overhead.
    // Wide characters and slashes tend to need more room than simple letters.
    const s = String(text || '');
    // Many of our labels include separators like " / ", which wrap nicely.
    // Estimate using the longest segment so we don't massively inflate left padding.
    const parts = s.split(/\s*\/\s*/g);
    const longest = parts.reduce((m, p) => Math.max(m, String(p || '').length), 0);
    const base = s.length * (fontSizePx * 0.55);
    const segmentBase = longest * (fontSizePx * 0.55);
    const extra = (s.match(/[\/\-]/g) || []).length * (fontSizePx * 0.15);
    return Math.max(base, segmentBase) + extra;
}

function autoFitYAxisLabels(option) {
    if (!option || typeof option !== 'object') return option;

    // Normalize yAxis into an array for easier processing.
    const yAxes = Array.isArray(option.yAxis) ? option.yAxis : (option.yAxis ? [option.yAxis] : []);
    if (yAxes.length === 0) return option;

    // Fit both category labels (wide text) and value labels (currency signs).
    let maxWidth = 0;
    let needsValueAxisPadding = false;
    for (const yAxis of yAxes) {
        if (!yAxis) continue;
        const axisLabel = yAxis.axisLabel || {};
        const fontSize = Number(axisLabel.fontSize || 12);

        if (yAxis.type === 'category') {
            const labels = Array.isArray(yAxis.data) ? yAxis.data : [];
            const widthOverride = Number(axisLabel.width || 0);
            for (const lbl of labels) {
                maxWidth = Math.max(maxWidth, __lifEstimateTextWidthPx(lbl, fontSize));
            }
            if (widthOverride > 0) {
                maxWidth = Math.max(maxWidth, widthOverride);
            }
        } else {
            // If a value axis formatter likely includes currency, ensure we don't clip the '$'.
            const fmt = axisLabel.formatter;
            if (typeof fmt === 'string' && fmt.includes('$')) needsValueAxisPadding = true;
            if (typeof fmt === 'function') needsValueAxisPadding = true;
            if (typeof yAxis.name === 'string' && yAxis.name.includes('$')) needsValueAxisPadding = true;
        }
    }

    if (maxWidth <= 0 && !needsValueAxisPadding) return option;

    const categoryDesiredLeft = maxWidth > 0 ? Math.min(Math.max(Math.ceil(maxWidth) + 20, 72), 180) : 0;
    const desiredLeft = Math.max(categoryDesiredLeft, needsValueAxisPadding ? 84 : 0);
    if (!option.grid || typeof option.grid !== 'object' || Array.isArray(option.grid)) {
        option.grid = { left: desiredLeft, right: 20, top: 36, bottom: 28, containLabel: true };
        return option;
    }

    const currentLeft = Number(option.grid.left || 0);
    if (!Number.isFinite(currentLeft) || currentLeft < desiredLeft) {
        option.grid.left = desiredLeft;
    }
    if (option.grid.containLabel !== true) {
        option.grid.containLabel = true;
    }
    return option;
}

function applyLandingChartOverrides(option, chartEl) {
    if (!__lifIsLandingStickyChartDom(chartEl)) return option;
    if (!option || typeof option !== 'object') return option;

    // Landing page uses a caption under the chart. Avoid a second title inside the chart.
    if (option.title) {
        if (Array.isArray(option.title)) {
            option.title = option.title.map(t => ({ ...t, show: false }));
        } else if (typeof option.title === 'object') {
            option.title = { ...option.title, show: false };
        }
    }

    return option;
}

async function loadLifData(rootPrefix) {
    if (__lifDataCache) return __lifDataCache;

    const [exploitsPayload, interventionsPayload] = await Promise.all([
        loadJson(`${rootPrefix}data/exploits.json`),
        loadJson(`${rootPrefix}data/interventions.json`),
    ]);

    __lifDataCache = {
        exploits: unwrapEnvelope(exploitsPayload) || [],
        interventions: unwrapEnvelope(interventionsPayload) || [],
    };

    return __lifDataCache;
}

async function loadSeries(rootPrefix, name) {
    const payload = await loadJson(`${rootPrefix}data/series/${name}.json`);
    if (payload && payload.series) return payload.series;
    return payload;
}

async function loadChartSpec(rootPrefix, chartId) {
    const payload = await loadJsonOptional(`${rootPrefix}data/charts/${chartId}.json`);
    if (!payload) return null;
    if (payload && payload.chart) return payload.chart;
    if (payload && payload.payload) return payload.payload;
    return payload;
}

function formatUsdShort(v) {
    if (v === null || v === undefined || Number.isNaN(v)) return '—';
    const n = Number(v);
    if (n >= 1e12) return `$${(n / 1e12).toFixed(2)}T`;
    if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
    if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`;
    if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`;
    return `$${n.toFixed(0)}`;
}

function createLifEchartsTheme() {
    return {
        // Keep palette tight for a consistent site look.
        color: [
            LIF_COLORS.blue,
            LIF_COLORS.slate,
            LIF_COLORS.green,
            LIF_COLORS.amber,
            LIF_COLORS.red,
            LIF_COLORS.purple
        ],
        textStyle: {
            fontFamily: 'Newsreader, Georgia, serif',
            color: '#1a1a1a',
        },
        title: {
            left: 'center',
            textStyle: {
                fontWeight: 500,
                fontSize: 15,
            },
        },
        grid: {
            left: 65,
            right: 25,
            top: 60,
            bottom: 55,
            containLabel: true,
        },
        legend: {
            left: 'center',
            bottom: 0,
            textStyle: {
                fontSize: 11,
                fontWeight: 400
            }
        },
        tooltip: {
            backgroundColor: 'rgba(255,255,255,0.96)',
            borderColor: '#e5e5e5',
            borderWidth: 1,
            textStyle: {
                color: '#1a1a1a',
            },
        },
        axisPointer: {
            lineStyle: {
                color: '#9CA3AF',
            },
        },
    };
}

function buildChartRegistry() {
    return {
        async chart01_annual_losses(ctx) {
            const series = await loadSeries(ctx.rootPrefix, 'yearly_totals');
            const yearly = series.yearly_loss_usd || {};
            const years = Object.keys(yearly).sort();
            const values = years.map(y => yearly[y]);

            return {
                title: { text: 'Annual Exploit Losses' },
                xAxis: { type: 'category', data: years },
                yAxis: {
                    type: 'value',
                    axisLabel: { formatter: v => formatUsdShort(v) },
                    splitLine: { lineStyle: { color: '#f0f0f0' } },
                },
                tooltip: {
                    trigger: 'axis',
                    valueFormatter: v => formatUsdShort(v),
                },
                series: [
                    {
                        type: 'bar',
                        data: values,
                        itemStyle: { opacity: 0.85 },
                    },
                    {
                        type: 'line',
                        data: values,
                        smooth: true,
                        symbol: 'circle',
                        symbolSize: 6,
                        lineStyle: { width: 3 },
                    },
                ],
                dataZoom: [
                    { type: 'inside' },
                    { type: 'slider', height: 18, bottom: 12 },
                ],
            };
        },

        async chart02_cumulative_losses(ctx) {
            const series = await loadSeries(ctx.rootPrefix, 'cumulative_totals');
            const cumulative = series.cumulative_loss_usd || {};
            const years = Object.keys(cumulative).sort();
            const values = years.map(y => cumulative[y]);

            return {
                title: { text: 'Cumulative Exploit Losses' },
                xAxis: { type: 'category', data: years },
                yAxis: {
                    type: 'value',
                    axisLabel: { formatter: v => formatUsdShort(v) },
                    splitLine: { lineStyle: { color: '#f0f0f0' } },
                },
                tooltip: {
                    trigger: 'axis',
                    valueFormatter: v => formatUsdShort(v),
                },
                series: [
                    {
                        type: 'line',
                        data: values,
                        smooth: true,
                        areaStyle: { opacity: 0.12 },
                        symbol: 'none',
                        lineStyle: { width: 3 },
                    },
                ],
                dataZoom: [
                    { type: 'inside' },
                    { type: 'slider', height: 18, bottom: 12 },
                ],
            };
        },

        async chart08_four_layer_timeline(ctx) {
            const series = await loadSeries(ctx.rootPrefix, 'four_layer_yearly_losses');
            const years = (series.years || []).map(y => String(y));
            const layers = series.layers || {};

            const intervened = layers.intervened_loss_usd || [];
            const eligibleNotIntervened = layers.eligible_not_intervened_loss_usd || [];
            const otherNonAddressable = layers.other_non_addressable_loss_usd || [];
            const systemic = layers.systemic_loss_usd || [];

            return {
                title: { text: 'Annual DeFi Losses by Category (Four-Layer)' },
                legend: { top: 28 },
                xAxis: { type: 'category', data: years },
                yAxis: {
                    type: 'value',
                    axisLabel: { formatter: v => formatUsdShort(v) },
                    splitLine: { lineStyle: { color: '#f0f0f0' } },
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: { type: 'shadow' },
                    valueFormatter: v => formatUsdShort(v),
                },
                series: [
                    {
                        name: 'Actually Intervened',
                        type: 'bar',
                        stack: 'total',
                        data: intervened,
                    },
                    {
                        name: 'Eligible (Not Intervened)',
                        type: 'bar',
                        stack: 'total',
                        data: eligibleNotIntervened,
                    },
                    {
                        name: 'Other Non-Addressable',
                        type: 'bar',
                        stack: 'total',
                        data: otherNonAddressable,
                    },
                    {
                        name: 'Systemic Failures',
                        type: 'bar',
                        stack: 'total',
                        data: systemic,
                    },
                ],
                dataZoom: [
                    { type: 'inside' },
                    { type: 'slider', height: 18, bottom: 12 },
                ],
            };
        },

        async chart09_vector_distribution(ctx) {
            const series = await loadSeries(ctx.rootPrefix, 'vector_distribution');
            const counts = series.vector_count || {};

            const rows = Object.entries(counts)
                .map(([k, v]) => ({ k, v }))
                .sort((a, b) => b.v - a.v)
                .slice(0, 12);

            const labels = rows.map(r => r.k);
            const values = rows.map(r => r.v);

            return {
                title: { text: 'Top Attack Vectors (Frequency)' },
                grid: {
                    left: 140,
                    right: 24,
                    top: 56,
                    bottom: 24,
                    containLabel: true,
                },
                xAxis: { type: 'value' },
                yAxis: {
                    type: 'category',
                    data: labels,
                    inverse: true,
                    axisLabel: {
                        width: 140,
                        overflow: 'breakAll',
                        interval: 0
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: { type: 'shadow' },
                },
                series: [
                    {
                        type: 'bar',
                        data: values,
                        itemStyle: { opacity: 0.9 },
                    },
                ],
            };
        },
    };
}

/* Stagger multiple resize ticks after a chart is rendered.
 * Mobile layout engines sometimes need a few frames to settle container
 * dimensions (especially within flex stacks). Firing at 0-50-150-400 ms
 * catches both immediate and deferred layout completion. */
function __lifForceResizeSequence(inst, chartEl) {
    const doResize = () => {
        if (!inst || inst.isDisposed()) return;
        inst.resize();
    };
    requestAnimationFrame(doResize);
    setTimeout(doResize, 50);
    setTimeout(doResize, 150);
    setTimeout(doResize, 400);

    // ResizeObserver for ongoing container changes (e.g. dock open/close)
    if (typeof ResizeObserver !== 'undefined' && chartEl && !chartEl.__lifResizeObserverAttached) {
        chartEl.__lifResizeObserverAttached = true;
        new ResizeObserver(doResize).observe(chartEl);
    }
    // Lazy-attach a single window resize listener per instance
    if (!chartEl.__lifWindowResizeAttached) {
        chartEl.__lifWindowResizeAttached = true;
        window.addEventListener('resize', doResize);
    }
}

async function setActiveInteractiveChart({ rootPrefix, chartId, chartEl, fallbackImgEl, fallbackSrc }) {
    if (!chartEl) {
        console.error('chartEl is null');
        return;
    }

    console.log('Loading chart:', chartId, 'rootPrefix:', rootPrefix);

    const frame = chartEl.closest('.narrative-chart-frame, .narrative-inline-chart-frame');

    if (fallbackImgEl && fallbackSrc) fallbackImgEl.src = fallbackSrc;
    if (frame) frame.classList.add('is-fallback');

    const themeName = 'lif';
    echarts.registerTheme(themeName, createLifEchartsTheme());

    const inst = echarts.getInstanceByDom(chartEl) || echarts.init(chartEl, themeName, { renderer: 'canvas' });

    try {
        const spec = await loadChartSpec(rootPrefix, chartId);
        console.log('Loaded spec:', chartId, spec);
        const option = (spec && spec.option) ? spec.option : spec;
        if (option && typeof option === 'object' && Object.keys(option).length > 0) {
            console.log('Using JSON spec option for:', chartId);
            if (frame) frame.classList.remove('is-fallback');
            // Force a synchronous reflow so the container gets its real dimensions
            void chartEl.offsetHeight;
            const base = sanitizeEchartsOption(option);
            const fitted = autoFitYAxisLabels(base);
            const finalOption = applyLandingChartOverrides(fitted, chartEl);
            inst.setOption(finalOption, { notMerge: true });
            // Multi-tick resize to handle mobile layout settling
            __lifForceResizeSequence(inst, chartEl);
            return;
        }
        console.log('JSON spec has no valid option, falling through to registry');
    } catch (e) {
        console.error('Failed to load chart spec:', chartId, e);
        // fall through to built-in registry
    }

    console.log('Trying built-in registry for:', chartId);
    const registry = buildChartRegistry();
    const fn = registry[chartId];

    if (!fn) {
        console.error('No registry function for:', chartId);
        return;
    }

    if (frame) frame.classList.remove('is-fallback');
    void chartEl.offsetHeight;

    try {
        const option = await fn({ rootPrefix });
        console.log('Registry returned option for:', chartId);
        const fitted = autoFitYAxisLabels(option);
        const finalOption = applyLandingChartOverrides(fitted, chartEl);
        inst.setOption(finalOption, { notMerge: true });
        if (frame) frame.classList.remove('is-fallback');
        console.log('Chart rendered successfully:', chartId);
    } catch (e) {
        console.error('Registry function failed:', chartId, e);
        if (frame) frame.classList.add('is-fallback');
        return;
    }

    __lifForceResizeSequence(inst, chartEl);
}
