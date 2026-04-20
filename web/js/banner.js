document.addEventListener('DOMContentLoaded', () => {
    const campaignId = 'giveth-qf-2026-04-23';
    const dismissKey = `lif_banner_dismissed_${campaignId}`;
    const now = new Date();
    const windowStart = new Date('2026-04-20T00:00:00Z');
    const windowEnd = new Date('2026-05-14T23:59:59Z');
    const isInWindow = now >= windowStart && now <= windowEnd;
    const isManuallyEnabled = localStorage.getItem('lif_banner_enabled') === 'true';

    if (!isInWindow && !isManuallyEnabled) return;

    // Check if dismissed
    if (localStorage.getItem(dismissKey)) return;

    // Create banner
    const banner = document.createElement('div');
    banner.id = 'global-banner';
    banner.innerHTML = `
        <div class="banner-content">
            <span>
                LIF has been accepted into the Ethereum Security QF Round on Giveth. Donate April 23–May 14:
                <a class="banner-link" href="https://giveth.io/project/lif:-legitimate-intervention-framework" target="_blank" rel="noopener noreferrer">giveth.io/project/lif:-legitimate-intervention-framework</a>
            </span>
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
            localStorage.setItem(dismissKey, 'true');
        });
    }
});
