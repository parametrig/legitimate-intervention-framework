document.addEventListener('DOMContentLoaded', () => {

    // Selectors
    // Selectors
    const sections = document.querySelectorAll('.narrative-section, .research-section, .report-section, .report-hero');
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
                const id = entry.target.getAttribute('data-id') || entry.target.id;
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

    // Smart Navbar Logic
    const header = document.querySelector('header');
    let lastScrollY = window.scrollY;

    const scrollIndicator = document.getElementById('scrollIndicator');
    const stickyControls = document.querySelector('.sticky-controls');
    let scrollTimeout;
    let stickyTimeout;

    // Scroll Progress & Smart Navbar
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;

        // 1. Scroll Progress
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = Math.min(Math.round((scrollTop / docHeight) * 100), 100);
        if (scrollProgress) {
            scrollProgress.textContent = scrollPercent + '%';
        }

        // 2. Smart Navbar Hide/Show
        if (header) {
            // If scrolling down and past the navbar height
            if (scrollTop > lastScrollY && scrollTop > 100) {
                header.classList.add('nav-hidden');
                document.body.classList.add('navbar-hidden');
            } else {
                // If scrolling up
                header.classList.remove('nav-hidden');
                document.body.classList.remove('navbar-hidden');
            }
        }

        // 3. Mobile Scroll Indicator Visibility (Handled by click now, so we don't auto-show on scroll)
        // Kept empty to preserve structure or we can remove this block entirely.
        // Logic moved to Click Handler below.

        // 4. Mobile Database Controls Visibility
        if (stickyControls && window.innerWidth <= 768) {
            stickyControls.classList.add('scrolling');
        }

        lastScrollY = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
    });

    // Mobile Edge Click Handler (Scroll Indicator)
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', (e) => {
            // Only toggle if we are on mobile/small screen
            if (window.innerWidth <= 1024) {
                scrollIndicator.classList.toggle('active');
            }
        });
    }

    // Focus Tracking for Database Controls
    if (stickyControls) {
        const inputs = stickyControls.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                stickyControls.classList.add('focused');
            });
            input.addEventListener('blur', () => {
                stickyControls.classList.remove('focused');
            });
            // Also keep visible during change/interaction
            input.addEventListener('change', () => {
                stickyControls.classList.add('scrolling');
            });
        });
    }

    // Initialize marker position on load
    setTimeout(() => updateMarker(0), 100);

    // Deep Link Search Logic (Database Page)
    const urlParams = new URLSearchParams(window.location.search);
    // Support both 'q' and 'search' params
    const searchQuery = urlParams.get('q') || urlParams.get('search');
    if (searchQuery && searchInput) {
        searchInput.value = searchQuery;
        // Trigger filter
        filterData(searchQuery);
    }

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

    const feedback = document.getElementById('copy-feedback');
    const showFeedback = () => {
        if (!feedback) return;
        feedback.getBoundingClientRect(); // Reflow
        feedback.style.opacity = '1';
        setTimeout(() => {
            feedback.style.opacity = '0';
        }, 2000);
    };

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(address).then(showFeedback).catch(err => {
            console.error('Failed to copy: ', err);
            // Fallback if needed
            fallbackCopyTextToClipboard(address, showFeedback);
        });
    } else {
        fallbackCopyTextToClipboard(address, showFeedback);
    }
}

function fallbackCopyTextToClipboard(text, callback) {
    const textArea = document.createElement("textarea");
    textArea.value = text;

    // Ensure it's not visible
    textArea.style.position = "fixed";
    textArea.style.left = "-9999px";
    textArea.style.top = "0";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful && callback) callback();
    } catch (err) {
        console.error('Fallback copy failed: ', err);
    }

    document.body.removeChild(textArea);
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

// ============================================
// DATABASE FUNCTIONALITY
// ============================================

let allInterventions = [];
let allExploits = [];
let currentView = 'interventions';
let currentSort = { column: 'date', direction: 'desc' };

// Format currency
function formatCurrency(value) {
    if (value === null || value === undefined) return '—';
    if (value >= 1e9) return '$' + (value / 1e9).toFixed(2) + 'B';
    if (value >= 1e6) return '$' + (value / 1e6).toFixed(1) + 'M';
    if (value >= 1e3) return '$' + (value / 1e3).toFixed(0) + 'K';
    return '$' + value.toFixed(0);
}

// Format date - show exact date
function formatDate(dateStr) {
    if (!dateStr) return '—';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

// Load JSON data
async function loadDatabaseData() {
    try {
        const [interventionsRes, exploitsRes] = await Promise.all([
            fetch('data/interventions.json'),
            fetch('data/exploits.json')
        ]);
        const interventionsPayload = await interventionsRes.json();
        const exploitsPayload = await exploitsRes.json();

        allInterventions = Array.isArray(interventionsPayload)
            ? interventionsPayload
            : (interventionsPayload.records || []);

        allExploits = Array.isArray(exploitsPayload)
            ? exploitsPayload
            : (exploitsPayload.records || []);
        return true;
    } catch (error) {
        console.error('Error loading database:', error);
        return false;
    }
}

// Calculate stats from data
function calculateStats(cases) {
    const count = cases.length;
    const dates = cases.map(c => c.date).filter(d => d);
    const years = dates.map(d => parseInt(d.substring(0, 4)));
    const minYear = Math.min(...years);
    const maxYear = Math.max(...years);
    const totalLoss = cases.reduce((sum, c) => sum + (c.loss_usd || 0), 0);
    const totalSaved = cases.reduce((sum, c) => sum + (c.loss_prevented_usd || 0), 0);

    return { count, minYear, maxYear, totalLoss, totalSaved };
}

// Update dynamic stats in header
function updateHeaderStats(stats) {
    const countEl = document.getElementById('caseCount');
    const yearEl = document.getElementById('yearRange');
    const savedEl = document.getElementById('savedAmount');

    if (countEl) countEl.textContent = stats.count;
    if (yearEl) yearEl.textContent = `${stats.minYear} and ${stats.maxYear}`;
    if (savedEl) savedEl.textContent = formatCurrency(stats.totalSaved);
}

// Update toggle counts
function updateToggleCounts() {
    const intCountEl = document.getElementById('interventionCount');
    const expCountEl = document.getElementById('exploitCount');

    if (intCountEl) intCountEl.textContent = allInterventions.length;
    if (expCountEl) expCountEl.textContent = allExploits.length;
}

// Populate year filter
function populateYearFilter() {
    const yearFilter = document.getElementById('filterYear');
    if (!yearFilter) return;

    const years = new Set();
    allInterventions.forEach(c => {
        if (c.date) years.add(c.date.substring(0, 4));
    });
    allExploits.forEach(c => {
        if (c.date) years.add(c.date.substring(0, 4));
    });

    const sortedYears = Array.from(years).sort().reverse();
    sortedYears.forEach(year => {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearFilter.appendChild(option);
    });
}

// Get current filters
function getFilters() {
    return {
        search: (document.getElementById('search')?.value || '').toLowerCase(),
        authority: document.getElementById('filterAuthority')?.value || '',
        scope: document.getElementById('filterScope')?.value || '',
        year: document.getElementById('filterYear')?.value || '',
        success: document.getElementById('filterSuccess')?.value || ''
    };
}

// Filter cases
function filterCases(cases) {
    const filters = getFilters();

    return cases.filter(c => {
        // Search filter
        if (filters.search) {
            const searchable = [
                c.protocol, c.chain, c.vector, c.description,
                c.intervention_notes, c.scope, c.authority
            ].join(' ').toLowerCase();
            if (!searchable.includes(filters.search)) return false;
        }

        // Authority filter
        if (filters.authority && c.authority !== filters.authority) return false;

        // Scope filter
        if (filters.scope && c.scope !== filters.scope) return false;

        // Year filter
        if (filters.year && (!c.date || !c.date.startsWith(filters.year))) return false;

        // Success filter
        if (filters.success) {
            const pct = c.success_pct;
            if (filters.success === 'high' && (pct === null || pct < 80)) return false;
            if (filters.success === 'medium' && (pct === null || pct < 20 || pct >= 80)) return false;
            if (filters.success === 'low' && (pct === null || pct >= 20)) return false;
        }

        return true;
    });
}


// Handle sort click
window.handleSort = function (column) {
    if (currentSort.column === column) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.direction = 'desc'; // Default to newest/highest
    }
    renderTable();
};

// Sort cases
function sortCases(cases) {
    const { column, direction } = currentSort;
    const mult = direction === 'asc' ? 1 : -1;

    return [...cases].sort((a, b) => {
        let valA = a[column];
        let valB = b[column];

        if (column === 'date') {
            valA = valA || '';
            valB = valB || '';
            return mult * valA.localeCompare(valB);
        }

        if (typeof valA === 'number' && typeof valB === 'number') {
            return mult * (valA - valB);
        }

        valA = String(valA || '');
        valB = String(valB || '');
        return mult * valA.localeCompare(valB);
    });
}

// Get authority tag class
function getAuthorityClass(authority) {
    if (!authority) return '';
    if (authority.includes('Signer')) return 'multisig';
    if (authority.includes('Delegated')) return 'council';
    if (authority.includes('Governance')) return 'gov';
    return '';
}

// Get vector label with fallback
function getVectorLabel(c) {
    if (c.vector && c.vector !== '—') return c.vector;

    // Fallbacks for empty vector
    if (c.scope === 'Asset') return 'Asset Freeze';
    if (c.scope === 'Account') return 'Account Freeze';
    if (c.scope === 'Protocol') return 'Protocol Pause';
    if (c.scope === 'Module') return 'Module Pause';

    return 'Intervention';
}

// Render table row
function renderRow(c, isIntervention = true) {
    const successClass = c.success_pct >= 80 ? 'success-high' :
        c.success_pct >= 20 ? 'success-medium' : 'success-low';

    return `
        <tr class="case-row" data-id="${c.id}" onclick="showCaseDetail('${c.id}')">
            <td style="white-space:nowrap;">${formatDate(c.date)}</td>
            <td>
                <strong>${c.protocol || '—'}</strong> ${c.has_rationale ? '<span class="rationale-badge" title="Detailed rationale available"><i data-lucide="file-text"></i></span>' : ''}
                <br><span class="chain-label">${c.chain || '—'}</span>
            </td>
            <td>
                <div class="loss-amount">-${formatCurrency(c.loss_usd)}</div>
                ${c.loss_prevented_usd ? `<div class="saved-amount">+${formatCurrency(c.loss_prevented_usd)} saved</div>` : ''}
                ${c.success_pct !== null ? `<div class="success-container"><div class="success-bar ${successClass}" style="width: ${c.success_pct}%"></div></div>` : ''}
            </td>
            <td>
                ${c.authority ? `<span class="tag ${getAuthorityClass(c.authority)}">${c.authority}</span>` : '—'}
                ${c.scope ? `<br><span class="scope-label">${c.scope}</span>` : ''}
            </td>
            <td>
                <span class="vector-label">${getVectorLabel(c)}</span>
                ${c.source_url ? `<a href="${c.source_url}" target="_blank" class="source-link" onclick="event.stopPropagation()">
                    <i data-lucide="external-link"></i>
                </a>` : ''}
            </td>
        </tr>
    `;
}

// Render table
function renderTable() {
    const tbody = document.getElementById('casesBody');
    const loading = document.getElementById('loadingState');
    const empty = document.getElementById('emptyState');
    const resultsCount = document.getElementById('resultsCount');
    const resultsTotals = document.getElementById('resultsTotals');

    if (!tbody) return;

    // Get data based on current view
    const data = currentView === 'interventions' ? allInterventions : allExploits;

    // Filter and sort
    const filtered = filterCases(data);
    const sorted = sortCases(filtered);

    // Hide loading
    if (loading) loading.style.display = 'none';

    // Show empty state or table
    if (sorted.length === 0) {
        tbody.innerHTML = '';
        if (empty) empty.style.display = 'flex';
        if (resultsCount) resultsCount.textContent = 'No results found';
        return;
    }

    if (empty) empty.style.display = 'none';

    // Render rows
    const isIntervention = currentView === 'interventions';
    tbody.innerHTML = sorted.map(c => renderRow(c, isIntervention)).join('');

    // Update results count
    const stats = calculateStats(sorted);
    if (resultsCount) {
        resultsCount.textContent = `Showing ${sorted.length} of ${data.length} cases`;
    }
    if (resultsTotals && isIntervention) {
        resultsTotals.innerHTML = `<span class="text-loss">-${formatCurrency(stats.totalLoss)} losses</span> <span class="text-saved">+${formatCurrency(stats.totalSaved)} saved</span>`;
    } else if (resultsTotals) {
        resultsTotals.innerHTML = `<span class="text-loss">${formatCurrency(stats.totalLoss)} total losses</span>`;
    }

    // Re-init icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Show case detail modal
function showCaseDetail(caseId) {
    const modal = document.getElementById('caseModal');
    if (!modal) return;

    // Find case
    let c = allInterventions.find(x => x.id === caseId);
    if (!c) c = allExploits.find(x => x.id === caseId);
    if (!c) return;

    const hasTimingData = c.time_to_detect_min !== null || c.time_to_contain_min !== null;
    const successRate = c.success_pct !== null ? `${c.success_pct}%` : '—';

    modal.innerHTML = `
        <div class="modal-content">
            <button class="modal-close" onclick="closeCaseModal()">&times;</button>
            <div class="modal-header">
                <h2>${c.protocol || 'Unknown Protocol'}</h2>
                <div class="modal-meta">
                    <span>${formatDate(c.date)}</span>
                    ${c.chain ? `<span class="modal-chain">${c.chain}</span>` : ''}
                    ${c.authority ? `<span class="tag ${getAuthorityClass(c.authority)}">${c.authority}</span>` : ''}
                </div>
            </div>
            
            <div class="modal-body">
                <div class="stat-grid">
                    <div class="stat-card loss">
                        <span class="stat-label">Loss</span>
                        <span class="stat-value">${formatCurrency(c.loss_usd)}</span>
                    </div>
                    <div class="stat-card saved">
                        <span class="stat-label">Saved</span>
                        <span class="stat-value">${formatCurrency(c.loss_prevented_usd)}</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-label">Success Rate</span>
                        <span class="stat-value">${successRate}</span>
                    </div>
                </div>

                <div class="detail-grid">
                    <div class="modal-section">
                        <h3>Classification</h3>
                        <div class="info-list">
                            <div class="info-item">
                                <span class="info-label">Vector</span>
                                <span class="info-value">${c.vector || '—'}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Scope</span>
                                <span class="info-value">${c.scope || '—'}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Authority</span>
                                <span class="info-value">${c.authority || '—'}</span>
                            </div>
                        </div>
                    </div>

                    <div class="modal-section">
                        <h3>Timing</h3>
                        <div class="info-list">
                            <div class="info-item">
                                <span class="info-label">Time to Detect</span>
                                <span class="info-value">${c.time_to_detect_min !== null ? c.time_to_detect_min + ' min' : '—'}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Time to Contain</span>
                                <span class="info-value">${c.time_to_contain_min !== null ? c.time_to_contain_min + ' min' : '—'}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="modal-section">
                    <h3>Incident Narrative</h3>
                    <div class="modal-narrative">
                        ${c.description || c.intervention_notes || 'No detailed description available for this case.'}
                    </div>
                </div>

                ${c.has_rationale && c.rationale ? `
                <div class="rationale-section">
                    <h3><i data-lucide="file-text"></i> Classification Rationale</h3>
                    <div class="rationale-content">
                        ${c.rationale}
                    </div>
                </div>
                ` : ''}
            </div>

            <div class="modal-footer">
                ${c.source_url ? `
                    <a href="${c.source_url}" target="_blank" class="source-link">
                        Source Document <i data-lucide="external-link"></i>
                    </a>
                ` : ''}
            </div>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Close case detail modal
function closeCaseModal() {
    const modal = document.getElementById('caseModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Clear all filters
function clearFilters() {
    document.getElementById('search').value = '';
    document.getElementById('filterAuthority').value = '';
    document.getElementById('filterScope').value = '';
    document.getElementById('filterYear').value = '';
    document.getElementById('filterSuccess').value = '';
    renderTable();
}

// Initialize database page
async function initDatabase() {
    const loading = document.getElementById('loadingState');

    // Load data
    const success = await loadDatabaseData();
    if (!success) {
        if (loading) loading.innerHTML = '<p>Error loading database. Please refresh.</p>';
        return;
    }

    // Check for deep link search
    const urlParams = new URLSearchParams(window.location.search);
    const searchTerm = urlParams.get('search');
    if (searchTerm) {
        const searchInput = document.getElementById('search');
        if (searchInput) searchInput.value = searchTerm;
    }

    // Calculate and display stats
    const stats = calculateStats(allInterventions);
    updateHeaderStats(stats);
    updateToggleCounts();
    populateYearFilter();

    // Render initial table
    renderTable();

    // Set up event listeners
    setupDatabaseListeners();
}

// Set up database event listeners
function setupDatabaseListeners() {
    // Search
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(renderTable, 200));
    }

    // Filters
    ['filterAuthority', 'filterScope', 'filterYear', 'filterSuccess'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', renderTable);
    });

    // View toggle
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentView = btn.dataset.view;
            renderTable();
        });
    });



    // Modal close on backdrop click
    const modal = document.getElementById('caseModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeCaseModal();
        });
    }

    // Escape key closes modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeCaseModal();
    });
}

// Debounce helper
function debounce(fn, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn.apply(this, args), delay);
    };
}

// Insight Toggle Logic for Research Page
function toggleInsight(btn) {
    const panel = btn.nextElementSibling;
    const icon = btn.querySelector('i');

    if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
        icon.style.transform = 'rotate(0deg)';
        btn.classList.remove('active');
    } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
        icon.style.transform = 'rotate(180deg)';
        btn.classList.add('active');
    }
}

// Initialize icons on all pages if Lucide is present
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
