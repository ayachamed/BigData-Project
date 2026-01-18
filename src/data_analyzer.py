"""PySpark-based YouTube data analyzer for big data processing."""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, mean, to_date,
    explode, udf
)
from pyspark.sql.types import StringType, ArrayType
import re

# Initialize Spark
spark = SparkSession.builder \
    .appName("YouTubeGazaAnalysis") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

print("=== ANALYSE DES VIDÉOS YOUTUBE SUR GAZA (PySpark) ===\n")

# =============================================================================
# DATA LOADING
# =============================================================================

try:
    import pandas as pd_loader
    pd_videos = pd_loader.read_json('data/youtube_videos.json')
    pd_comments = pd_loader.read_json('data/youtube_comments.json')
    
    df_videos = spark.createDataFrame(pd_videos)
    df_comments = spark.createDataFrame(pd_comments)
    
    print("✓ Data loaded successfully\n")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Run data_collector.py first!")
    spark.stop()
    exit()


# =============================================================================
# 1. GENERAL STATISTICS
# =============================================================================

print("1. STATISTIQUES GÉNÉRALES")

video_count = df_videos.count()
comment_count = df_comments.count()
print(f"   - Vidéos: {video_count}")
print(f"   - Commentaires: {comment_count}")

# Calculate means
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


# =============================================================================
# 2. TOP CHANNELS (Spark SQL)
# =============================================================================

print("\n2. TOP 10 DES CHAÎNES")

df_videos.createOrReplaceTempView("videos")

top_channels = spark.sql("""
    SELECT channelTitle,
           COUNT(*) as nb_videos,
           SUM(viewCount) as total_views,
           SUM(likeCount) as total_likes
    FROM videos
    GROUP BY channelTitle
    ORDER BY nb_videos DESC
    LIMIT 10
""")

print(top_channels.toPandas().to_string(index=False))


# =============================================================================
# 3. TEMPORAL EVOLUTION
# =============================================================================

print("\n3. ÉVOLUTION TEMPORELLE")

timeline = df_videos.withColumn("published_date", to_date(col("publishedAt"))) \
                    .groupBy("published_date") \
                    .agg(count("*").alias("video_count")) \
                    .orderBy(col("published_date").desc()) \
                    .limit(10)

print("Dernières 10 dates:")
for row in timeline.collect():
    print(f"  {row['published_date']}: {row['video_count']} vidéos")


# =============================================================================  
# 4. KEYWORD EXTRACTION
# =============================================================================

print("\n4. MOTS-CLÉS DANS LES TITRES (Normalisés)")

def extract_keywords(title):
    """Extract keywords from title - simple and clean."""
    if not title:
        return []
    
    import re
    
    # Stop words
    stops = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
        'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which',
        'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him',
        'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some',
        'video', 'news', 'latest', 'live', 'watch', 'full', 'today'
    }
    
    # Clean title
    title = re.sub(r'#\w+', '', title)  # Remove hashtags
    words = re.findall(r'\b\w+\b', title.lower())
    
    # Filter and normalize
    keywords = []
    for word in words:
        # Filter short words and stop words
        if len(word) <= 2 or word in stops:
            continue
        
        # Simple stemming
        if word.endswith('ing'):
            word = word[:-3]
        elif word.endswith('s') and len(word) > 3:
            word = word[:-1]
        
        # Semantic mappings
        if word in ('palestinian', 'palestinians'):
            word = 'palestine'
        elif word in ('israeli', 'israelis'):
            word = 'israel'
        
        if len(word) > 2:
            keywords.append(word)
    
    return keywords

# Apply UDF
extract_keywords_udf = udf(extract_keywords, ArrayType(StringType()))

keyword_counts = df_videos.withColumn("keywords", extract_keywords_udf(col("title"))) \
                         .select(explode(col("keywords")).alias("keyword")) \
                         .groupBy("keyword") \
                         .agg(count("*").alias("count")) \
                         .orderBy(col("count").desc()) \
                         .limit(15)

print("Mots les plus fréquents:")
for row in keyword_counts.collect():
    print(f"   {row['keyword']}: {row['count']}")


# =============================================================================
# 5. TOP VIDEOS
# =============================================================================

print("\n5. TOP 10 VIDÉOS LES PLUS VUES")

top_videos = df_videos.select("viewCount", "channelTitle", "title") \
                      .orderBy(col("viewCount").desc()) \
                      .limit(10)

for video in top_videos.collect():
    title_preview = video['title'][:70] + "..." if len(video['title']) > 70 else video['title']
    print(f"   {video['viewCount']:,} vues - {video['channelTitle']}: {title_preview}")


# =============================================================================
# 6. COMMENT ANALYSIS
# =============================================================================

print("\n6. ANALYSE DES COMMENTAIRES")
print(f"   - Total: {comment_count}")

# Top authors
df_comments.createOrReplaceTempView("comments")
top_authors = spark.sql("""
    SELECT author, COUNT(*) as count
    FROM comments
    GROUP BY author
    ORDER BY count DESC
    LIMIT 10
""")

print("   - Auteurs les plus actifs:")
for row in top_authors.collect():
    print(f"     {row['author']}: {row['count']} commentaires")

# Most liked
top_liked = df_comments.orderBy(col("likeCount").desc()).limit(5)

print("   - Commentaires les plus likés:")
for row in top_liked.collect():
    text_preview = (row['text'][:80] + "...") if row['text'] and len(row['text']) > 80 else row['text']
    print(f"     {row['likeCount']:,} likes - @{row['author']}: {text_preview}")


# =============================================================================
# 7. ANALYSIS BY QUERY
# =============================================================================

print("\n7. ANALYSE PAR MOT-CLÉ DE RECHERCHE")

query_stats = df_videos.groupBy("query") \
                       .agg(
                           count("*").alias("nb_videos"),
                           spark_sum("viewCount").alias("total_views"),
                           spark_sum("likeCount").alias("total_likes")
                       ) \
                       .orderBy("nb_videos", ascending=False)

print(query_stats.toPandas().to_string(index=False))


# =============================================================================
# SAVE RESULTS
# =============================================================================

print("\n✓ Analyse PySpark terminée avec succès!")
print("✓ Fichiers sauvegardés dans outputs/")

# Convert to pandas for CSV compatibility
top_channels.toPandas().to_csv('outputs/analysis_videos_pyspark.csv', index=False)
df_comments.select("videoId", "commentId", "author", "text", "likeCount", "publishedAt") \
          .toPandas() \
          .to_csv('outputs/analysis_comments_pyspark.csv', index=False)

# Stop Spark
spark.stop()
