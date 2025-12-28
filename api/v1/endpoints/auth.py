from fastapi import APIRouter, HTTPException, Depends, status, Body
import jwt
from jwt.exceptions import PyJWTError as JWTError
from pydantic import ValidationError
from schemas.token import TokenPayload
from typing import Any
from schemas.user import UserCreate, UserResponse
from schemas.token import Token, RefreshTokenRequest, TokenRefreshResponse, LoginRequest
from core.utils import create_user, authenticate_user
from core.security import create_access_token, create_refresh_token
from datetime import datetime, timedelta, timezone
from core.config import settings
from models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate) -> Any:
    user = await User.find_one(User.email == user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This Email is already in use.",
        )
    user_username = await User.find_one(User.username == user_in.username)
    if user_username:
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is already in use.",
        )
    
    user = await create_user(user_in)
    return user

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest = Body(...)) -> Any:
    user = await authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    
    return {
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "access_token": access_token,
        "username": user.username
    }

@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(request: RefreshTokenRequest) -> Any:
    """
    Get a new access token using a refresh token.
    """
    try:
        payload = jwt.decode(
            request.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Smart Rotation Logic
    # Check if existing refresh token expires in less than 2 days
    exp_timestamp = payload.get("exp")
    if not exp_timestamp:
         raise HTTPException(status_code=400, detail="Invalid token")

    expire_date = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    
    # If expiring in < 2 days, rotate it
    if expire_date - now < timedelta(days=2):
        new_refresh_token = create_refresh_token(subject=token_data.sub)
    else:
        new_refresh_token = request.refresh_token

    access_token = create_access_token(subject=token_data.sub)

    return {
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
        "access_token": access_token
    }
