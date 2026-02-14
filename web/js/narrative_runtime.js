document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('[data-narrative-section]');
    const chartEl = document.getElementById('interactiveChart');
    const fallbackImg = document.getElementById('interactiveChartFallbackImg');
    const dockCloseBtn = document.getElementById('chartDockClose');
    const dockReopenBtn = document.getElementById('chartDockReopen');
    const chartCaptionLink = document.getElementById('chartCaptionLink');

    const rootPrefix = document.body.getAttribute('data-root-prefix') || '';

    function setDockClosed(closed) {
        if (closed) {
            document.body.classList.add('dock-closed');
        } else {
            document.body.classList.remove('dock-closed');
        }
    }

    if (dockCloseBtn) {
        dockCloseBtn.addEventListener('click', (e) => {
            e.preventDefault();
            setDockClosed(true);
        });
    }

    if (dockReopenBtn) {
        dockReopenBtn.addEventListener('click', (e) => {
            e.preventDefault();
            setDockClosed(false);
        });
    }

    // Listen for section activation from scroll_navigator.js
    window.addEventListener('lifSectionActivated', async (e) => {
        const { id, element, chartId, fallbackSrc } = e.detail;

        const inlineChartEl = element.querySelector('[data-inline-chart]');
        const inlineFallbackImg = element.querySelector('.narrative-inline-chart-fallback img');

        if (chartCaptionLink && chartId) {
            const chartAnchor = element.getAttribute('data-chart-anchor');
            const prettyTitleById = {
                chart02_cumulative_losses: 'Cumulative Exploit Losses',
                chart01_annual_losses: 'Annual Exploit Losses',
                chart08_four_layer_timeline: 'Annual DeFi Losses by Category',
                chart09_vector_distribution: 'Top Attack Vectors (Frequency)',
                chart21_authority_performance: 'Authority Performance Comparison',
                chart38_success_vs_time: 'Success vs. Response Time',
                chart28_matrix_heatmap_combined: 'Scope × Authority Matrix',
                chart50_loss_prevented_vs_incurred: 'Value Saved vs. Incurred',
            };

            const pretty = prettyTitleById[chartId] || chartId;
            chartCaptionLink.textContent = pretty;

            if (chartAnchor) {
                chartCaptionLink.href = `${rootPrefix}research/all/?chart=${encodeURIComponent(chartAnchor)}`;
            }
        }

        if (chartId) {
            await setActiveInteractiveChart({
                rootPrefix,
                chartId,
                chartEl: inlineChartEl || chartEl,
                fallbackImgEl: inlineFallbackImg || fallbackImg,
                fallbackSrc,
            });
        }
    });

    // Handle deep-linking via URL param
    const urlParams = new URLSearchParams(window.location.search);
    const chartParam = urlParams.get('chart');
    if (chartParam) {
        const target = document.querySelector(`[data-chart-anchor="${chartParam}"]`) || document.querySelector(`#${chartParam}`);
        if (target) {
            setTimeout(() => {
                const y = target.getBoundingClientRect().top + window.scrollY - 90;
                window.scrollTo({ top: Math.max(y, 0), behavior: 'smooth' });
            }, 100);
        }
    }
});
