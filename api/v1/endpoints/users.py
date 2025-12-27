from fastapi import APIRouter, HTTPException
from typing import List, Any
from models.user import User
from schemas.user import UserResponse

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve all users.
    Only active users are returned.
    """
    query = {User.is_active: True}
        
    users = await User.find(query).skip(skip).limit(limit).to_list()
    return users



@router.get("/{username}", response_model=UserResponse)
async def read_user_by_username(username: str) -> Any:
    """
    Get user by username.
    """
    user = await User.find_one(User.username == username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user
