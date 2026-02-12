from mongodb import get_database
from text_processing import process_text, get_unique_terms
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class IndexingService:
    """Service for building and maintaining inverted index"""
    
    @staticmethod
    async def build_index_for_document(doc_id: str, title: str, content: str):
        """Build inverted index entries for a document"""
        db = get_database()
        
        # Combine title and content for indexing (title gets more weight)
        full_text = f"{title} {title} {content}"  # Title appears twice for higher weight
        
        # Get unique terms
        terms = get_unique_terms(full_text)
        
        # Update inverted index for each term
        for term in terms:
            await db.inverted_index.update_one(
                {"term": term},
                {
                    "$addToSet": {"doc_ids": doc_id},
                    "$inc": {"doc_count": 0}  # Will be set correctly below
                },
                upsert=True
            )
        
        # Update document counts
        for term in terms:
            result = await db.inverted_index.find_one({"term": term})
            if result:
                doc_count = len(result.get("doc_ids", []))
                await db.inverted_index.update_one(
                    {"term": term},
                    {"$set": {"doc_count": doc_count}}
                )
        
        logger.info(f"✅ Indexed document {doc_id} with {len(terms)} unique terms")
    
    @staticmethod
    async def remove_document_from_index(doc_id: str):
        """Remove a document from the inverted index"""
        db = get_database()
        
        # Remove doc_id from all index entries
        await db.inverted_index.update_many(
            {"doc_ids": doc_id},
            {"$pull": {"doc_ids": doc_id}}
        )
        
        # Update document counts and remove empty entries
        await db.inverted_index.delete_many({"doc_ids": {"$size": 0}})
        
        # Update doc_count for remaining entries
        cursor = db.inverted_index.find({})
        async for entry in cursor:
            doc_count = len(entry.get("doc_ids", []))
            await db.inverted_index.update_one(
                {"_id": entry["_id"]},
                {"$set": {"doc_count": doc_count}}
            )
        
        logger.info(f"✅ Removed document {doc_id} from index")
    
    @staticmethod
    async def get_documents_for_term(term: str) -> List[str]:
        """Get list of document IDs containing a term"""
        db = get_database()
        
        result = await db.inverted_index.find_one({"term": term.lower()})
        
        if result:
            return result.get("doc_ids", [])
        return []
    
    @staticmethod
    async def rebuild_entire_index():
        """Rebuild the entire inverted index from scratch"""
        db = get_database()
        
        # Clear existing index
        await db.inverted_index.delete_many({})
        
        # Rebuild from all documents
        cursor = db.documents.find({})
        count = 0
        
        async for doc in cursor:
            doc_id = str(doc["_id"])
            title = doc.get("title", "")
            content = doc.get("content", "")
            
            await IndexingService.build_index_for_document(doc_id, title, content)
            count += 1
        
        logger.info(f"✅ Rebuilt entire index for {count} documents")
        return count
