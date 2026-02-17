/**
 * audio_player.js
 * Persistent audio player with mini-dock.
 *
 * Features:
 *  - Saves playback position to sessionStorage so a page reload or
 *    navigation within the site resumes from the same timestamp.
 *  - Injects a floating mini-player dock at the bottom of the viewport
 *    with play/pause, rewind 15 s, forward 15 s, progress bar, time
 *    display, and a close button.
 *  - Works across all pages: each page includes this script and the
 *    audio path is resolved relative to the page via the constant below.
 *
 * Usage:
 *   Any element can trigger the player by calling:
 *     window.lifAudioPlayer.open()
 *
 *   The hero "listen" button on index.html does this via onclick.
 */

(function () {
    'use strict';

    const STORAGE_KEY = 'lif_audio_state';
    const SKIP_SECONDS = 15;

    /* -------------------------------------------------------
       Resolve audio path relative to the current page.
       The canonical path from site root is:
         audio/code_is_law_vs_kill_switch.m4a
       We figure out how many levels deep we are and prepend
       the right number of "../".
    ------------------------------------------------------- */
    function resolveAudioSrc() {
        const path = window.location.pathname;
        // Count directory depth under /web/ (which is site root)
        const segments = path.replace(/\/index\.html$/, '/').replace(/\/[^/]*\.html$/, '/').split('/').filter(Boolean);
        // For file:// or deployed, find how deep we are relative to site root
        // Simple heuristic: count segments after the last "web" segment
        const webIdx = segments.lastIndexOf('web');
        let depth = 0;
        if (webIdx >= 0) {
            depth = segments.length - webIdx - 1;
        } else {
            // Fallback: guess from typical URL patterns
            if (path.includes('/research/all/') || path.includes('/research/threat/') ||
                path.includes('/research/intervention/') || path.includes('/research/efficiency/') ||
                path.includes('/research/framework/')) {
                depth = 2;
            } else if (path.includes('/research/') || path.includes('/summary/')) {
                depth = 1;
            }
        }
        const prefix = depth > 0 ? '../'.repeat(depth) : '';
        return prefix + 'audio/code_is_law_vs_kill_switch.m4a';
    }

    /* -------------------------------------------------------
       State helpers
    ------------------------------------------------------- */
    function loadState() {
        try {
            const raw = sessionStorage.getItem(STORAGE_KEY);
            return raw ? JSON.parse(raw) : null;
        } catch { return null; }
    }

    function saveState(currentTime, playing) {
        try {
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
                currentTime: currentTime || 0,
                playing: !!playing,
                ts: Date.now()
            }));
        } catch { /* quota exceeded – ignore */ }
    }

    function clearState() {
        try { sessionStorage.removeItem(STORAGE_KEY); } catch { }
    }

    /* -------------------------------------------------------
       Format seconds → m:ss or h:mm:ss
    ------------------------------------------------------- */
    function fmt(s) {
        if (!isFinite(s)) return '0:00';
        s = Math.floor(s);
        const h = Math.floor(s / 3600);
        const m = Math.floor((s % 3600) / 60);
        const sec = s % 60;
        const ss = sec < 10 ? '0' + sec : sec;
        return h > 0 ? `${h}:${m < 10 ? '0' + m : m}:${ss}` : `${m}:${ss}`;
    }

    /* -------------------------------------------------------
       Build the mini-player dock (injected once into <body>)
    ------------------------------------------------------- */
    function createDock() {
        const dock = document.createElement('div');
        dock.id = 'lifAudioDock';
        dock.innerHTML = `
            <audio id="lifAudio" preload="auto">
                <source src="${resolveAudioSrc()}" type="audio/mp4">
            </audio>
            <div class="lif-audio-controls">
                <button class="lif-audio-btn" id="lifAudioRew" title="Rewind 15s" aria-label="Rewind 15 seconds">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 256 256" fill="currentColor">
                        <path d="M224,128a96,96,0,0,1-162.38,69.27,8,8,0,1,1,10.78-11.82A80,80,0,1,0,48,128a80.8,80.8,0,0,0,2.07,18.17L62,138.25a8,8,0,0,1,12,10.5l-24,27.43a8,8,0,0,1-12.05-.05l-24-27.43a8,8,0,1,1,12.06-10.5l13.7,15.65A96.15,96.15,0,0,1,32,128,96,96,0,0,1,224,128Z"/>
                    </svg>
                </button>
                <button class="lif-audio-btn lif-audio-play" id="lifAudioPlay" title="Play/Pause" aria-label="Play or pause">
                    <svg class="play-icon" xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 256 256" fill="currentColor">
                        <path d="M232.4,114.49,88.32,26.35a16,16,0,0,0-16.2-.3A15.86,15.86,0,0,0,64,39.87V216.13A15.94,15.94,0,0,0,80,232a16.16,16.16,0,0,0,8.36-2.35L232.4,141.51a15.81,15.81,0,0,0,0-27ZM80,215.94V40l143.83,88Z"/>
                    </svg>
                    <svg class="pause-icon" xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 256 256" fill="currentColor" style="display:none;">
                        <path d="M216,48V208a16,16,0,0,1-16,16H160a16,16,0,0,1-16-16V48a16,16,0,0,1,16-16h40A16,16,0,0,1,216,48ZM96,32H56A16,16,0,0,0,40,48V208a16,16,0,0,0,16,16H96a16,16,0,0,0,16-16V48A16,16,0,0,0,96,32Z"/>
                    </svg>
                </button>
                <button class="lif-audio-btn" id="lifAudioFwd" title="Forward 15s" aria-label="Forward 15 seconds">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 256 256" fill="currentColor">
                        <path d="M224,128a96,96,0,0,1-162.38,69.27,8,8,0,1,1,10.78-11.82A80,80,0,1,0,48,128a80.8,80.8,0,0,0,2.07,18.17L62,138.25a8,8,0,0,1,12,10.5l-24,27.43a8,8,0,0,1-12.05-.05l-24-27.43a8,8,0,1,1,12.06-10.5l13.7,15.65A96.15,96.15,0,0,1,32,128,96,96,0,0,1,224,128Z" transform="scale(-1,1) translate(-256,0)"/>
                    </svg>
                </button>
                <div class="lif-audio-progress-wrap" id="lifAudioProgressWrap">
                    <div class="lif-audio-progress-bar" id="lifAudioProgressBar"></div>
                </div>
                <span class="lif-audio-time" id="lifAudioTime">0:00 / 0:00</span>
                <button class="lif-audio-btn lif-audio-close" id="lifAudioClose" title="Close player" aria-label="Close player">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 256 256" fill="currentColor">
                        <path d="M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z"/>
                    </svg>
                </button>
            </div>
        `;
        document.body.appendChild(dock);
        return dock;
    }

    /* -------------------------------------------------------
       Player controller
    ------------------------------------------------------- */
    let dock, audio;
    let dockReady = false;
    let podcastBtn;

    function ensureDock() {
        if (dockReady) return;
        dock = createDock();
        audio = document.getElementById('lifAudio');

        // Find the podcast button on the page (the one that opens the player)
        podcastBtn = document.querySelector('.landing-action-btn[onclick*="lifAudioPlayer"]');

        const playBtn = document.getElementById('lifAudioPlay');
        const rewBtn = document.getElementById('lifAudioRew');
        const fwdBtn = document.getElementById('lifAudioFwd');
        const closeBtn = document.getElementById('lifAudioClose');
        const progWrap = document.getElementById('lifAudioProgressWrap');
        const progBar = document.getElementById('lifAudioProgressBar');
        const timeEl = document.getElementById('lifAudioTime');
        const playIcon = playBtn.querySelector('.play-icon');
        const pauseIcon = playBtn.querySelector('.pause-icon');

        function syncIcons() {
            if (audio.paused) {
                playIcon.style.display = '';
                pauseIcon.style.display = 'none';
                if (podcastBtn) podcastBtn.classList.remove('playing');
            } else {
                playIcon.style.display = 'none';
                pauseIcon.style.display = '';
                if (podcastBtn) podcastBtn.classList.add('playing');
            }
        }

        function updateProgress() {
            const pct = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
            progBar.style.width = pct + '%';
            timeEl.textContent = fmt(audio.currentTime) + ' / ' + fmt(audio.duration);
        }

        audio.addEventListener('timeupdate', () => {
            updateProgress();
            saveState(audio.currentTime, !audio.paused);
        });
        audio.addEventListener('play', syncIcons);
        audio.addEventListener('pause', syncIcons);
        audio.addEventListener('ended', () => {
            syncIcons();
            clearState();
            if (podcastBtn) podcastBtn.classList.remove('playing');
        });

        playBtn.addEventListener('click', () => {
            if (audio.paused) audio.play().catch(() => { });
            else audio.pause();
        });

        rewBtn.addEventListener('click', () => {
            audio.currentTime = Math.max(0, audio.currentTime - SKIP_SECONDS);
        });

        fwdBtn.addEventListener('click', () => {
            audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + SKIP_SECONDS);
        });

        progWrap.addEventListener('click', (e) => {
            const rect = progWrap.getBoundingClientRect();
            const pct = (e.clientX - rect.left) / rect.width;
            if (audio.duration) audio.currentTime = pct * audio.duration;
        });

        closeBtn.addEventListener('click', () => {
            audio.pause();
            dock.classList.remove('open');
            document.body.classList.remove('has-audio-dock');
            clearState();
            if (podcastBtn) podcastBtn.classList.remove('playing');
        });

        dockReady = true;
    }

    function openPlayer(resumeTime) {
        ensureDock();
        dock.classList.add('open');
        document.body.classList.add('has-audio-dock'); // Signal layout shift

        if (typeof resumeTime === 'number' && resumeTime > 0) {
            audio.currentTime = resumeTime;
        }
        audio.play().catch(() => { });
    }

    /* -------------------------------------------------------
       Auto-resume on page load (if state exists)
    ------------------------------------------------------- */
    function autoResume() {
        const state = loadState();
        if (!state) return;
        // Only resume if state is recent (< 2 hours)
        if (Date.now() - state.ts > 2 * 60 * 60 * 1000) {
            clearState();
            return;
        }
        ensureDock();
        dock.classList.add('open');
        document.body.classList.add('has-audio-dock');

        const onCanPlay = () => {
            audio.removeEventListener('canplay', onCanPlay);
            audio.currentTime = state.currentTime || 0;
            if (state.playing) {
                audio.play().catch(() => { });
            }
        };
        if (audio.readyState >= 2) {
            onCanPlay();
        } else {
            audio.addEventListener('canplay', onCanPlay);
        }
    }

    /* -------------------------------------------------------
       Save state before navigating away
    ------------------------------------------------------- */
    window.addEventListener('beforeunload', () => {
        if (audio && !audio.paused) {
            saveState(audio.currentTime, true);
        } else if (audio && audio.currentTime > 0) {
            saveState(audio.currentTime, false);
        }
    });

    /* -------------------------------------------------------
       Public API
    ------------------------------------------------------- */
    window.lifAudioPlayer = {
        open: function () { openPlayer(); },
        resume: function (t) { openPlayer(t); },
    };

    /* -------------------------------------------------------
       Init on DOMContentLoaded
    ------------------------------------------------------- */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', autoResume);
    } else {
        autoResume();
    }
})();
