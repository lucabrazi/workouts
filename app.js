// Function to toggle the modal menu
function toggleMenu() {
    const modal = document.getElementById('navModal');
    if (modal) modal.classList.toggle('show');
}

// Functions for the Exercise Info Modal
function openInfoModal(event, btn) {
    event.stopPropagation(); // Prevents clicks from triggering parent elements
    document.getElementById('infoModalTitle').textContent = btn.getAttribute('data-name');
    document.getElementById('infoModalDesc').textContent = btn.getAttribute('data-desc');

    // Check for a video link and display the button if it exists
    const videoBtn = document.getElementById('infoModalVideoBtn');
    const videoUrl = btn.getAttribute('data-video');
    if (videoUrl) {
        videoBtn.style.display = 'flex';
        videoBtn.setAttribute('data-url', videoUrl);
        videoBtn.textContent = isEmbeddableVideo(videoUrl) ? '▶ Watch Video' : '▶ Find Videos on YouTube';
    } else {
        videoBtn.style.display = 'none';
    }

    const modal = document.getElementById('infoModal');
    if (modal) modal.classList.add('show');
}

function closeInfoModal() {
    const modal = document.getElementById('infoModal');
    if (modal) modal.classList.remove('show');
}

// Single YouTube videos can play in the popup; anything else (e.g. a search page) can't be embedded
function isEmbeddableVideo(url) {
    return url.includes('youtube.com/watch?v=') || url.includes('youtu.be/');
}

function openVideoModal() {
    let url = document.getElementById('infoModalVideoBtn').getAttribute('data-url');
    if (!url) return;

    if (!isEmbeddableVideo(url)) {
        closeInfoModal();
        window.open(url, '_blank', 'noopener');
        return;
    }

    // Auto-convert standard YouTube links to iframe embed links
    if (url.includes('youtube.com/watch?v=')) {
        url = url.replace('youtube.com/watch?v=', 'youtube.com/embed/').split('&')[0];
    } else if (url.includes('youtu.be/')) {
        url = url.replace('youtu.be/', 'youtube.com/embed/').split('?')[0];
    }

    closeInfoModal(); // Close the info modal to make way for the video
    document.getElementById('videoIframe').src = url;
    const modal = document.getElementById('videoModal');
    if (modal) modal.classList.add('show');
}

function closeVideoModal() {
    const modal = document.getElementById('videoModal');
    if (modal) modal.classList.remove('show');
    document.getElementById('videoIframe').src = ''; // Clear src to stop video playback
}

// Custom Confirm Modal Logic
let pendingConfirmCallback = null;

function openConfirmModal(msg, callback, title = 'Confirm Reset', actionLabel = 'Reset') {
    document.getElementById('confirmModalMsg').textContent = msg;
    document.getElementById('confirmModalTitle').textContent = title;
    document.getElementById('confirmActionBtn').textContent = actionLabel;
    pendingConfirmCallback = callback;
    const modal = document.getElementById('confirmModal');
    if (modal) modal.classList.add('show');
}

function closeConfirmModal() {
    pendingConfirmCallback = null;
    const modal = document.getElementById('confirmModal');
    if (modal) modal.classList.remove('show');
}

document.addEventListener('DOMContentLoaded', () => {
    const confirmBtn = document.getElementById('confirmActionBtn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            if (pendingConfirmCallback) {
                pendingConfirmCallback();
            }
            closeConfirmModal();
        });
    }
});

// Each routine page sets data-storage-prefix on <body> so checkbox progress doesn't collide
// between routines. The original routine keeps the old 'workout-cb-' keys.
const storagePrefix = document.body.dataset.storagePrefix || 'workout-cb-';

let currentActiveDay = 'overview';
let currentWorkoutMode = 'moderate';

// Helper to update URL with day and mode parameters
function updateUrl(dayId, mode) {
    const currentUrl = new URL(window.location.href);
    const params = new URLSearchParams();

    if (mode === 'extreme') {
        params.set('m', 'y');
    }
    if (dayId && dayId !== 'overview') {
        params.set('day', dayId);
    }

    const queryString = params.toString();
    const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + (queryString ? '?' + queryString : '');

    if (currentUrl.search !== (queryString ? '?' + queryString : '')) {
        window.history.pushState({ path: newUrl }, '', newUrl);
    }
}

// Function to set the workout intensity mode
function setMode(modeValue) {
    currentWorkoutMode = modeValue;

    // Sync select element state
    const modeSelect = document.getElementById('modeSelect');
    if (modeSelect) modeSelect.value = modeValue;

    // Apply theme tint
    const body = document.body;
    if (modeValue === 'extreme') {
        body.classList.add('theme-extreme');
    } else {
        body.classList.remove('theme-extreme');
    }

    // Dynamically update repetition texts in the DOM
    const repElements = document.querySelectorAll('.exercise-reps');
    repElements.forEach(el => {
        const moderateReps = el.getAttribute('data-reps-moderate') || el.textContent;
        const extremeReps = el.getAttribute('data-reps-extreme') || el.textContent;

        // Keep moderate default attributes if not present
        if (!el.hasAttribute('data-reps-moderate')) {
            el.setAttribute('data-reps-moderate', el.textContent);
        }

        if (modeValue === 'extreme') {
            el.textContent = extremeReps;
        } else {
            el.textContent = moderateReps;
        }
    });

    updateUrl(currentActiveDay, currentWorkoutMode);
}

// Function to switch visible workout day and modify the URL query variable
function setDay(dayId) {
    // Close modal if open
    const modal = document.getElementById('navModal');
    if (modal) modal.classList.remove('show');

    // Hide all workout views
    const views = document.querySelectorAll('.workout-day');
    views.forEach(view => view.classList.remove('active'));

    // Deactivate all navigation buttons
    const buttons = document.querySelectorAll('.nav-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Target view selection
    const selectedView = document.getElementById(dayId);
    if (selectedView) {
        selectedView.classList.add('active');

        // Highlight the matching menu button
        buttons.forEach(btn => {
            if ((btn.getAttribute('onclick') || '').includes(`'${dayId}'`)) {
                btn.classList.add('active');
            }
        });

        currentActiveDay = dayId;
        updateUrl(currentActiveDay, currentWorkoutMode);
    }
}

// Function to handle switching visual rounds
function changeRound(btn, direction, maxRounds) {
    const controls = btn.parentElement;
    const container = controls.parentElement;
    const indicator = controls.querySelector('.round-indicator');
    const lists = container.querySelectorAll('.round-list');

    let currentRound = 1;
    lists.forEach(list => {
        if (list.classList.contains('active')) currentRound = parseInt(list.dataset.round);
    });

    let newRound = currentRound + direction;
    if (newRound < 1) newRound = 1;
    if (newRound > maxRounds) newRound = maxRounds;

    lists.forEach(list => list.classList.remove('active'));
    container.querySelector(`.round-list[data-round="${newRound}"]`).classList.add('active');
    indicator.textContent = `Round ${newRound} / ${maxRounds}`;

    controls.querySelector('.prev-round').disabled = (newRound === 1);
    controls.querySelector('.next-round').disabled = (newRound === maxRounds);
}

// Dynamically build the UI for multiple rounds
function initRounds() {
    document.querySelectorAll('.rounds').forEach(roundSpan => {
        const h2 = roundSpan.parentElement;
        const ul = h2.nextElementSibling;
        if (ul && ul.tagName === 'UL') {
            // Use the largest number so a range like "2–3 Rounds" builds 3 rounds
            const match = roundSpan.textContent.match(/\d+/g);
            if (!match) return;

            const numRounds = Math.max(...match.map(Number));
            const container = document.createElement('div');
            container.className = 'rounds-container';
            h2.parentNode.insertBefore(container, ul);

            const controls = document.createElement('div');
            controls.className = 'round-controls';
            controls.innerHTML = `
                <button class="round-btn prev-round" onclick="changeRound(this, -1, ${numRounds})" disabled>&larr; Prev</button>
                <span class="round-indicator">Round 1 / ${numRounds}</span>
                <button class="round-btn next-round" onclick="changeRound(this, 1, ${numRounds})">Next &rarr;</button>
            `;
            container.appendChild(controls);

            for (let i = 1; i <= numRounds; i++) {
                const clone = (i === 1) ? ul : ul.cloneNode(true);
                clone.className = `round-list round-${i} ${i === 1 ? 'active' : ''}`;
                clone.dataset.round = i;

                // Update dynamic text variations per round
                clone.querySelectorAll('[data-round-text]').forEach(el => {
                    const texts = el.getAttribute('data-round-text').split('|');
                    el.textContent = texts[i - 1] || texts[texts.length - 1];
                });

                clone.querySelectorAll('[data-round-reps-moderate]').forEach(el => {
                    const texts = el.getAttribute('data-round-reps-moderate').split('|');
                    el.setAttribute('data-reps-moderate', texts[i - 1] || texts[texts.length - 1]);
                });

                clone.querySelectorAll('[data-round-reps-extreme]').forEach(el => {
                    const texts = el.getAttribute('data-round-reps-extreme').split('|');
                    el.setAttribute('data-reps-extreme', texts[i - 1] || texts[texts.length - 1]);
                });

                clone.querySelectorAll('[data-round-name]').forEach(el => {
                    const texts = el.getAttribute('data-round-name').split('|');
                    el.setAttribute('data-name', texts[i - 1] || texts[texts.length - 1]);
                });

                clone.querySelectorAll('[data-round-desc]').forEach(el => {
                    const texts = el.getAttribute('data-round-desc').split('|');
                    el.setAttribute('data-desc', texts[i - 1] || texts[texts.length - 1]);
                });

                // Clear checked states on clones to ensure they start empty
                if (i !== 1) clone.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
                container.appendChild(clone);
            }
        }
    });
}

// Function to reset all progress for the entire week
function resetWeek() {
    openConfirmModal('Are you sure you want to reset all workout progress for the week?', clearWeekProgress);
}

// Uncheck everything and put every round back to Round 1, without asking
function clearWeekProgress() {
    const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    allCheckboxes.forEach((cb, index) => {
        cb.checked = false;
        localStorage.removeItem(`${storagePrefix}${index}`);
    });

    // Reset all dynamic rounds back to Round 1
    document.querySelectorAll('.rounds-container').forEach(container => {
        const lists = container.querySelectorAll('.round-list');
        lists.forEach(list => list.classList.remove('active'));
        const firstRound = container.querySelector('.round-list[data-round="1"]');
        if (firstRound) firstRound.classList.add('active');

        const indicator = container.querySelector('.round-indicator');
        if (indicator) indicator.textContent = `Round 1 / ${lists.length}`;

        const prevBtn = container.querySelector('.prev-round');
        if (prevBtn) prevBtn.disabled = true;
        const nextBtn = container.querySelector('.next-round');
        if (nextBtn && lists.length > 1) nextBtn.disabled = false;
    });
}

// Function to reset progress for a specific day
function resetDay(dayId) {
    openConfirmModal('Are you sure you want to reset progress for this day?', () => {
        const dayDiv = document.getElementById(dayId);
        if (!dayDiv) return;

        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
        allCheckboxes.forEach((cb, index) => {
            if (dayDiv.contains(cb)) {
                cb.checked = false;
                localStorage.removeItem(`${storagePrefix}${index}`);
            }
        });

        // Reset dynamic rounds within this day only
        dayDiv.querySelectorAll('.rounds-container').forEach(container => {
            const lists = container.querySelectorAll('.round-list');
            lists.forEach(list => list.classList.remove('active'));
            const firstRound = container.querySelector('.round-list[data-round="1"]');
            if (firstRound) firstRound.classList.add('active');

            const indicator = container.querySelector('.round-indicator');
            if (indicator) indicator.textContent = `Round 1 / ${lists.length}`;

            const prevBtn = container.querySelector('.prev-round');
            if (prevBtn) prevBtn.disabled = true;
            const nextBtn = container.querySelector('.next-round');
            if (nextBtn && lists.length > 1) nextBtn.disabled = false;
        });
    });
}

// On initial page load: check URL variables
window.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize rounds first so dynamic checkboxes are created
    initRounds();

    const urlParams = new URLSearchParams(window.location.search);

    // Check for mode parameter (only routines with a mode selector support Extreme)
    const initialMode = urlParams.get('m');
    if (initialMode && initialMode.toLowerCase() === 'y' && document.getElementById('modeSelect')) {
        setMode('extreme');
    } else {
        setMode('moderate');
    }

    const initialDay = urlParams.get('day');

    // Valid views are whatever days this routine page defines
    const validDays = Array.from(document.querySelectorAll('.workout-day')).map(view => view.id);

    if (initialDay && validDays.includes(initialDay.toLowerCase())) {
        setDay(initialDay.toLowerCase());
    } else {
        setDay('overview'); // Default fallback
    }

    // 2. Add LocalStorage persistence for all checkboxes
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach((cb, index) => {
        const savedState = localStorage.getItem(`${storagePrefix}${index}`);
        if (savedState === 'true') cb.checked = true;

        cb.addEventListener('change', (e) => {
            localStorage.setItem(`${storagePrefix}${index}`, e.target.checked);
        });
    });
});
