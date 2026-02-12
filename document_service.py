from mongodb import get_database
from document import Document, DocumentCreate, DocumentUpdate
from indexing_service import IndexingService
from fastapi import HTTPException, status
from bson import ObjectId
from typing import List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document CRUD operations"""
    
    @staticmethod
    async def create_document(doc_data: DocumentCreate, author_id: str) -> Document:
        """Create a new document and index it"""
        db = get_database()
        
        # Create document
        doc = Document(
            title=doc_data.title,
            content=doc_data.content,
            author_id=author_id
        )
        
        # Insert into database
        result = await db.documents.insert_one(doc.model_dump(by_alias=True, exclude={"id"}))
        doc_id = str(result.inserted_id)
        doc.id = doc_id
        
        # Build index for this document
        await IndexingService.build_index_for_document(doc_id, doc.title, doc.content)
        
        logger.info(f"✅ Created document {doc_id}")
        return doc
    
    @staticmethod
    async def get_document(doc_id: str, user_id: str) -> Document:
        """Get a specific document"""
        db = get_database()
        
        try:
            doc = await db.documents.find_one({"_id": ObjectId(doc_id)})
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid document ID"
            )
        
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Check ownership
        if doc["author_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this document"
            )
        
        doc["_id"] = str(doc["_id"])
        return Document(**doc)
    
    @staticmethod
    async def get_user_documents(user_id: str, skip: int = 0, limit: int = 10) -> List[Document]:
        """Get all documents for a user"""
        db = get_database()
        
        cursor = db.documents.find({"author_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
        
        documents = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            documents.append(Document(**doc))
        
        return documents
    
    @staticmethod
    async def update_document(doc_id: str, doc_data: DocumentUpdate, user_id: str) -> Document:
        """Update a document and re-index it"""
        db = get_database()
        
        # Get existing document
        doc = await DocumentService.get_document(doc_id, user_id)
        
        # Prepare update data
        update_data = {}
        if doc_data.title is not None:
            update_data["title"] = doc_data.title
        if doc_data.content is not None:
            update_data["content"] = doc_data.content
        
        if not update_data:
            return doc
        
        update_data["updated_at"] = datetime.utcnow()
        
        # Update document
        await db.documents.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": update_data}
        )
        
        # Re-index document
        updated_doc = await db.documents.find_one({"_id": ObjectId(doc_id)})
        await IndexingService.remove_document_from_index(doc_id)
        await IndexingService.build_index_for_document(
            doc_id,
            updated_doc["title"],
            updated_doc["content"]
        )
        
        updated_doc["_id"] = str(updated_doc["_id"])
        logger.info(f"✅ Updated document {doc_id}")
        return Document(**updated_doc)
    
    @staticmethod
    async def delete_document(doc_id: str, user_id: str):
        """Delete a document and remove from index"""
        db = get_database()
        
        # Verify ownership
        await DocumentService.get_document(doc_id, user_id)
        
        # Remove from index
        await IndexingService.remove_document_from_index(doc_id)
        
        # Delete document
        await db.documents.delete_one({"_id": ObjectId(doc_id)})
        
        logger.info(f"✅ Deleted document {doc_id}")
