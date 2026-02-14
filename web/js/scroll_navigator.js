/**
 * scroll_navigator.js
 * Generic scroll indication and section highlighting.
 * Handles:
 * - Vertical indicator dot/bar movement.
 * - Intersection Observer for active section detection.
 * - Smooth scroll on dot click.
 * - Header show/hide on scroll.
 */

document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('[data-narrative-section]');
    const scrollIndicator = document.getElementById('scrollIndicator');
    const scrollSections = document.querySelectorAll('.scroll-section');
    const scrollMarker = document.getElementById('scrollMarker');
    const scrollProgress = document.getElementById('scrollProgress');
    const header = document.querySelector('header');

    if (!sections.length || !scrollIndicator) return;

    let lastScrollY = window.scrollY;

    // --- MARKER UPDATE ---
    function updateMarker(targetSectionIndex) {
        if (targetSectionIndex >= 0 && scrollSections[targetSectionIndex]) {
            const activeItem = scrollSections[targetSectionIndex];
            const topPos = activeItem.offsetTop + (activeItem.offsetHeight / 2) - 6;
            if (scrollMarker) scrollMarker.style.top = `${topPos}px`;
        }
    }

    // --- SECTION ACTIVATION ---
    function activateSection(entryTarget) {
        const id = entryTarget.getAttribute('data-id') || entryTarget.id;

        sections.forEach(s => s.classList.remove('active'));
        entryTarget.classList.add('active');

        scrollSections.forEach((s, index) => {
            s.classList.remove('active');
            if (s.getAttribute('data-target') === id) {
                s.classList.add('active');
                updateMarker(index);
            }
        });

        // Trigger custom event for other scripts (like chart loaders)
        const event = new CustomEvent('lifSectionActivated', {
            detail: {
                id,
                element: entryTarget,
                chartId: entryTarget.getAttribute('data-chart'),
                fallbackSrc: entryTarget.getAttribute('data-fallback-src')
            }
        });
        window.dispatchEvent(event);
    }

    // --- INTERSECTION OBSERVER ---
    const isMobile = window.innerWidth <= 768;
    const observerOptions = {
        root: null,
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

    // Initialize first section
    if (sections[0]) activateSection(sections[0]);

    // --- CLICK TO SCROLL ---
    scrollSections.forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.getAttribute('data-target');
            const targetSection = document.querySelector(`[data-id="${targetId}"]`) || document.getElementById(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
                // If it's a mobile toggle navigator, close it
                if (window.innerWidth <= 1024) {
                    scrollIndicator.classList.remove('active');
                }
            }
        });
    });

    // --- WINDOW SCROLL EVENTS ---
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;

        // Progress percentage
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = Math.min(Math.round((scrollTop / docHeight) * 100), 100);
        if (scrollProgress) scrollProgress.textContent = scrollPercent + '%';

        // Header Hide/Show
        if (header) {
            if (scrollTop > lastScrollY && scrollTop > 100) {
                header.classList.add('nav-hidden');
            } else {
                header.classList.remove('nav-hidden');
            }
        }

        lastScrollY = scrollTop <= 0 ? 0 : scrollTop;
    }, { passive: true });

    // --- MOBILE TOGGLE ---
    scrollIndicator.addEventListener('click', (e) => {
        // Only toggle if clicking on the indicator background, not on navigation links or their children
        if (window.innerWidth <= 1024 && 
            e.target === scrollIndicator && 
            !e.target.closest('.nav-icon-link') &&
            !e.target.closest('.nav-links')) {
            scrollIndicator.classList.toggle('active');
        }
    });

    // Handle initial marker position
    setTimeout(() => updateMarker(0), 100);
});
