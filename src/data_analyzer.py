import pandas as pd
import json
from datetime import datetime
import re
from collections import Counter
import utils

print("=== ANALYSE DES VIDÉOS YOUTUBE SUR GAZA (Pandas) ===")

# Charger les données
try:
    with open('data/youtube_videos.json', 'r', encoding='utf-8') as f:
        videos_data = json.load(f)

    with open('data/youtube_comments.json', 'r', encoding='utf-8') as f:
        comments_data = json.load(f)
except FileNotFoundError:
    print("Files not found! Run data_collector.py first.")
    exit()

df_videos = pd.DataFrame(videos_data)
df_comments = pd.DataFrame(comments_data)

print(f"\n1.  STATISTIQUES GÉNÉRALES")
print(f"   - Vidéos collectées: {len(df_videos)}")
print(f"   - Commentaires collectés: {len(df_comments)}")

# Convertir les colonnes numériques
df_videos['viewCount'] = pd.to_numeric(df_videos['viewCount'], errors='coerce').fillna(0)
df_videos['likeCount'] = pd.to_numeric(df_videos['likeCount'], errors='coerce').fillna(0)
df_videos['commentCount'] = pd.to_numeric(df_videos['commentCount'], errors='coerce').fillna(0)

print(f"   - Vues moyennes: {df_videos['viewCount'].mean():.0f}")
print(f"   - Likes moyens: {df_videos['likeCount'].mean():.0f}")
print(f"   - Commentaires moyens: {df_videos['commentCount'].mean():.0f}")

print(f"\n2.  TOP 10 DES CHAÎNES")
top_channels = df_videos.groupby('channelTitle').agg({
    'videoId': 'count',
    'viewCount': 'sum',
    'likeCount': 'sum'
}).rename(columns={'videoId': 'nb_videos', 'viewCount': 'total_views', 'likeCount': 'total_likes'})

top_channels = top_channels.sort_values('nb_videos', ascending=False).head(10)
print(top_channels)

print(f"\n3.  ÉVOLUTION TEMPORELLE")
df_videos['published_date'] = pd.to_datetime(df_videos['publishedAt']).dt.date
timeline = df_videos.groupby('published_date').size()
print("Dernières 10 dates:")
print(timeline.tail(10))

print(f"\n4.  MOTS-CLÉS DANS LES TITRES (Normalisés)")
# Keyword Extraction Pipeline
all_titles = ' '.join(df_videos['title']).lower()

# 1. Remove hashtags entirely
all_titles = re.sub(r'#\w+', '', all_titles)

all_words = all_titles.split()

# 2. Get stopwords and normalize
stop_words = utils.get_stop_words()
stop_words.add('video') # Add specific noise word if needed

normalized_words = []
for word in all_words:
    if len(word) > 3 and word not in stop_words:
        # Normalize (clean punct, mapping, stemming)
        norm_word = utils.normalize_keyword(word)
        if norm_word and len(norm_word) > 3 and norm_word not in stop_words:
            normalized_words.append(norm_word)

word_counts = Counter(normalized_words)
print("Mots les plus fréquents dans les titres:")
for word, count in word_counts.most_common(15):
    print(f"   {word}: {count}")

print(f"\n5.  TOP 10 VIDÉOS LES PLUS VUES")
top_videos = df_videos.nlargest(10, 'viewCount')[['channelTitle', 'title', 'viewCount', 'likeCount', 'commentCount']]
for idx, row in top_videos.iterrows():
    print(f"   {row['viewCount']} vues - {row['channelTitle']}: {row['title'][:60]}...")

if len(df_comments) > 0:
    print(f"\n6.  ANALYSE DES COMMENTAIRES (Filtrés Anglais)")
    print(f"   - Commentaires totaux: {len(df_comments)}")
    
    # Convertir les likes des commentaires
    df_comments['likeCount'] = pd.to_numeric(df_comments['likeCount'], errors='coerce').fillna(0)
    
    # Double check filtering just in case (though collector does it)
    # Could imply stricter filtering here if needed, but we trust collector for now.
    
    top_authors = df_comments['author'].value_counts().head(10)
    print("   - Auteurs les plus actifs:")
    for author, count in top_authors.items():
        print(f"     {author}: {count} commentaires")
    
    top_comments = df_comments.nlargest(5, 'likeCount')[['author', 'text', 'likeCount']]
    print("   - Commentaires les plus likés:")
    for idx, row in top_comments.iterrows():
        print(f"     {row['likeCount']} likes - {row['author']}: {row['text'][:80]}...")

# 7. Analyse par requête de recherche
print(f"\n7.  ANALYSE PAR MOT-CLÉ DE RECHERCHE")
query_analysis = df_videos.groupby('query').agg({
    'videoId': 'count',
    'viewCount': 'sum',
    'likeCount': 'sum'
}).rename(columns={'videoId': 'nb_videos', 'viewCount': 'total_views', 'likeCount': 'total_likes'})
print(query_analysis)

# Sauvegarder les résultats
df_videos.to_csv('outputs/analysis_videos_pandas.csv', index=False)
if len(df_comments) > 0:
    df_comments.to_csv('outputs/analysis_comments_pandas.csv', index=False)
print(f"\n Analyse Pandas terminée avec succès!")
print(f" Fichiers sauvegardés dans outputs/")
