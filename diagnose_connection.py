import asyncio
import sys
import os
import pymongo
from pymongo.errors import AutoReconnect, ServerSelectionTimeoutError
from mongodb import connect_db, close_db, get_database

async def diagnose_connection():
    print("🔍 DIAGNOSTIC STARTING...")
    print(f"python version: {sys.version}")
    
    print("\n1. 🔐 Testing Application Connection Logic...")
    try:
        await connect_db()
        print("   ✅ connect_db() function executed successfully")
        
        db = get_database()
        print("   ✅ get_database() returned database object")
        
        # Force a server call
        print("   ... Pinging database ...")
        await db.command('ping')
        print("   ✅ MongoDB Handshake Successful!")
        
        # Check database access
        print(f"   ... Checking access to collections ...")
        collections = await db.list_collection_names()
        print(f"   ✅ Collections found: {collections}")
        
        count = await db.documents.count_documents({})
        print(f"   ✅ Documents accessible! (Found {count} documents)")
        
        await close_db()
        
    except Exception as e:
        print(f"   ❌ CONNECTION FAILED: {type(e).__name__}")
        print(f"   Detailed: {e}")
        print("   ------------------------------------------------")
        print("   👉 If this fails, the issue is strictly network or auth.")
        return

    print("\n✅ DIAGNOSTIC COMPLETE: Database connection is PERFECT.")
    print("---------------------------------------------------")
    print("The issue is likely PORT CONFLICT if the site doesn't load.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(diagnose_connection())
