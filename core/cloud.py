import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from core.config import settings

cloudinary.config( 
    cloud_name=settings.CLOUDINARY_CLOUD_NAME, 
    api_key=settings.CLOUDINARY_API_KEY, 
    api_secret=settings.CLOUDINARY_API_SECRET 
)

def upload_image(file: UploadFile) -> str:
    """
    Uploads an image file to Cloudinary and returns the secure URL.
    """
    try:
        # Read file content
        file_content = file.file.read()
        
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(
            file_content,
            folder="artfolio/artworks",
            resource_type="image"
        )
        
        return response.get("secure_url")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

def delete_image(public_id: str):
    """
    Deletes an image from Cloudinary using its public_id.
    """
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception as e:
        print(f"Error deleting image {public_id}: {e}")
