# Zedd or Zeds Dead?

Can you tell the difference between Zedd and Zeds Dead? Test your EDM knowledge with this music guessing game!

## 🎵 How to Play

1. Click the play button to hear a 15-second clip from a song
2. Guess whether it's by **Zedd** or **Zeds Dead**
3. Track your score and streak!

## 🎮 Features

- 308 songs total (167 Zedd, 141 Zeds Dead)
- 50/50 randomization ensures fair gameplay
- Only official channel uploads
- Sleek EDM-themed design with neon colors
- Responsive mobile-friendly layout

## 🛠️ Tech Stack

- Vanilla JavaScript (ES6 modules)
- YouTube IFrame API for audio playback
- CSS Grid & Flexbox for responsive layout
- Google Fonts (Fredoka One, Outfit)

## 🚀 Development

### Prerequisites

- Python 3 (for fetching songs)
- YouTube Data API v3 key

### Fetching Songs

To refresh the song list:

```bash
export YOUTUBE_API_KEY=your_api_key_here
python3 fetch_songs.py
```

This will fetch the latest videos from the official Zedd and Zeds Dead YouTube channels.

### Local Development

Simply open `index.html` in a modern browser or use a local server:

```bash
python3 -m http.server 8000
```

## 📝 License

Project created for educational and entertainment purposes.

## 🙏 Credits

Inspired by the "Goose or Geese" game. All music belongs to the respective artists (Zedd and Zeds Dead).
