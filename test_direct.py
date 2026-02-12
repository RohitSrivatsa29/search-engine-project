"""Direct test of auth service"""
import asyncio
import sys
sys.path.insert(0, '.')

from mongodb import connect_db, close_db
from auth_service import AuthService
from user import UserCreate

async def test():
    await connect_db()
    
    try:
        user_data = UserCreate(
            email="directtest@example.com",
            username="directtest",
            password="testpass123"
        )
        
        print("Creating user...")
        user = await AuthService.register_user(user_data)
        print(f"✅ User created: {user.email}")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    await close_db()

if __name__ == "__main__":
    asyncio.run(test())
