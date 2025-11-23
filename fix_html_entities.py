import json
import html

# Load the songs
with open('songs.js', 'r') as f:
    content = f.read()
    # Extract the JSON array part
    json_str = content.replace('export const songs = ', '').rstrip(';')
    songs = json.loads(json_str)

print(f"Processing {len(songs)} songs...")

# Clean up HTML entities in titles
cleaned_count = 0
for song in songs:
    original_title = song['title']
    # Decode HTML entities
    cleaned_title = html.unescape(original_title)
    
    if original_title != cleaned_title:
        print(f"Cleaned: {original_title}")
        print(f"      -> {cleaned_title}")
        song['title'] = cleaned_title
        cleaned_count += 1

print(f"\nCleaned {cleaned_count} song titles with HTML entities.")

# Write back to songs.js
with open('songs.js', 'w') as f:
    f.write(f"export const songs = {json.dumps(songs, indent=4)};")

print("Done! Updated songs.js")
