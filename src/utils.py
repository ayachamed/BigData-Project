"""Utility functions for YouTube Big Data pipeline."""

import re

# =============================================================================
# LANGUAGE DETECTION
# =============================================================================

def is_english(text):
    """Check if text is likely English using ASCII ratio and stop words."""
    if not text:
        return False
        
    # Remove URLs, mentions, hashtags
    text_content = re.sub(r'http\S+|@\S+|#\S+', '', text)
    if not text_content.strip():
        return False

    # Check ASCII ratio (allow some emojis)
    ascii_chars = sum(1 for c in text_content if ord(c) < 128)
    ascii_ratio = ascii_chars / len(text_content) if text_content else 0
    
    if ascii_ratio < 0.8:
        return False
        
    # Check for English stop words (for longer text)
    words = text_content.lower().split()
    if len(words) > 3:
        common_words = {'the', 'and', 'is', 'to', 'in', 'of', 'it', 'that'}
        if not any(w in common_words for w in words):
            return False
    elif len(words) > 0 and ascii_ratio < 1.0:
        return False
                  
    return True


# =============================================================================
# KEYWORD NORMALIZATION
# =============================================================================

SEMANTIC_MAPPINGS = {
    'palestinians': 'palestine',
    'palestinian': 'palestine',
    'gazans': 'gaza',
    'israelis': 'israel',
    'israeli': 'israel',
}

def normalize_keyword(word):
    """Normalize keyword: lowercase, stem, and map semantically."""
    word = word.lower().strip()
    word = re.sub(r'[^\w\s]', '', word)  # Remove punctuation
    
    # Apply semantic mappings
    if word in SEMANTIC_MAPPINGS:
        return SEMANTIC_MAPPINGS[word]
        
    # Simple stemming
    if word.endswith('ing'):
        return word[:-3]
    if word.endswith('ies') and len(word) > 4:
        return word[:-3] + 'y'
    if word.endswith('s') and not word.endswith('ss') and len(word) > 3:
        return word[:-1]
    if word.endswith('ed') and len(word) > 4:
        return word[:-2]
          
    return word


def extract_keywords(title):
    """
    Extract and normalize keywords from title.
    PySpark-compatible (no external dependencies).
    """
    if not title:
        return []
    
    # Remove hashtags
    title = re.sub(r'#\w+', '', title)
    
    # Tokenize
    words = re.findall(r'\b\w+\b', title.lower())
    
    # Filter and normalize
    keywords = []
    stop_words = get_stop_words()
    
    for word in words:
        if len(word) > 2 and word not in stop_words:
            normalized = normalize_keyword(word)
            if normalized and len(normalized) > 2:
                keywords.append(normalized)
    
    return keywords


# =============================================================================
# STOP WORDS
# =============================================================================

def get_stop_words():
    """Return common English stop words and noise terms."""
    return {
        # Common English
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
        # YouTube/News noise
        'video', 'news', 'latest', 'live', 'watch', 'full', 'today', 'update',
        'breaking', 'vs', 'exclusive', 'special', 'report', 'official'
    }


# =============================================================================
# DURATION PARSING
# =============================================================================

def parse_duration(duration_str):
    """Parse ISO 8601 duration (e.g., PT1H2M10S) to seconds."""
    if not duration_str:
        return 0
        
    duration_str = duration_str.replace('PT', '')
    
    hours = minutes = seconds = 0
    
    if 'H' in duration_str:
        parts = duration_str.split('H')
        hours = int(parts[0])
        duration_str = parts[1]
        
    if 'M' in duration_str:
        parts = duration_str.split('M')
        minutes = int(parts[0])
        duration_str = parts[1]
        
    if 'S' in duration_str:
        seconds = int(duration_str.split('S')[0])
        
    return hours * 3600 + minutes * 60 + seconds
