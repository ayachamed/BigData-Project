import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import re
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))
import utils
from utils import get_data_dir, get_outputs_dir
import json

# Chart configuration
plt.style.use('default')

# =========================
# DATA LOADING
# =========================
# Load CSV data (supports both JSON and CSV)
data_dir = get_data_dir()

if os.path.exists(f'{data_dir}/youtube_videos.json'):
    with open(f'{data_dir}/youtube_videos.json', 'r', encoding='utf-8') as f:
        videos_data = json.load(f)
    df_videos = pd.DataFrame(videos_data)
else:
    df_videos = pd.read_csv(f'{data_dir}/youtube_videos.csv')

# Convert numeric columns
df_videos['viewCount'] = pd.to_numeric(df_videos['viewCount'], errors='coerce')
df_videos['likeCount'] = pd.to_numeric(df_videos['likeCount'], errors='coerce')

print(" CREATING VISUALIZATIONS...")

# Get output directory
outputs_dir = get_outputs_dir()

# =========================
# 1. TOP CHANNELS
# =========================
plt.figure(figsize=(12, 6))
top_channels = df_videos['channelTitle'].value_counts().head(10)
if not top_channels.empty:
    plt.barh(range(len(top_channels)), top_channels.values)
    plt.yticks(range(len(top_channels)), top_channels.index)
    plt.title('Top 10 Channels by Video Count')
    plt.xlabel('Number of Videos')
    plt.tight_layout()
    plt.savefig(f'{outputs_dir}/top_channels.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Chart 1: Top channels created")

# =========================
# 2. MOST FREQUENT KEYWORDS
# =========================
plt.figure(figsize=(12, 6))

# Keyword extraction using utils for consistent stemming
all_titles = ' '.join(df_videos['title']).lower()
all_titles = re.sub(r'#\w+', '', all_titles)  # Remove hashtags

all_words = re.findall(r'\b\w+\b', all_titles)
stop_words = utils.get_stop_words()

normalized_words = []
for word in all_words:
    if len(word) > 3 and word not in stop_words:
        norm_word = utils.normalize_keyword(word)
        if norm_word and len(norm_word) > 3 and norm_word not in stop_words:
            normalized_words.append(norm_word)

word_counts = Counter(normalized_words)
top_words = dict(word_counts.most_common(15))

if top_words:
    plt.barh(range(len(top_words)), list(top_words.values()))
    plt.yticks(range(len(top_words)), list(top_words.keys()))
    plt.title('Top 15 Keywords in Titles (Normalized)')
    plt.xlabel('Frequency')
    plt.tight_layout()
    plt.savefig(f'{outputs_dir}/top_words.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Chart 2: Top keywords created")

# =========================
# 3. PERFORMANCE BY KEYWORD
# =========================
query_stats = df_videos.groupby('query').agg({
    'viewCount': 'sum',
    'likeCount': 'sum'
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.bar(range(len(query_stats)), query_stats['viewCount'])
ax1.set_title('Views by Keyword')
ax1.set_xticks(range(len(query_stats)))
ax1.set_xticklabels(query_stats.index, rotation=45)
ax1.set_ylabel('Views')

ax2.bar(range(len(query_stats)), query_stats['likeCount'])
ax2.set_title('Likes by Keyword')
ax2.set_xticks(range(len(query_stats)))
ax2.set_xticklabels(query_stats.index, rotation=45)
ax2.set_ylabel('Likes')

plt.tight_layout()
plt.savefig(f'{outputs_dir}/query_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Chart 3: Performance by keyword created")

# =========================
# 4. TOP MOST VIEWED VIDEOS
# =========================
plt.figure(figsize=(12, 8))
top_videos = df_videos.nlargest(8, 'viewCount')[['title', 'viewCount', 'channelTitle']]
top_videos['short_title'] = (
    top_videos['channelTitle'] + ': ' + top_videos['title'].str[:25] + '...'
)

if not top_videos.empty:
    plt.barh(range(len(top_videos)), top_videos['viewCount'])
    plt.yticks(range(len(top_videos)), top_videos['short_title'])
    plt.title('Top 8 Most Viewed Videos')
    plt.xlabel('Views')
    plt.tight_layout()
    plt.savefig(f'{outputs_dir}/top_videos.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Chart 4: Top videos created")

# =========================
# 5. TIMELINE EVOLUTION
# =========================
plt.figure(figsize=(14, 6))
df_videos['published_date'] = pd.to_datetime(df_videos['publishedAt'])

# Group by year-month for better visualization over 2-year range
df_videos['year_month'] = df_videos['published_date'].dt.to_period('M')
timeline = df_videos.groupby('year_month').size()

# Create complete range from Oct 2023 to Oct 2025
full_range = pd.period_range(start='2023-10', end='2025-10', freq='M')
timeline = timeline.reindex(full_range, fill_value=0)

# Convert period index to strings for plotting
timeline_dates = [str(period) for period in timeline.index]
timeline_values = timeline.values

if len(timeline_dates) > 0:
    plt.plot(
        timeline_dates,
        timeline_values,
        marker='o',
        linewidth=2,
        markersize=4
    )

    plt.title('Evolution of Published Videos Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Videos', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(f'{outputs_dir}/timeline.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Chart 5: Timeline created")

# =========================
# 6. KEYWORD DISTRIBUTION
# =========================
plt.figure(figsize=(10, 8))
query_counts = df_videos['query'].value_counts()
plt.pie(
    query_counts.values,
    labels=query_counts.index,
    autopct='%1.1f%%',
    startangle=90
)
plt.title('Distribution of Search Keywords')
plt.tight_layout()
plt.savefig(f'{outputs_dir}/query_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Chart 6: Keyword distribution created")

# =========================
# FINAL REPORT
# =========================
print("\n KEY STATISTICS REPORT:")
print(f"   • Videos analyzed: {len(df_videos)}")
print(f"   • Unique channels: {df_videos['channelTitle'].nunique()}")
print(f"   • Total views: {int(df_videos['viewCount'].sum()):,}")
print(f"   • Total likes: {int(df_videos['likeCount'].sum()):,}")
print(f"   • Most popular keyword: '{df_videos['query'].value_counts().index[0] if not df_videos.empty else 'N/A'}'")
print(f"   • Most active channel: '{df_videos['channelTitle'].value_counts().index[0] if not df_videos.empty else 'N/A'}'")
print(f"   • Most frequent word: '{word_counts.most_common(1)[0][0] if word_counts else 'N/A'}'")

print("\n 6 charts created successfully!")
print(" All charts are saved in outputs/")