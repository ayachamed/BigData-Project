from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, mean, to_date, 
    explode, split, lower, regexp_replace, trim, size, collect_list
)
from pyspark.sql.types import StringType
from pyspark.sql import functions as F
import json
from datetime import datetime
import re
from collections import Counter
import utils

print("=== ANALYSE DES VIDÉOS YOUTUBE SUR GAZA (PySpark) ===")

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("YouTubeGazaAnalysis") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Suppress INFO logs for cleaner output
spark.sparkContext.setLogLevel("WARN")

# Load data: Use pandas for JSON parsing, then convert to Spark
# (Spark's read.json() struggles with certain JSON array structures)
try:
    import pandas as pd_loader
    pd_videos = pd_loader.read_json('data/youtube_videos.json')
    pd_comments = pd_loader.read_json('data/youtube_comments.json')
    
    # Convert to Spark DataFrames
    df_videos = spark.createDataFrame(pd_videos)
    df_comments = spark.createDataFrame(pd_comments)
    
    print(f"✓ Data loaded successfully via pandas → Spark conversion")
    
except Exception as e:
    print(f"Files not found! Run data_collector.py first. Error: {e}")
    spark.stop()
    exit()

print(f"\n1.  STATISTIQUES GÉNÉRALES")
video_count = df_videos.count()
comment_count = df_comments.count()
print(f"   - Vidéos collectées: {video_count}")
print(f"   - Commentaires collectés: {comment_count}")

# Convert numeric columns and calculate stats
df_videos = df_videos.withColumn("viewCount", col("viewCount").cast("long")) \
                     .withColumn("likeCount", col("likeCount").cast("long")) \
                     .withColumn("commentCount", col("commentCount").cast("long"))

stats = df_videos.select(
    mean("viewCount").alias("avg_views"),
    mean("likeCount").alias("avg_likes"),
    mean("commentCount").alias("avg_comments")
).first()

print(f"   - Vues moyennes: {stats['avg_views']:.0f}")
print(f"   - Likes moyens: {stats['avg_likes']:.0f}")
print(f"   - Commentaires moyens: {stats['avg_comments']:.0f}")

# 2. TOP 10 CHANNELS using Spark SQL
print(f"\n2.  TOP 10 DES CHAÎNES")
df_videos.createOrReplaceTempView("videos")

top_channels = spark.sql("""
    SELECT 
        channelTitle,
        COUNT(*) as nb_videos,
        SUM(viewCount) as total_views,
        SUM(likeCount) as total_likes
    FROM videos
    GROUP BY channelTitle
    ORDER BY nb_videos DESC
    LIMIT 10
""")

# Convert to pandas for display (small dataset)
top_channels_pd = top_channels.toPandas()
print(top_channels_pd.to_string(index=False))

# 3. TEMPORAL EVOLUTION
print(f"\n3.  ÉVOLUTION TEMPORELLE")
df_videos = df_videos.withColumn("published_date", to_date(col("publishedAt")))
timeline = df_videos.groupBy("published_date") \
                    .agg(count("*").alias("video_count")) \
                    .orderBy(col("published_date").desc()) \
                    .limit(10)

print("Dernières 10 dates:")
timeline_pd = timeline.toPandas()
for _, row in timeline_pd.iterrows():
    print(f"  {row['published_date']}: {row['video_count']} vidéos")

# 4. KEYWORD EXTRACTION using Spark transformations
print(f"\n4.  MOTS-CLÉS DANS LES TITRES (Normalisés)")

# Import utils functions locally to avoid serialization issues
import utils
stop_words_local = utils.get_stop_words()

def extract_keywords_from_title(title):
    """Extract and normalize keywords from title - standalone for Spark"""
    if not title:
        return []
    
    import re
    
    # Inline stop words for Spark worker
    stop_words = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
        'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
        'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him',
        'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some',
        'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look',
        'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after',
        'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even',
        'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
        'video', 'news', 'latest', 'live', 'watch', 'full', 'today', 'update',
        'breaking', 'vs', 'exclusive', 'special', 'report', 'official'
    }
    
    # Simple normalize function (inline)
    def normalize_word(word):
        # Lowercase and remove special chars
        word = word.lower().strip()
        word = re.sub(r'[^a-z]', '', word)
        if not word:
            return None
        # Simple stemming
        if word.endswith('ing'):
            word = word[:-3]
        elif word.endswith('ed'):
            word = word[:-2]
        elif word.endswith('s') and len(word) > 3:
            word = word[:-1]
        # Semantic mappings
        mappings = {
            'palestinian': 'palestine',
            'israeli': 'israel',
            'gazans': 'gaza'
        }
        return mappings.get(word, word)
    
    # Remove hashtags
    title = re.sub(r'#\w+', '', title)
    
    # Tokenize and clean
    words = re.findall(r'\b\w+\b', title.lower())
    
    # Filter and normalize
    keywords = []
    for word in words:
        if len(word) > 2 and word not in stop_words:
            normalized = normalize_word(word)
            if normalized and len(normalized) > 2:
                keywords.append(normalized)
    
    return keywords

# Register UDF
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType

extract_keywords_udf = udf(extract_keywords_from_title, ArrayType(StringType()))

# Apply keyword extraction
df_with_keywords = df_videos.withColumn("keywords", extract_keywords_udf(col("title")))

# Explode and count keywords
keyword_counts = df_with_keywords.select(explode(col("keywords")).alias("keyword")) \
                                  .groupBy("keyword") \
                                  .agg(count("*").alias("count")) \
                                  .orderBy(col("count").desc()) \
                                  .limit(15)

print("Mots les plus fréquents dans les titres:")
for row in keyword_counts.collect():
    print(f"   {row['keyword']}: {row['count']}")

# 5. TOP 10 MOST VIEWED VIDEOS
print(f"\n5.  TOP 10 VIDÉOS LES PLUS VUES")
top_videos = df_videos.select("viewCount", "channelTitle", "title") \
                      .orderBy(col("viewCount").desc()) \
                      .limit(10)

for video in top_videos.collect():
    print(f"   {video['viewCount']} vues - {video['channelTitle']}: {video['title'][:70]}...")

# 6. COMMENT ANALYSIS
print(f"\n6.  ANALYSE DES COMMENTAIRES (Filtrés Anglais)")
print(f"   - Commentaires totaux: {comment_count}")

# Most active authors
df_comments.createOrReplaceTempView("comments")
top_authors = spark.sql("""
    SELECT author, COUNT(*) as comment_count
    FROM comments
    GROUP BY author
    ORDER BY comment_count DESC
    LIMIT 10
""")

print("   - Auteurs les plus actifs:")
for row in top_authors.collect():
    print(f"     {row['author']}: {row['comment_count']} commentaires")

# Most liked comments
top_liked = df_comments.select("author", "text", "likeCount") \
                       .orderBy(col("likeCount").desc()) \
                       .limit(5)

print("   - Commentaires les plus likés:")
for row in top_liked.collect():
    text_preview = row['text'][:80] if row['text'] else ""
    print(f"     {row['likeCount']} likes - @{row['author']}: {text_preview}...")

# 7. ANALYSIS BY QUERY KEYWORD
print(f"\n7.  ANALYSE PAR MOT-CLÉ DE RECHERCHE")
query_stats = df_videos.groupBy("query") \
                       .agg(
                           count("*").alias("nb_videos"),
                           spark_sum("viewCount").alias("total_views"),
                           spark_sum("likeCount").alias("total_likes")
                       ) \
                       .orderBy("nb_videos", ascending=False)

query_stats_pd = query_stats.toPandas()
print(query_stats_pd.to_string(index=False))

# SAVE RESULTS TO CSV (pandas for compatibility with existing pipeline)
print(f"\n Analyse PySpark terminée avec succès!")
print(f" Fichiers sauvegardés dans outputs/")

# Convert necessary dataframes to pandas and save
top_channels_pd.to_csv('outputs/analysis_videos_pyspark.csv', index=False)

# Save comments analysis
comments_analysis = df_comments.select("videoId", "commentId", "author", "text", "likeCount", "publishedAt") \
                               .toPandas()
comments_analysis.to_csv('outputs/analysis_comments_pyspark.csv', index=False)

# Stop Spark session
spark.stop()
