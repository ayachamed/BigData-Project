import requests
import json
import time
import pandas as pd
from datetime import datetime, timedelta

class YouTubeCollector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def search_videos(self, query, max_results=25, published_after=None, published_before=None):
        """Search videos by keyword"""
        videos = []
        
        url = f"{self.base_url}/search"
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': min(max_results, 50),
            'key': self.api_key,
            'order': 'date'
        }
        
        if published_after:
            params['publishedAfter'] = published_after
            
        if published_before:
            params['publishedBefore'] = published_before
            
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data:
                for item in data['items']:
                    video_data = {
                        'videoId': item['id']['videoId'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'publishedAt': item['snippet']['publishedAt'],
                        'channelTitle': item['snippet']['channelTitle'],
                        'query': query
                    }
                    # Get statistics
                    stats = self.get_video_stats(item['id']['videoId'])
                    video_data.update(stats)
                    videos.append(video_data)
                    
        except Exception as e:
            print(f"Error during search: {e}")
            
        return videos
    
    def get_video_stats(self, video_id):
        """Get video statistics"""
        url = f"{self.base_url}/videos"
        params = {
            'part': 'statistics,snippet',
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
                    'tags': item['snippet'].get('tags', [])
                }
        except Exception as e:
            print(f"Error getting video stats {video_id}: {e}")
            
        return {
            'viewCount': 0,
            'likeCount': 0,
            'commentCount': 0,
            'tags': []
        }
    
    def get_comments(self, video_id, max_comments=100):
        """Get video comments"""
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
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'videoId': video_id,
                        'commentId': item['id'],
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'likeCount': comment['likeCount'],
                        'publishedAt': comment['publishedAt'],
                        'sentiment': 'neutral'  # For future analysis
                    })
                
                # Pagination
                if 'nextPageToken' in data and len(comments) < max_comments:
                    params['pageToken'] = data['nextPageToken']
                else:
                    break
                    
                time.sleep(0.1)  # Respect API quotas
                
        except Exception as e:
            print(f"Error getting comments {video_id}: {e}")
            
        return comments

    def save_to_files(self, videos_data, output_dir="."):
        """Save data to JSON and CSV files"""
        # Save videos
        with open(f'{output_dir}/youtube_videos.json', 'w', encoding='utf-8') as f:
            json.dump(videos_data, f, ensure_ascii=False, indent=2)
        
        # Save to CSV
        df_videos = pd.DataFrame(videos_data)
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
    
    # Period (from October 7, 2023 to October 10, 2025)
    published_after = "2023-10-07T00:00:00Z"
    published_before = "2025-10-10T23:59:59Z"
    
    collector = YouTubeCollector(API_KEY)
    all_videos_data = []
    
    print(" Starting YouTube data collection...")
    print(f" Period: from 10/07/2023 to 10/10/2025")
    print(f" Keywords: {queries}")
    
    for i, query in enumerate(queries, 1):
        print(f"\n Search {i}/{len(queries)}: '{query}'")
        
        videos = collector.search_videos(query, max_results=50, published_after=published_after, published_before=published_before)
        
        for j, video in enumerate(videos, 1):
            print(f"   Video {j}/{len(videos)}: {video['title'][:50]}...")
            
            # Get comments
            comments = collector.get_comments(video['videoId'], max_comments=30)
            video['comments'] = comments
            video['commentsCount'] = len(comments)
            
            all_videos_data.append(video)
            
            # Pause between requests
            time.sleep(0.5)
        
        # Pause between keywords
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
