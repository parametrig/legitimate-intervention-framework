document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('[data-narrative-section]');
    const scrollSections = document.querySelectorAll('.scroll-section');
    const scrollMarker = document.getElementById('scrollMarker');
    const scrollProgress = document.getElementById('scrollProgress');
    const scrollIndicator = document.getElementById('scrollIndicator');

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

    function updateMarker(targetSectionIndex) {
        if (targetSectionIndex >= 0 && scrollSections[targetSectionIndex]) {
            const activeItem = scrollSections[targetSectionIndex];
            const topPos = activeItem.offsetTop + (activeItem.offsetHeight / 2) - 6;
            if (scrollMarker) scrollMarker.style.top = `${topPos}px`;
        }
    }

    async function activateSection(entryTarget) {
        const id = entryTarget.getAttribute('data-id') || entryTarget.id;
        const chartId = entryTarget.getAttribute('data-chart');
        const fallbackSrc = entryTarget.getAttribute('data-fallback-src');

        const inlineChartEl = entryTarget.querySelector('[data-inline-chart]');
        const inlineFallbackImg = entryTarget.querySelector('.narrative-inline-chart-fallback img');

        sections.forEach(s => s.classList.remove('active'));
        entryTarget.classList.add('active');

        scrollSections.forEach((s, index) => {
            s.classList.remove('active');
            if (s.getAttribute('data-target') === id) {
                s.classList.add('active');
                updateMarker(index);
            }
        });

        if (chartCaptionLink && chartId) {
            const chartAnchor = entryTarget.getAttribute('data-chart-anchor');
            const prettyTitleById = {
                chart02_cumulative_losses: 'Cumulative Exploit Losses',
                chart01_annual_losses: 'Annual Exploit Losses',
                chart08_four_layer_timeline: 'Annual DeFi Losses by Category',
                chart09_vector_distribution: 'Top Attack Vectors (Frequency)',
            };

            const pretty = prettyTitleById[chartId] || chartId;
            chartCaptionLink.textContent = pretty;

            if (chartAnchor) {
                chartCaptionLink.href = `research/all/?chart=${encodeURIComponent(chartAnchor)}`;
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
    }

    const isMobile = window.innerWidth <= 768;
    const observerOptions = {
        root: null,
        // On mobile the fixed bottom chart dock reduces the usable viewport height.
        // If we keep the same margins, sections may never become "intersecting".
        rootMargin: isMobile ? '-25% 0px -60% 0px' : '-40% 0px -40% 0px',
        threshold: 0,
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                activateSection(entry.target);
            }
        });
    }, observerOptions);

    sections.forEach(section => observer.observe(section));

    if (sections[0]) {
        activateSection(sections[0]);
    }

    scrollSections.forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.getAttribute('data-target');
            const targetSection = document.querySelector(`[data-id="${targetId}"]`);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });

    const header = document.querySelector('header');
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = Math.min(Math.round((scrollTop / docHeight) * 100), 100);
        if (scrollProgress) scrollProgress.textContent = scrollPercent + '%';

        if (header) {
            if (scrollTop > lastScrollY && scrollTop > 100) {
                header.classList.add('nav-hidden');
                document.body.classList.add('navbar-hidden');
            } else {
                header.classList.remove('nav-hidden');
                document.body.classList.remove('navbar-hidden');
            }
        }

        lastScrollY = scrollTop <= 0 ? 0 : scrollTop;
    });

    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            if (window.innerWidth <= 1024) {
                scrollIndicator.classList.toggle('active');
            }
        });
    }

    setTimeout(() => updateMarker(0), 100);

    const urlParams = new URLSearchParams(window.location.search);
    const chartParam = urlParams.get('chart');
    if (chartParam) {
        const target = document.querySelector(`[data-chart-anchor="${chartParam}"]`) || document.querySelector(`#${chartParam}`);
        if (target) {
            const y = target.getBoundingClientRect().top + window.scrollY - 90;
            window.scrollTo({ top: Math.max(y, 0), behavior: 'smooth' });
            activateSection(target);
        }
    }
});
