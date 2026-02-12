from mongodb import get_database
from text_processing import process_text
from typing import List, Dict
import math
import logging

logger = logging.getLogger(__name__)


class RankingService:
    """Service for ranking search results using TF-IDF"""
    
    @staticmethod
    def calculate_tf(term: str, doc: Dict) -> float:
        """Calculate Term Frequency (TF) for a term in a document"""
        # Combine title and content (title appears twice for higher weight)
        full_text = f"{doc.get('title', '')} {doc.get('title', '')} {doc.get('content', '')}"
        tokens = process_text(full_text)
        
        if not tokens:
            return 0.0
        
        # Count occurrences of term
        term_count = tokens.count(term.lower())
        total_terms = len(tokens)
        
        if total_terms == 0:
            return 0.0
        
        # TF = (count of term) / (total terms in document)
        tf = term_count / total_terms
        return tf
    
    @staticmethod
    async def calculate_idf(term: str) -> float:
        """Calculate Inverse Document Frequency (IDF) for a term"""
        db = get_database()
        
        # Get total number of documents
        total_docs = await db.documents.count_documents({})
        
        if total_docs == 0:
            return 0.0
        
        # Get number of documents containing the term
        index_entry = await db.inverted_index.find_one({"term": term.lower()})
        
        if not index_entry:
            return 0.0
        
        docs_with_term = index_entry.get("doc_count", 0)
        
        if docs_with_term == 0:
            return 0.0
        
        # IDF = log(total documents / documents with term)
        idf = math.log(total_docs / docs_with_term)
        return idf
    
    @staticmethod
    async def calculate_tfidf(term: str, doc: Dict) -> float:
        """Calculate TF-IDF score for a term in a document"""
        tf = RankingService.calculate_tf(term, doc)
        idf = await RankingService.calculate_idf(term)
        
        tfidf = tf * idf
        return tfidf
    
    @staticmethod
    async def rank_documents(documents: List[Dict], query_terms: List[str]) -> List[Dict]:
        """Rank documents by relevance to query using TF-IDF"""
        
        # Calculate scores for each document
        ranked_docs = []
        
        for doc in documents:
            total_score = 0.0
            
            # Sum TF-IDF scores for all query terms
            for term in query_terms:
                tfidf = await RankingService.calculate_tfidf(term, doc)
                total_score += tfidf
            
            # Add score to document
            doc["relevance_score"] = round(total_score, 4)
            ranked_docs.append(doc)
        
        # Sort documents by score (highest first)
        ranked_docs.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return ranked_docs
