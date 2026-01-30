document.addEventListener('DOMContentLoaded', () => {

    // Selectors
    const sections = document.querySelectorAll('.narrative-section, .research-section');
    const scrollSections = document.querySelectorAll('.scroll-section');
    const charts = document.querySelectorAll('.chart-img');
    const scrollMarker = document.getElementById('scrollMarker');
    const scrollProgress = document.getElementById('scrollProgress');

    // Function to update marker position
    function updateMarker(targetSectionIndex) {
        if (targetSectionIndex >= 0 && scrollSections[targetSectionIndex]) {
            const activeItem = scrollSections[targetSectionIndex];
            // Calculate top position relative to parent container
            // adding roughly half height of item (offset) to center the arrow
            const topPos = activeItem.offsetTop + (activeItem.offsetHeight / 2) - 6;
            scrollMarker.style.top = `${topPos}px`;
        }
    }

    // Intersection Observer Options
    const observerOptions = {
        root: null,
        rootMargin: '-40% 0px -40% 0px',
        threshold: 0
    };

    // Observer Callback
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('data-id');
                const chartId = entry.target.getAttribute('data-chart');

                // 1. Highlight Narrative Text
                sections.forEach(s => s.classList.remove('active'));
                entry.target.classList.add('active');

                // 2. Update Scroll Indicator
                scrollSections.forEach((s, index) => {
                    s.classList.remove('active');
                    if (s.getAttribute('data-target') === id) {
                        s.classList.add('active');
                        updateMarker(index);
                    }
                });

                // 3. Swap Charts
                charts.forEach(c => {
                    c.classList.remove('active');
                    if (c.id === chartId) {
                        c.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);

    // Observe all narrative sections
    sections.forEach(section => {
        observer.observe(section);
    });

    // Click to Scroll
    scrollSections.forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.getAttribute('data-target');
            // Try to find target section by data-id
            const targetSection = document.querySelector(`[data-id="${targetId}"]`);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });

    // Scroll Progress
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = Math.min(Math.round((scrollTop / docHeight) * 100), 100);
        if (scrollProgress) {
            scrollProgress.textContent = scrollPercent + '%';
        }
    });

    // Initialize marker position on load
    setTimeout(() => updateMarker(0), 100);

    // Lightbox Logic
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    document.body.appendChild(lightbox);

    charts.forEach(chart => {
        chart.addEventListener('click', () => {
            // Only allow clicking the active chart to avoid confusion
            if (!chart.classList.contains('active')) return;

            lightbox.innerHTML = `<img src="${chart.src}" alt="${chart.alt}">`;
            lightbox.style.display = 'flex';
            // Slight delay to allow CSS transition to catch the display change
            requestAnimationFrame(() => {
                lightbox.classList.add('visible');
            });
        });
    });

    lightbox.addEventListener('click', () => {
        lightbox.classList.remove('visible');
        setTimeout(() => {
            lightbox.style.display = 'none';
            lightbox.innerHTML = '';
        }, 300);
    });

    // Initialize Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

// Global Helpers
function toggleSection(id) {
    const content = document.getElementById('content-' + id);
    const chevron = document.getElementById('chevron-' + id);
    if (!content || !chevron) return;

    content.classList.toggle('open');
    chevron.classList.toggle('open');
}

function copyAddress() {
    const address = '0x5A30de56F4d345b3ab5c3759463335BA3a3AB637';
    navigator.clipboard.writeText(address).then(() => {
        const feedback = document.getElementById('copy-feedback');
        if (!feedback) return;

        feedback.style.opacity = '1';
        setTimeout(() => {
            feedback.style.opacity = '0';
        }, 2000);
    });
}

function initSearch() {
    const searchInput = document.getElementById('search');
    const rows = document.querySelectorAll('.case-row');
    if (!searchInput || rows.length === 0) return;

    searchInput.addEventListener('keyup', (e) => {
        const term = e.target.value.toLowerCase();
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(term) ? '' : 'none';
        });
    });
}

// Call initSearch if elements exist
document.addEventListener('DOMContentLoaded', initSearch);
