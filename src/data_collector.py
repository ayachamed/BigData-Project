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
                'order': 'relevance' # Use relevance within the chunks for better content mix
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
                    duration_str = stats.get('duration', '')
                    duration_seconds = utils.parse_duration(duration_str)
                    if duration_seconds < 60:
                        # print(f"     [Debug] Discarded Short: {video_id} ({duration_str})") # Commented out to reduce noise, enable if needed
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

def collect_videos_split_window(collector, query, target=100):
    """Collect videos using split-window strategy for timeline coverage."""
    # Split 2023-2025 into two chunks for temporal distribution
    chunk1_videos = collector.search_videos(
        query, max_results=50,
        published_after="2023-10-06T00:00:00Z",
        published_before="2024-10-06T23:59:59Z"
    )
    
    chunk2_videos = collector.search_videos(
        query, max_results=50,
        published_after="2024-10-07T00:00:00Z",
        published_before="2025-10-11T23:59:59Z"
    )
    
    videos = chunk1_videos + chunk2_videos
    
    # Fallback: fill to target if needed
    if len(videos) < target:
        deficit = target - len(videos)
        print(f"   - Collecting {deficit} more videos...")
        
        fallback = collector.search_videos(
            query, max_results=deficit,
            published_after="2023-10-06T00:00:00Z",
            published_before="2025-10-11T23:59:59Z"
        )
        
        # Deduplicate
        existing_ids = {v['videoId'] for v in videos}
        videos.extend(v for v in fallback if v['videoId'] not in existing_ids)
    
    return videos[:target]  # Ensure max limit


def main():
    """Main data collection pipeline."""
    # Load API key
    try:
        import config
        API_KEY = config.API_KEY
    except ImportError:
        print("ERROR: config.py missing. Create it with your API_KEY.")
        return
    
    # Configuration
    queries = [
        "Gaza war",
        "Israel Palestine conflict",
        "Gaza humanitarian crisis",
        "Palestine news",
        "Israel Hamas war"
    ]
    
    collector = YouTubeCollector(API_KEY)
    all_videos = []
    
    print("=== YOUTUBE DATA COLLECTION ===")
    print(f"Period: 2023-10-06 to 2025-10-11")
    print(f"Target: 100 long-form videos per query\n")
    
    # Collect videos for each query
    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] {query}")
        
        videos = collect_videos_split_window(collector, query, target=100)
        
        # Fetch comments
        for j, video in enumerate(videos, 1):
            title_preview = video['title'][:50] + "..." if len(video['title']) > 50 else video['title']
            print(f"   [{j}/{len(videos)}] {title_preview}")
            
            video['comments'] = collector.get_comments(video['videoId'], max_comments=30)
            video['commentsCount'] = len(video['comments'])
            
            all_videos.append(video)
            time.sleep(0.5)
        
        time.sleep(1)
    
    # Save
    print(f"\n💾 Saving data...")
    collector.save_to_files(all_videos, output_dir="data")
    
    # Summary
    total_comments = sum(len(v.get('comments', [])) for v in all_videos)
    print(f"\n✓ Collection completed!")
    print(f"   - Videos: {len(all_videos)}")
    print(f"   - Comments: {total_comments}")


if __name__ == "__main__":
    main()
