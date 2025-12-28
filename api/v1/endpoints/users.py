from fastapi import APIRouter, HTTPException
from typing import List, Any
from models.user import User
from schemas.user import UserResponse
from models.artwork import Artwork
from schemas.artwork import ArtworkResponse

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



@router.get("/search", response_model=List[UserResponse])
async def search_users(q: str) -> Any:
    """
    Search users by username or full name.
    """
    query = {
        "$or": [
            {"username": {"$regex": q, "$options": "i"}},
            {"full_name": {"$regex": q, "$options": "i"}}
        ],
        "is_active": True
    }
    users = await User.find(query).to_list()
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

@router.get("/{user_id}/artworks", response_model=List[ArtworkResponse])
async def read_user_artworks(
    user_id: str,
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve all artworks by a specific user.
    """
    try:
        from beanie import PydanticObjectId
        obj_id = PydanticObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user = await User.get(obj_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Query artworks where owner.id matches the user's ID
    artworks = await Artwork.find(Artwork.owner.id == obj_id).skip(skip).limit(limit).to_list()
    
    # Populate the owner field with the user object for response validation
    for art in artworks:
        art.owner = user
        
    return artworks
