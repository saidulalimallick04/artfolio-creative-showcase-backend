from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List, Any, Optional
from models.artwork import Artwork
from models.user import User
from beanie import Link

from schemas.artwork import ArtworkResponse, ArtworkUpdate
from api.deps import get_current_user
from core.cloud import upload_image


router = APIRouter()

@router.post("", response_model=ArtworkResponse, status_code=status.HTTP_201_CREATED)
async def create_artwork(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create a new artwork. Requires an image file and metadata.
    """
    # Upload image to Cloudinary
    image_url = upload_image(image)
    
    artwork = Artwork(
        title=title,
        description=description,
        image_url=image_url,
        owner=current_user
    )
    await artwork.create()
    return artwork

@router.get("", response_model=List[ArtworkResponse])
async def read_artworks(
    skip: int = 0,
    limit: int = 100
) -> Any:
    """ 
    Retrieve all artworks.
    """
    # Fetch all to apply randomization
    all_artworks = await Artwork.find_all().skip(skip).limit(skip+limit).to_list()
    # Manually fetch links to avoid Beanie crash/validation error
    # This is a workaround for the fetch_links bug
    for art in all_artworks:
        if isinstance(art.owner, Link):
            # Fetch the user. Ideally use lookups but simple fetch for now
            # Note: accessign art.owner after this might still be a Link locally depending on Beanie behavior
            # Check if we can replace it.
            # Using fetch() on the link itself if available, or finding the user.
            user = await User.get(art.owner.ref.id)
            art.owner = user
            
    return all_artworks

@router.get("/search", response_model=List[ArtworkResponse])
async def search_artworks(q: str) -> Any:
    """
    Search artworks by title or description.
    """
    query = {
        "$or": [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}}
        ]
    }
    all_artworks = await Artwork.find(query).to_list()
    
    # Populate owner links
    for art in all_artworks:
        if isinstance(art.owner, Link):
            user = await User.get(art.owner.ref.id)
            art.owner = user
            
    return all_artworks

@router.get("/{id}", response_model=ArtworkResponse)
async def read_artwork(id: str) -> Any:
    """
    Get a specific artwork by ID.
    """
    artwork = await Artwork.get(id)
    if not artwork:
        raise HTTPException(
            status_code=404,
            detail="Artwork not found"
        )
    if isinstance(artwork.owner, Link):
        user = await User.get(artwork.owner.ref.id)
        artwork.owner = user
    return artwork

@router.patch("/{id}", response_model=ArtworkResponse)
async def update_artwork(
    id: str,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update artwork details. Only the owner can update.
    """
    artwork = await Artwork.get(id)
    if not artwork:
        raise HTTPException(
            status_code=404,
            detail="Artwork not found"
        )
        
    if artwork.owner.ref.id != current_user.id:
         raise HTTPException(
            status_code=403,
            detail="Not authorized to update this artwork"
        )
        
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
        
    if image:
        # Delete old image if exists? For now we just overwrite the URL
        image_url = upload_image(image)
        update_data["image_url"] = image_url
        
    if update_data:
        await artwork.set(update_data)
        
    # Manually set owner to current_user to ensure response validation passes
    # (Beanie's Link doesn't auto-fetch, but we know it's the current user)
    artwork.owner = current_user
    
    return artwork

@router.delete("/{id}", response_model=dict)
async def delete_artwork(
    id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete an artwork. Only the owner can delete it.
    """
    artwork = await Artwork.get(id)
    if not artwork:
        raise HTTPException(
            status_code=404,
            detail="Artwork not found"
        )
    
    if artwork.owner.ref.id != current_user.id:
         raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this artwork"
        )

    # TODO: Extract public_id from Cloudinary URL if we want to delete from Cloudinary too
    # For now, we just delete from DB
    await artwork.delete()
    return {"message": "Artwork deleted successfully"}
