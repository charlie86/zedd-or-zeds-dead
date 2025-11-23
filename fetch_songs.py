import sys
import os
import json
import urllib.request
import urllib.parse
import re
import random

API_KEY = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('YOUTUBE_API_KEY')

if not API_KEY:
    print("Please provide a YouTube API key as an argument or set YOUTUBE_API_KEY environment variable.")
    sys.exit(1)

ARTISTS = [
    { 'name': 'Zedd', 'query': 'Zedd official video', 'channelId': 'UCPNokRZ9hacjIQ3IQL6HNUQ' },
    { 'name': 'Zeds Dead', 'query': 'Zeds Dead official video', 'channelId': 'UCsYkUlicwVBtW-pAInUSyPA' }
]
MAX_RESULTS = 50

def parse_duration(duration_str):
    """Parses ISO 8601 duration (e.g., PT4M13S) into seconds."""
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    return hours * 3600 + minutes * 60 + seconds

def get_video_details(video_ids, api_key):
    """Fetches content details (duration) for a list of video IDs."""
    if not video_ids:
        return {}
        
    ids_str = ",".join(video_ids)
    url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={ids_str}&key={api_key}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            parsed = json.loads(data)
            
            details = {}
            for item in parsed.get('items', []):
                duration_sec = parse_duration(item['contentDetails']['duration'])
                details[item['id']] = duration_sec
            return details
    except Exception as e:
        print(f"Error fetching video details: {e}")
        return {}

def search_youtube_page(query, api_key, channel_id=None, page_token=None):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={encoded_query}&type=video&maxResults=50&key={api_key}"
    if channel_id:
        url += f"&channelId={channel_id}"
    if page_token:
        url += f"&pageToken={page_token}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return {}

def main():
    all_songs = []
    
    for artist in ARTISTS:
        print(f"Fetching songs for {artist['name']}...")
        songs_added = 0
        next_page_token = None
        
        while songs_added < 200:
            try:
                response = search_youtube_page(artist['query'], API_KEY, artist.get('channelId'), next_page_token)
                items = response.get('items', [])
                next_page_token = response.get('nextPageToken')
                
                if not items:
                    break
                
                # Filter out non-music content
                filtered_items = []
                
                for item in items:
                    title = item['snippet']['title'].lower()
                    # Remove non-songs
                    if ('interview' in title or 'review' in title or 'reaction' in title or 
                        'podcast' in title or 'episode' in title or 'out now' in title or 
                        'out next week' in title or 'is out' in title or 'out this friday' in title or
                        'teaser' in title or 'trailer' in title or 'full album' in title or
                        'making of' in title or 'behind the scenes' in title or 'recap' in title or
                        'event #' in title or 'thank you' in title or 'residency' in title or
                        'shorts' in title or 'sound check' in title or 'scariest flight' in title or
                        'super nintendo world' in title or 'returns to' in title or
                        'live @' in title or 'live at' in title or 'vertical video' in title or
                        'waltz video' in title or 'dragon ball daima' in title or
                        'zedd in the park' in title or 'tour' in title or 'edc mexico' in title or
                        'ultra china' in title or 'ultra japan' in title or 'true colors - event' in title):
                        continue
                        
                    filtered_items.append(item)
                
                if not filtered_items:
                    if not next_page_token:
                        break
                    continue

                # Get video IDs to fetch details
                video_ids = [item['id']['videoId'] for item in filtered_items]
                video_details = get_video_details(video_ids, API_KEY)
                
                for item in filtered_items:
                    video_id = item['id']['videoId']
                    duration = video_details.get(video_id, 0)
                    
                    # Skip if duration is too short (< 30s) or missing
                    if duration < 30:
                        continue
                        
                    # Calculate random start time
                    max_start = max(0, duration - 20) 
                    start_time = random.randint(0, max_start)
                    
                    song = {
                        'id': f"{artist['name'].lower().replace(' ', '-')}-{video_id}",
                        'artist': artist['name'],
                        'title': item['snippet']['title'],
                        'youtubeId': video_id,
                        'startTime': start_time,
                        'duration': 15,
                        'totalDuration': duration
                    }
                    all_songs.append(song)
                    songs_added += 1
                    
                    if songs_added >= 200:
                        break
                
                print(f"  Fetched page. Total so far: {songs_added}")
                
                if not next_page_token:
                    break
                    
            except Exception as e:
                print(f"Error fetching for {artist['name']}: {e}")
                break
        
        print(f"Finished {artist['name']}: Found {songs_added} songs")

    # Write to songs.js
    with open('songs.js', 'w') as f:
        f.write(f"export const songs = {json.dumps(all_songs, indent=4)};")
    print(f'Saved {len(all_songs)} songs to songs.js')

if __name__ == "__main__":
    main()
