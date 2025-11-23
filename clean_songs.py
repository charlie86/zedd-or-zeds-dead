import json
import re

# Load the songs
with open('songs.js', 'r') as f:
    content = f.read()
    # Extract the JSON array part
    json_str = content.replace('export const songs = ', '').replace(';', '')
    songs = json.loads(json_str)

initial_count = len(songs)
print(f"Initial song count: {initial_count}")

# Define exclusion patterns (case-insensitive)
exclusion_patterns = [
    r"making of",
    r"behind the scenes",
    r"recap",
    r"event #",
    r"thank you",
    r"residency",
    r"shorts",
    r"sound check",
    r"scariest flight",
    r"super nintendo world",
    r"returns to",
    r"out now",
    r"out this friday",
    r"out next week",
    r"is out",
    r"teaser",
    r"trailer",
    r"full album",
    r"interview",
    r"review",
    r"reaction",
    r"podcast",
    r"episode",
    r"live at", # Often just a set, not a specific song unless formatted well, but let's be careful. User didn't explicitly say remove live sets, but "ZEDD LIVE @ ULTRA" is usually a full set.
    r"live @",
    r"vertical video", # Usually duplicate
    r"waltz video", # Usually duplicate
    r"dragon ball daima", # Anime themes might be okay, but user flagged "Making Of" so maybe they want strict music videos? Let's keep anime themes for now unless they look like promos.
    # User flagged "Zedd - Making Of "Spectrum" Music Video"
    # User flagged "Thank you Ottawa!!!"
    # User flagged "VEGAS!!! Catch my 2024 residency..."
]

# Additional specific titles or patterns based on user feedback
specific_exclusions = [
    "zedd - making of",
    "vegas!!! catch my",
    "thank you ottawa",
    "our new song",
    "scariest flight",
    "went to super nintendo world",
    "this is why we sound check",
    "zedd in the park",
    "telos tour",
    "europe tour",
    "echo tour",
    "edc mexico",
    "ultra china",
    "ultra japan",
    "true colors - event",
    "behind the scenes",
    "lost in japan"
]

cleaned_songs = []
removed_count = 0

for song in songs:
    title = song['title'].lower()
    should_remove = False
    
    # Remove very short videos (likely social clips)
    if song.get('totalDuration', 0) < 45:
        should_remove = True
        print(f"Removing (too short < 45s): {song['title']}")

    # Check general patterns
    if not should_remove:
        for pattern in exclusion_patterns:
            if re.search(pattern, title):
                should_remove = True
                print(f"Removing (pattern '{pattern}'): {song['title']}")
                break
            
    # Check specific phrases if not already removed
    if not should_remove:
        for phrase in specific_exclusions:
            if phrase in title:
                should_remove = True
                print(f"Removing (phrase '{phrase}'): {song['title']}")
                break
    
    # Check for "Live @" or "Live at" which are often full sets (1hr+)
    # But keep "Live from" if it looks like a single song performance
    if not should_remove:
        if "live @" in title or "live at ultra" in title or "live at coachella" in title:
             # Check duration if available? The json has 'totalDuration'.
             # Full sets are usually long.
             if song.get('totalDuration', 0) > 600: # > 10 mins
                 should_remove = True
                 print(f"Removing (long live set): {song['title']}")

    if not should_remove:
        cleaned_songs.append(song)
    else:
        removed_count += 1

print(f"\nRemoved {removed_count} songs.")
print(f"Remaining song count: {len(cleaned_songs)}")

# Write back to songs.js
with open('songs.js', 'w') as f:
    f.write(f"export const songs = {json.dumps(cleaned_songs, indent=4)};")
