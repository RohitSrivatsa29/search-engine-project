from fastapi import APIRouter, Depends, status, Query
from auth_middleware import get_current_user
from document_service import DocumentService
from document import DocumentCreate, DocumentUpdate, DocumentResponse
from user import User
from typing import List

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    doc_data: DocumentCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new document"""
    doc = await DocumentService.create_document(doc_data, current_user.id)
    return doc


@router.get("", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """Get all documents for the current user"""
    docs = await DocumentService.get_user_documents(current_user.id, skip, limit)
    return docs


@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(
    doc_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific document"""
    doc = await DocumentService.get_document(doc_id, current_user.id)
    return doc


@router.put("/{doc_id}", response_model=DocumentResponse)
async def update_document(
    doc_id: str,
    doc_data: DocumentUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a document"""
    doc = await DocumentService.update_document(doc_id, doc_data, current_user.id)
    return doc


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    doc_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a document"""
    await DocumentService.delete_document(doc_id, current_user.id)
