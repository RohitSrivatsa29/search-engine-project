"""
Debug search service error locally
"""
import asyncio
from mongodb import connect_db, close_db
from search_service import SearchService
import traceback

async def debug_search():
    print("Debugging Search Service...")
    await connect_db()
    
    try:
        query = "python"
        print(f"Searching for: '{query}'")
        
        # Call search service directly
        results = await SearchService.search(query, page=1, limit=10)
        
        print(f"✅ Search successful!")
        print(f"Total results: {results['total_results']}")
        for doc in results['results']:
            print(f"- {doc['title']} (Score: {doc['relevance_score']:.4f})")
            
    except Exception as e:
        print(f"Search failed: {type(e).__name__}: {e}")
        import sys
        traceback.print_exc(file=sys.stdout)
    
    await close_db()

if __name__ == "__main__":
    asyncio.run(debug_search())
