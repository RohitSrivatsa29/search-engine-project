from mongodb import get_database
from user import User, UserCreate, UserLogin
from security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta
from config import settings


class AuthService:
    """Authentication service for user management"""
    
    @staticmethod
    async def register_user(user_data: UserCreate) -> User:
        """Register a new user"""
        db = get_database()
        
        # Check if user already exists
        existing_user = await db.users.find_one({
            "$or": [
                {"email": user_data.email},
                {"username": user_data.username}
            ]
        })
        
        if existing_user:
            if existing_user.get("email") == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Create new user document
        user_doc = {
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hash_password(user_data.password),
            "created_at": User.model_fields['created_at'].default_factory()
        }
        
        # Insert into database
        result = await db.users.insert_one(user_doc)
        user_doc["_id"] = str(result.inserted_id)
        
        return User(**user_doc)
    
    @staticmethod
    async def authenticate_user(login_data: UserLogin) -> dict:
        """Authenticate user and return JWT token"""
        db = get_database()
        
        # Find user by email
        user = await db.users.find_one({"email": login_data.email})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not verify_password(login_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    @staticmethod
    async def get_user_by_email(email: str) -> User:
        """Get user by email"""
        db = get_database()
        user = await db.users.find_one({"email": email})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user["_id"] = str(user["_id"])
        return User(**user)
