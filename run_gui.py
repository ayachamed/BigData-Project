#!/usr/bin/env python3
"""
Main launcher for YouTube Gaza Data Collector
Integrates GUI with data collection pipeline
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui import launch_gui
from data_collector import YouTubeCollector, collect_videos_split_window
import time

def main():
    """Launch GUI and run collection pipeline."""
    
    print("=" * 60)
    print("YouTube Gaza Data Collector - GUI Mode")
    print("=" * 60)
    
    # Launch GUI to get configuration
    config = launch_gui()
    
    if not config:
        print("\n❌ Collection cancelled by user.")
        return
    
    print("\n" + "=" * 60)
    print("STARTING DATA COLLECTION")
    print("=" * 60)
    print(f"\n📋 Configuration:")
    print(f"   Queries: {', '.join(config['queries'])}")
    print(f"   Period: {config['start_date']} to {config['end_date']}")
    print(f"   Videos per query: {config['videos_per_query']}")
    print(f"   Total target: {len(config['queries']) * config['videos_per_query']} videos")
    
    # Load API key
    try:
        import config as api_config
        API_KEY = api_config.API_KEY
    except ImportError:
        print("\n❌ ERROR: config.py missing. Create it with your API_KEY.")
        return
    
    # Initialize collector
    collector = YouTubeCollector(API_KEY)
    all_videos = []
    
    # Convert dates to ISO format
    start_iso = f"{config['start_date']}T00:00:00Z"
    end_iso = f"{config['end_date']}T23:59:59Z"
    
    print("\n" + "=" * 60)
    print("COLLECTING VIDEOS")
    print("=" * 60)
    
    # Collect videos for each query
    for i, query in enumerate(config['queries'], 1):
        print(f"\n[{i}/{len(config['queries'])}] {query}")
        print("-" * 60)
        
        # Use split-window strategy for better timeline coverage
        videos = collect_videos_split_window(
            collector,
            query,
            target=config['videos_per_query']
        )
        
        print(f"✓ Collected {len(videos)} videos for '{query}'")
        
        # Fetch comments for each video
        print("   Fetching comments...")
        for j, video in enumerate(videos, 1):
            title_preview = video['title'][:50] + "..." if len(video['title']) > 50 else video['title']
            if j % 10 == 0 or j == len(videos):
                print(f"   [{j}/{len(videos)}] Processing...")
            
            video['comments'] = collector.get_comments(video['videoId'], max_comments=30)
            video['commentsCount'] = len(video['comments'])
            
            all_videos.append(video)
            time.sleep(0.5)
        
        print(f"✓ Processed all videos for '{query}'")
        time.sleep(1)
    
    # Save data
    print("\n" + "=" * 60)
    print("SAVING DATA")
    print("=" * 60)
    
    collector.save_to_files(all_videos, output_dir="data")
    
    # Summary
    total_comments = sum(len(v.get('comments', [])) for v in all_videos)
    
    print("\n" + "=" * 60)
    print("✓ COLLECTION COMPLETED!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   Total videos collected: {len(all_videos)}")
    print(f"   Total comments collected: {total_comments}")
    print(f"   Data saved to: data/")
    print(f"\n💡 Next steps:")
    print(f"   1. Run: python3 src/data_analyzer.py")
    print(f"   2. Run: python3 src/data_visualizer.py")
    print()


if __name__ == "__main__":
    main()
