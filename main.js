import { songs } from './songs.js';

const state = {
    score: 0,
    streak: 0,
    currentSong: null,
    isPlaying: false,
    player: null,
    isPlayerReady: false,
    playbackTimeout: null,
    currentStartTime: 0
};

// DOM Elements
const playBtn = document.getElementById('play-btn');
const statusMsg = document.getElementById('status-message');
const scoreEl = document.getElementById('score');
const streakEl = document.getElementById('streak');
const choiceBtns = document.querySelectorAll('.choice-btn');
const app = document.getElementById('app');

// Initialize YouTube API
const tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
const firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

window.onYouTubeIframeAPIReady = () => {
    state.player = new YT.Player('audio-container', {
        height: '0',
        width: '0',
        playerVars: {
            'playsinline': 1,
            'controls': 0,
            'disablekb': 1
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
            'onError': onPlayerError
        }
    });
};

function onPlayerReady(event) {
    console.log("Player ready");
    state.isPlayerReady = true;
    event.target.setVolume(100);
    statusMsg.textContent = "Ready to play!";
    playBtn.disabled = false;
}

function onPlayerError(event) {
    console.error("YouTube Player Error:", event.data);
    statusMsg.textContent = "Error loading audio. Try refreshing.";
    statusMsg.style.color = "#ff3333";
}

function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.ENDED) {
        stopPlaying();
    }
}

function loadRandomSong() {
    // 50/50 chance for each artist
    const targetBand = Math.random() < 0.5 ? 'Zedd' : 'Zeds Dead';
    const bandSongs = songs.filter(s => s.artist === targetBand);

    // Fallback if something is wrong with filtering (shouldn't happen)
    if (bandSongs.length === 0) {
        console.warn(`No songs found for ${targetBand}, falling back to random`);
        const randomIndex = Math.floor(Math.random() * songs.length);
        state.currentSong = songs[randomIndex];
    } else {
        const randomIndex = Math.floor(Math.random() * bandSongs.length);
        state.currentSong = bandSongs[randomIndex];
    }

    if (state.player && state.isPlayerReady) {
        // Randomize start time if totalDuration is available
        let startTime = state.currentSong.startTime;
        if (state.currentSong.totalDuration) {
            // Ensure we have at least 20s of play time
            const maxStart = Math.max(0, state.currentSong.totalDuration - 20);
            startTime = Math.floor(Math.random() * maxStart);
        }

        state.currentStartTime = startTime;

        state.player.cueVideoById({
            videoId: state.currentSong.youtubeId,
            startSeconds: startTime
        });
        // No need to pause, cueing doesn't auto-play
        playBtn.disabled = false;
    }
}

function playSong() {
    if (!state.isPlayerReady || !state.currentSong) {
        loadRandomSong();
    }

    if (state.player) {
        // Clear any existing timeout
        if (state.playbackTimeout) {
            clearTimeout(state.playbackTimeout);
        }

        // Use loadVideoById to ensure playback starts reliably
        // This fixes the issue where playVideo() sometimes fails after cueing
        state.player.loadVideoById({
            videoId: state.currentSong.youtubeId,
            startSeconds: state.currentStartTime
        });

        state.isPlaying = true;
        statusMsg.textContent = "Choose wisely";
        statusMsg.style.color = "var(--text-color)";
        updateUI();

        // Stop after duration
        state.playbackTimeout = setTimeout(() => {
            if (state.isPlaying) {
                stopPlaying();
            }
        }, state.currentSong.duration * 1000);
    }
}

function stopPlaying() {
    if (state.player) {
        state.player.pauseVideo();
    }
    if (state.playbackTimeout) {
        clearTimeout(state.playbackTimeout);
        state.playbackTimeout = null;
    }
    state.isPlaying = false;
    updateUI();
}

function handleGuess(artist) {
    if (!state.currentSong) return;

    const isCorrect = artist === state.currentSong.artist;

    // Disable play button during transition
    playBtn.disabled = true;

    const cleanSongTitle = cleanTitle(state.currentSong.title);

    if (isCorrect) {
        state.score += 10;
        state.streak += 1;

        const successMessages = [
            "Correct",
            "You got it",
            "Nailed it"
        ];
        const randomMsg = successMessages[Math.floor(Math.random() * successMessages.length)];

        statusMsg.textContent = `${randomMsg} It was ${cleanSongTitle}`;
        statusMsg.style.color = "var(--accent-color)";
        triggerConfetti();

        // Add bounce animation to the correct button
        const btn = artist === 'Zedd' ? document.querySelector('.zedd') : document.querySelector('.zeds-dead');
        btn.classList.add('bounce');
        setTimeout(() => btn.classList.remove('bounce'), 1000);

    } else {
        state.streak = 0;

        const failMessages = [
            "Wrong",
            "Incorrect",
            "No",
            "Nope"
        ];
        const randomMsg = failMessages[Math.floor(Math.random() * failMessages.length)];

        statusMsg.textContent = `${randomMsg} It was ${cleanSongTitle} by ${state.currentSong.artist}`;
        statusMsg.style.color = "#ff6b6b";

        // Add shake animation to the game container
        const container = document.querySelector('.game-container');
        container.classList.add('shake');
        setTimeout(() => container.classList.remove('shake'), 500);
    }

    scoreEl.textContent = state.score;
    streakEl.textContent = state.streak;

    stopPlaying();

    // Load next song after a delay
    setTimeout(() => {
        statusMsg.textContent = "Ready for next song...";
        statusMsg.style.color = "#aaa";
        loadRandomSong();
    }, 2000);
}

function updateUI() {
    if (state.isPlaying) {
        app.classList.add('playing');
        playBtn.innerHTML = '<svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>'; // Pause icon
    } else {
        app.classList.remove('playing');
        playBtn.innerHTML = '<svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'; // Play icon
    }
}

function triggerConfetti() {
    // Simple CSS based visual feedback or we could import a library
    // For now, just a console log or simple effect
    console.log("Confetti!");
}

function cleanTitle(title) {
    let cleaned = title
        // Decode HTML entities
        .replace(/&quot;/g, '"')
        .replace(/&amp;/g, '&')
        .replace(/&#39;/g, "'")
        // Remove standard suffixes
        .replace(/\(Official Video\)/gi, '')
        .replace(/\(Official Music Video\)/gi, '')
        .replace(/\(Official Audio\)/gi, '')
        .replace(/\(Official Visualizer\)/gi, '')
        .replace(/\(Official Lyric Video\)/gi, '')
        .replace(/\(Live\)/gi, '')
        .replace(/\(Live on KEXP\)/gi, '')
        .replace(/\[4K\]/gi, '')
        .replace(/\[Full Album\]/gi, '')
        // Remove band prefixes (more aggressive)
        .replace(/^Zedd\s*[-:"']?\s*/i, '')
        .replace(/^Zeds Dead\s*[-:"']?\s*/i, '')
        .replace(/^Zedd\s+/i, '') // Just the name and space
        .replace(/^Zeds Dead\s+/i, '')
        // Remove specific show patterns
        .replace(/Saturday Sessions: Goose performs /gi, '')
        .replace(/ \| The Tonight Show Starring Jimmy Fallon/gi, '')
        .replace(/ \| From The Basement/gi, '')
        .replace(/Official TGR x Goose /gi, '')
        .replace(/ Music Video/gi, '') // Cleanup for TGR
        // Remove trailing junk
        .replace(/ - \d+\/\d+\/\d+ .*/, '') // Remove dates/locations
        .trim();

    // Remove surrounding quotes if present
    if (cleaned.startsWith('"') && cleaned.endsWith('"')) {
        cleaned = cleaned.slice(1, -1);
    }

    return cleaned;
}

// Event Listeners
playBtn.addEventListener('click', () => {
    if (state.isPlaying) {
        stopPlaying();
    } else {
        playSong();
    }
});

choiceBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const artist = btn.dataset.artist;
        handleGuess(artist);
    });
});

// Initial load
// Wait for API to be ready before loading first song
const checkReady = setInterval(() => {
    if (state.isPlayerReady) {
        loadRandomSong();
        clearInterval(checkReady);
    }
}, 500);
