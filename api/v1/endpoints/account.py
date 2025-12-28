from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Any, Optional
from schemas.user import UserResponse
from models.user import User
from api.deps import get_current_user
from core.cloud import upload_image

router = APIRouter()

@router.get("", response_model=UserResponse)
async def read_account_details(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user account details.
    """
    return current_user

@router.patch("", response_model=UserResponse)
async def update_account_details(
    full_name: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update account details (Profile Info & Image).
    """
    updated = False
    
    if full_name is not None:
        current_user.full_name = full_name
        updated = True
        
    if bio is not None:
        current_user.bio = bio
        updated = True
        
    if profile_image:
        image_url = upload_image(profile_image)
        current_user.profile_image = image_url
        updated = True
        
    if updated:
        await current_user.save()
        
    return current_user

@router.patch("/deactivate", response_model=dict)
async def deactivate_account(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deactivate own account.
    """
    current_user.is_active = False
    await current_user.save()
    return {"message": "User account deactivated successfully"}

@router.patch("/reactivate", response_model=dict)
async def reactivate_account(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Reactivate own account.
    """
    current_user.is_active = True
    await current_user.save()
    return {"message": "User account reactivated successfully"}
