"""
Test server startup sequence
"""
import asyncio
from mongodb import connect_db, close_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_startup():
    print("🚀 Testing MongoDB connection startup...")
    try:
        await connect_db()
        print("✅ Startup routine completed successfully!")
        await close_db()
    except Exception as e:
        print(f"❌ Startup failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_startup())
