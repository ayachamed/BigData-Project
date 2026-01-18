import re
import math

def is_english(text):
    """
    Heuristic to check if text is English.
    Checks if a significant portion of the text consists of ASCII characters
    and common English stop words.
    """
    if not text:
        return False
        
    # Remove URLs, mentions, hashtags for language detection
    text_content = re.sub(r'http\S+|@\S+|#\S+', '', text)
    if not text_content.strip():
        return False

    # Check ASCII ratio
    ascii_chars = sum(1 for c in text_content if ord(c) < 128)
    ascii_ratio = ascii_chars / len(text_content) if len(text_content) > 0 else 0
    
    if ascii_ratio < 0.8:  # Allow some non-ASCII (emojis, etc.)
        return False
        
    # Check for common English stop words (if text is long enough)
    words = text_content.lower().split()
    if len(words) > 3:
        common_words = {'the', 'and', 'is', 'to', 'in', 'of', 'it', 'that', 'for', 'you', 'with', 'on', 'are', 'as', 'be', 'this', 'have', 'not'}
        if not any(w in common_words for w in words):
             return False
    elif len(words) > 0:
        # For very short sentences, trust ASCII but require high ratio
        if ascii_ratio < 1.0: # Short text must be purely ASCII to be safe
            return False
                 
    return True

def normalize_keyword(word):
    """
    Normalize keywords:
    - Lowercase
    - Remove common suffixes (simple stemming)
    - Map specific terms to roots
    - Remove special characters
    """
    word = word.lower().strip()
    word = re.sub(r'[^\w\s]', '', word) # Remove punctuation
    
    # Specific mappings
    mappings = {
        'palestinians': 'palestine',
        'palestinian': 'palestine',
        'gazans': 'gaza',
        'israelis': 'israel',
        'israeli': 'israel',
        'hamas': 'hamas', # Keep specific names
    }
    
    if word in mappings:
        return mappings[word]
        
    # Simple stemming for English plurals/suffixes
    # Very basic rules to avoid over-stemming
    if word.endswith('ing'):
        return word[:-3]
    if word.endswith('ies') and len(word) > 4:
         return word[:-3] + 'y'
    if word.endswith('s') and not word.endswith('ss') and len(word) > 3:
        return word[:-1]
    if word.endswith('ed') and len(word) > 4:
         return word[:-2]
         
    return word

def parse_duration(duration_str):
    """
    Parse ISO 8601 duration string (e.g., PT1H2M10S) to seconds.
    """
    if not duration_str:
        return 0
        
    duration_str = duration_str.replace('PT', '')
    
    hours = 0
    minutes = 0
    seconds = 0
    
    if 'H' in duration_str:
        parts = duration_str.split('H')
        hours = int(parts[0])
        duration_str = parts[1]
        
    if 'M' in duration_str:
        parts = duration_str.split('M')
        minutes = int(parts[0])
        duration_str = parts[1]
        
    if 'S' in duration_str:
        parts = duration_str.split('S')
        seconds = int(parts[0])
        
    return hours * 3600 + minutes * 60 + seconds

def get_stop_words():
    """Return a set of common English stop words."""
    return {
        'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have', 'has', 'was', 'were', 
        'are', 'you', 'your', 'about', 'their', 'what', 'who', 'how', 'when', 'where', 'why',
        'will', 'would', 'could', 'should', 'can', 'may', 'its', 'our', 'been', 'being',
        'into', 'more', 'some', 'than', 'then', 'just', 'over', 'time', 'only', 'very',
        'also', 'even', 'most', 'after', 'before', 'because', 'while', 'since', 'them',
        'these', 'those', 'such', 'much', 'many', 'between', 'during', 'through'
    }
