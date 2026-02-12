from fastapi import APIRouter, Query
from search_service import SearchService
from typing import Dict

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("", response_model=Dict)
async def search_documents(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Results per page")
):
    """
    Search for documents matching the query.
    
    Returns documents ranked by relevance using TF-IDF algorithm.
    """
    results = await SearchService.search(q, page, limit)
    return results
