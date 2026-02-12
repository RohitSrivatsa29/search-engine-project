"""Test MongoDB connection"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    print(f"Testing connection to: {mongodb_url}")
    
    try:
        client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        db_list = await client.list_database_names()
        print(f"📚 Available databases: {db_list}")
        
        client.close()
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("1. If using local MongoDB, make sure it's running:")
        print("   - Windows: net start MongoDB")
        print("2. If using MongoDB Atlas:")
        print("   - Update MONGODB_URL in .env file")
        print("   - Format: mongodb+srv://username:password@cluster.mongodb.net/")

if __name__ == "__main__":
    asyncio.run(test_connection())
