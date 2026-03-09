document.addEventListener('DOMContentLoaded', () => {
    // Banner disabled by default. To enable for a future announcement, set:
    // localStorage.setItem('lif_banner_enabled', 'true')
    if (localStorage.getItem('lif_banner_enabled') !== 'true') return;

    // Check if dismissed
    if (localStorage.getItem('lif_banner_dismissed')) return;

    // Create banner
    const banner = document.createElement('div');
    banner.id = 'global-banner';
    banner.innerHTML = `
        <div class="banner-content">
            <span>This site is in final review. Corrections welcome.</span>
            <button id="banner-dismiss" aria-label="Dismiss">×</button>
        </div>
    `;

    // Prepend to body
    document.body.prepend(banner);

    // Handle dismiss
    const dismissBtn = document.getElementById('banner-dismiss');
    if (dismissBtn) {
        dismissBtn.addEventListener('click', () => {
            banner.style.opacity = '0';
            setTimeout(() => banner.remove(), 300);
            localStorage.setItem('lif_banner_dismissed', 'true');
        });
    }
});
