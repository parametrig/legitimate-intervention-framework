let __lifDataCache = null;

async function loadJson(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`);
    return res.json();
}

function unwrapEnvelope(payload) {
    if (Array.isArray(payload)) return payload;
    if (payload && Array.isArray(payload.records)) return payload.records;
    return payload;
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
        color: ['#2563EB', '#16A34A', '#D97706', '#7C3AED', '#DC2626', '#64748B'],
        textStyle: {
            fontFamily: 'Newsreader, Georgia, serif',
            color: '#1a1a1a',
        },
        title: {
            textStyle: {
                fontWeight: 600,
                fontSize: 16,
            },
        },
        grid: {
            left: 48,
            right: 32,
            top: 56,
            bottom: 44,
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
                xAxis: { type: 'value' },
                yAxis: { type: 'category', data: labels, inverse: true },
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

async function setActiveInteractiveChart({ rootPrefix, chartId, chartEl, fallbackImgEl, fallbackSrc }) {
    if (!chartEl) return;

    const frame = chartEl.closest('.narrative-chart-frame');

    const registry = buildChartRegistry();
    const fn = registry[chartId];

    if (!fn) {
        if (frame) frame.classList.add('is-fallback');
        if (fallbackImgEl && fallbackSrc) fallbackImgEl.src = fallbackSrc;
        return;
    }

    if (frame) frame.classList.remove('is-fallback');

    const themeName = 'lif';
    if (!echarts.getTheme(themeName)) {
        echarts.registerTheme(themeName, createLifEchartsTheme());
    }

    const inst = echarts.getInstanceByDom(chartEl) || echarts.init(chartEl, themeName, { renderer: 'canvas' });

    const option = await fn({ rootPrefix });
    inst.setOption(option, { notMerge: true });

    window.addEventListener('resize', () => inst.resize());
}
