import re
from typing import List, Set


def tokenize(text: str) -> List[str]:
    """Split text into individual words (tokens)"""
    # Convert to lowercase and split by whitespace and punctuation
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens


def normalize(tokens: List[str]) -> List[str]:
    """Normalize tokens (already lowercased in tokenize)"""
    return tokens


def remove_stop_words(tokens: List[str]) -> List[str]:
    """Remove common stop words that don't add meaning"""
    stop_words: Set[str] = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have', 'had',
        'what', 'when', 'where', 'who', 'which', 'why', 'how'
    }
    
    return [token for token in tokens if token not in stop_words]


def process_text(text: str) -> List[str]:
    """Process text: tokenize, normalize, and remove stop words"""
    tokens = tokenize(text)
    tokens = normalize(tokens)
    tokens = remove_stop_words(tokens)
    return tokens


def get_unique_terms(text: str) -> Set[str]:
    """Get unique terms from text"""
    tokens = process_text(text)
    return set(tokens)
