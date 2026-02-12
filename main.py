from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from mongodb import connect_db, close_db
from config import settings
import logging

# Import routers
from auth import router as auth_router
from documents import router as documents_router
from search import router as search_router
from sample_data import router as sample_data_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Search Engine API...")
    print("🚀 LIFESPAN STARTUP EVENT TRIGGERED")
    
    # Retry connection logic directly in lifespan to ensure app starts
    for i in range(3):
        try:
            await connect_db()
            logger.info("✅ Database connection established.")
            break
        except Exception as e:
            logger.warning(f"⚠️ Startup connection attempt {i+1} failed: {e}")
            if i < 2:
                import asyncio
                await asyncio.sleep(2)
            else:
                logger.error("❌ Could not connect to MongoDB on startup. App will run but API may fail.")
    
    try:
        yield
    except Exception as e:
        logger.error(f"❌ Application runtime error: {e}")
    finally:
        # Shutdown
        logger.info("🛑 Shutting down Search Engine API...")
        try:
            await close_db()
        except Exception as e:
            logger.warning(f"⚠️ Error closing database connection: {e}")


# Create FastAPI app
app = FastAPI(
    title="Search Engine API",
    description="A professional search engine with inverted indexing and TF-IDF ranking",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS - Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(search_router)
app.include_router(sample_data_router)


from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

# Serve index.html as the root page
@app.get("/")
async def read_root():
    return FileResponse("index.html")

# Serve index.html explicitly
@app.get("/index.html")
async def read_index_html():
    return FileResponse("index.html")

# Serve upload.html
@app.get("/upload.html")
async def read_upload_html():
    return FileResponse("upload.html")

# Serve upload.html at /upload too (legacy support)
@app.get("/upload")
async def read_upload():
    return FileResponse("upload.html")

@app.get("/health")
async def health_check():
    """Health check endpoint with DB status"""
    from mongodb import get_database
    
    db_status = "disconnected"
    db_error = None
    
    try:
        db = get_database()
        if db is not None:
            # Simple command to check connection
            await db.command('ping')
            db_status = "connected"
    except Exception as e:
        db_status = "error"
        db_error = str(e)
        logger.error(f"Health check DB error: {e}")

    return {
        "status": "online",
        "service": "Search Engine API",
        "database": db_status,
        "error": db_error,
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Launching Search Engine Server...")
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
