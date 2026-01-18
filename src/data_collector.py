import requests
import json
import time
import pandas as pd
from datetime import datetime, timedelta
import utils

class YouTubeCollector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def search_videos(self, query, max_results=50, published_after=None, published_before=None):
        """Search videos by keyword with strict constraints"""
        videos = []
        next_page_token = None
        
        # Enforce max_results to be at least 50 if possible (but we fetch in batches if needed)
        # The user requested "never 25", so we aim for 50.
        target_results = max(max_results, 50)
        
        print(f"   Targeting {target_results} videos for query '{query}'...")

        url = f"{self.base_url}/search"
        
        while len(videos) < target_results:
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': min(target_results - len(videos), 50), # API limit is 50
                'key': self.api_key,
                'order': 'date' # Use date to ensure we get the relevant window coverage if needed
            }
            
            if published_after:
                params['publishedAfter'] = published_after
            if published_before:
                params['publishedBefore'] = published_before
            if next_page_token:
                params['pageToken'] = next_page_token
                
            try:
                response = requests.get(url, params=params)
                data = response.json()
                
                if 'items' not in data:
                    print(f"   No items found or API error: {data}")
                    break
                    
                for item in data['items']:
                    video_id = item['id']['videoId']
                    
                    # Get detailed stats to check duration (filter shorts)
                    stats = self.get_video_details(video_id)
                    
                    if not stats: 
                        continue
                        
                    # Filter Shorts: Duration must be >= 60 seconds
                    duration_seconds = utils.parse_duration(stats.get('duration', ''))
                    if duration_seconds < 60:
                        continue
                        
                    video_data = {
                        'videoId': video_id,
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'publishedAt': item['snippet']['publishedAt'],
                        'channelTitle': item['snippet']['channelTitle'],
                        'query': query,
                        'durationVal': duration_seconds # Keep for debugging
                    }
                    video_data.update(stats)
                    videos.append(video_data)
                    
                    if len(videos) >= target_results:
                        break
                
                if 'nextPageToken' in data and len(videos) < target_results:
                    next_page_token = data['nextPageToken']
                    time.sleep(0.2) # API rate limit safety
                else:
                    break
                    
            except Exception as e:
                print(f"Error during search: {e}")
                break
                
        if len(videos) < target_results:
            print(f"   Warning: Could only find {len(videos)} videos matching constraints (Target: {target_results})")

        return videos
    
    def get_video_details(self, video_id):
        """Get video statistics and content details (for duration)"""
        url = f"{self.base_url}/videos"
        params = {
            'part': 'statistics,snippet,contentDetails',
            'id': video_id,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                item = data['items'][0]
                return {
                    'viewCount': item['statistics'].get('viewCount', 0),
                    'likeCount': item['statistics'].get('likeCount', 0),
                    'commentCount': item['statistics'].get('commentCount', 0),
                    'tags': item['snippet'].get('tags', []),
                    'duration': item['contentDetails'].get('duration', ''),
                    'definition': item['contentDetails'].get('definition', '')
                }
        except Exception as e:
            print(f"Error getting video stats {video_id}: {e}")
            
        return None
    
    def get_comments(self, video_id, max_comments=100):
        """Get video comments with English filtering"""
        comments = []
        url = f"{self.base_url}/commentThreads"
        params = {
            'part': 'snippet',
            'videoId': video_id,
            'maxResults': min(max_comments, 100),
            'key': self.api_key,
            'order': 'relevance'
        }
        
        try:
            while len(comments) < max_comments:
                response = requests.get(url, params=params)
                data = response.json()
                
                if 'items' not in data:
                    break
                    
                for item in data['items']:
                    comment_snip = item['snippet']['topLevelComment']['snippet']
                    text = comment_snip['textDisplay']
                    
                    # ENGLISH FILTERING
                    if not utils.is_english(text):
                        continue
                        
                    comments.append({
                        'videoId': video_id,
                        'commentId': item['id'],
                        'author': comment_snip['authorDisplayName'],
                        'text': text,
                        'likeCount': comment_snip['likeCount'],
                        'publishedAt': comment_snip['publishedAt'],
                        'sentiment': 'neutral'
                    })
                
                if 'nextPageToken' in data and len(comments) < max_comments:
                    params['pageToken'] = data['nextPageToken']
                else:
                    break
                    
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error getting comments {video_id}: {e}")
            
        return comments

    def save_to_files(self, videos_data, output_dir="."):
        """Save data to JSON and CSV files"""
        if not videos_data:
            print("No data to save.")
            return

        # Save videos
        with open(f'{output_dir}/youtube_videos.json', 'w', encoding='utf-8') as f:
            json.dump(videos_data, f, ensure_ascii=False, indent=2)
        
        # Save to CSV
        df_videos = pd.DataFrame(videos_data)
        # Drop complex objects for CSV if needed, but pandas usually handles basic dicts as strings
        df_videos.to_csv(f'{output_dir}/youtube_videos.csv', index=False, encoding='utf-8')
        
        # Save all comments
        all_comments = []
        for video in videos_data:
            all_comments.extend(video.get('comments', []))
        
        with open(f'{output_dir}/youtube_comments.json', 'w', encoding='utf-8') as f:
            json.dump(all_comments, f, ensure_ascii=False, indent=2)
        
        if all_comments:
            df_comments = pd.DataFrame(all_comments)
            df_comments.to_csv(f'{output_dir}/youtube_comments.csv', index=False, encoding='utf-8')

def main():
    # Load configuration
    try:
        import config
        API_KEY = config.API_KEY
    except ImportError:
        print("Error: config.py file is missing. Please create a config.py file with your API_KEY.")
        return
    
    # Search keywords
    queries = [
        "Gaza war",
        "Israel Palestine conflict", 
        "Gaza humanitarian crisis",
        "Palestine news",
        "Israel Hamas war"
    ]
    
    # Strict Period: 2023-10-06 to 2025-10-11
    published_after = "2023-10-06T00:00:00Z"
    published_before = "2025-10-11T23:59:59Z"
    
    collector = YouTubeCollector(API_KEY)
    all_videos_data = []
    
    print(" Starting YouTube data collection...")
    print(f" Period: from {published_after} to {published_before}")
    print(f" Keywords: {queries}")
    print(" Constraints: >60s duration (Standard), English comments only, 50 videos per query.")
    
    for i, query in enumerate(queries, 1):
        print(f"\n Search {i}/{len(queries)}: '{query}'")
        
        # Requesting 50 videos
        videos = collector.search_videos(query, max_results=50, published_after=published_after, published_before=published_before)
        
        for j, video in enumerate(videos, 1):
            print(f"   Video {j}/{len(videos)}: {video['title'][:50]}... ({video.get('duration', 'N/A')})")
            
            # Get comments
            comments = collector.get_comments(video['videoId'], max_comments=30)
            video['comments'] = comments
            video['commentsCount'] = len(comments)
            
            all_videos_data.append(video)
            
            time.sleep(0.5)
        
        time.sleep(1)
    
    # Save data
    print(f"\n Saving data...")
    collector.save_to_files(all_videos_data, output_dir="data")
    
    # Statistics
    total_comments = sum(len(video.get('comments', [])) for video in all_videos_data)
    print(f"\n Collection completed!")
    print(f" Statistics:")
    print(f"   - Videos collected: {len(all_videos_data)}")
    print(f"   - Comments collected: {total_comments}")
    print(f"   - Files created: youtube_videos.json, youtube_videos.csv, youtube_comments.json, youtube_comments.csv")

if __name__ == "__main__":
    main()
