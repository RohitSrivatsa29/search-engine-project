"""
Enhanced search service with fuzzy matching and auto-correct
"""
from mongodb import get_database
from text_processing import process_text
from ranking_service import RankingService
from typing import List, Dict
from bson import ObjectId

class SearchService:
    """Service for searching documents with fuzzy matching"""
    
    @staticmethod
    def calculate_similarity(word1: str, word2: str) -> float:
        """Calculate similarity between two words using Levenshtein distance"""
        if word1 == word2:
            return 1.0
        
        # Simple similarity based on common characters
        len1, len2 = len(word1), len(word2)
        if len1 == 0 or len2 == 0:
            return 0.0
        
        # Count matching characters
        matches = sum(1 for c in word1 if c in word2)
        max_len = max(len1, len2)
        
        return matches / max_len
    
    @staticmethod
    async def expand_query_with_fuzzy_match(query_terms: List[str], threshold: float = 0.7) -> List[str]:
        """Expand query terms with similar terms from the index"""
        db = get_database()
        expanded_terms = set(query_terms)
        
        # Get all unique terms from the index
        index_terms = await db.inverted_index.distinct("term")
        
        for query_term in query_terms:
            for index_term in index_terms:
                similarity = SearchService.calculate_similarity(query_term.lower(), index_term.lower())
                if similarity >= threshold and index_term not in expanded_terms:
                    expanded_terms.add(index_term)
        
        return list(expanded_terms)
    
    @staticmethod
    async def search(query: str, page: int = 1, limit: int = 10, use_fuzzy: bool = True) -> Dict:
        """
        Search for documents matching the query with fuzzy matching
        
        Args:
            query: Search query string
            page: Page number (1-indexed)
            limit: Number of results per page
            use_fuzzy: Enable fuzzy matching for typo tolerance
        
        Returns:
            Dictionary with search results and metadata
        """
        db = get_database()
        
        # Process query
        query_terms = process_text(query)
        
        if not query_terms:
            return {
                "query": query,
                "total_results": 0,
                "page": page,
                "limit": limit,
                "results": []
            }
        
        # Expand query with fuzzy matching if enabled
        if use_fuzzy:
            query_terms = await SearchService.expand_query_with_fuzzy_match(query_terms)
        
        # Find documents containing any of the query terms
        matching_doc_ids = set()
        
        for term in query_terms:
            # Find documents in inverted index
            index_entry = await db.inverted_index.find_one({"term": term})
            if index_entry:
                matching_doc_ids.update(index_entry.get("doc_ids", []))
        
        if not matching_doc_ids:
            return {
                "query": query,
                "total_results": 0,
                "page": page,
                "limit": limit,
                "results": []
            }
        
        # Get document details
        documents = []
        documents = []
        for doc_id in matching_doc_ids:
            try:
                # Convert string ID to ObjectId for lookup
                doc = await db.documents.find_one({"_id": ObjectId(doc_id)})
                if doc:
                    doc["_id"] = str(doc["_id"])
                    documents.append(doc)
            except Exception:
                # Skip invalid IDs or other errors
                continue
        
        # Rank documents by relevance
        ranked_docs = await RankingService.rank_documents(documents, query_terms)
        
        # Pagination
        total_results = len(ranked_docs)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_results = ranked_docs[start_idx:end_idx]
        
        return {
            "query": query,
            "total_results": total_results,
            "page": page,
            "limit": limit,
            "results": paginated_results
        }
