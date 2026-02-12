from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
import logging
import certifi

logger = logging.getLogger(__name__)

# Global database client
client: AsyncIOMotorClient = None
database = None

async def connect_db():
    """Connect to MongoDB database with retry logic"""
    global client, database
    
    retries = 3
    for attempt in range(retries):
        try:
            # Create AsyncIOMotorClient with certifi and increased timeout
            client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=20000,
                socketTimeoutMS=20000
            )
            
            # Get database
            database = client[settings.DATABASE_NAME]
            
            # Test connection
            await client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {settings.DATABASE_NAME}")
            
            # Create indexes
            await create_indexes()
            return
            
        except Exception as e:
            logger.warning(f"Connection attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                import asyncio
                await asyncio.sleep(2)
            else:
                logger.error(f"Failed to connect to MongoDB after {retries} attempts")
                raise


async def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        logger.info("Closed MongoDB connection")


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # User collection indexes
        await database.users.create_index("email", unique=True)
        await database.users.create_index("username", unique=True)
        
        # Document collection indexes
        await database.documents.create_index("author_id")
        await database.documents.create_index("created_at")
        
        # Inverted index collection indexes
        await database.inverted_index.create_index("term")
        
        logger.info("Database indexes created")
    except Exception as e:
        logger.warning(f"Index creation warning: {e}")


def get_database():
    """Get database instance"""
    return database
