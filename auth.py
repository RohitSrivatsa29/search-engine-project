from fastapi import APIRouter, Depends, status
from auth_service import AuthService
from auth_middleware import get_current_user
from user import UserCreate, UserLogin, Token, UserResponse, User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
    """Register a new user"""
    user = await AuthService.register_user(user_data)
    return user


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    """Login and get JWT token"""
    token = await AuthService.authenticate_user(login_data)
    return token


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return current_user
