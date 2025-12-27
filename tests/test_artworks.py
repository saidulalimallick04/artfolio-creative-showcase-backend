import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
import os

# Read the valid test image created by the debug script
# If it doesn't exist, we should probably fail or handle it, 
# but for now we assume the debug steps created it.
IMAGE_PATH = "test_image.jpg"

def get_image_content():
    if os.path.exists(IMAGE_PATH):
        with open(IMAGE_PATH, "rb") as f:
            return f.read()
    # Fallback to a minimal valid JPEG if file missing (though user asked to use the file)
    raise Exception("Test image not found or error")

@pytest.mark.asyncio
async def test_create_artwork(client: AsyncClient, auth_headers):
    image_content = get_image_content()
    # Mock Cloudinary upload
    with patch("api.v1.endpoints.artworks.upload_image") as mock_upload:
        mock_upload.return_value = "http://res.cloudinary.com/demo/image/upload/sample.jpg"
        
        response = await client.post("/api/v1/artworks/", 
            data={"title": "Test Art"},
            files={"image": ("test_image.jpg", image_content, "image/jpeg")},
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Art"
        assert data["image_url"] == "http://res.cloudinary.com/demo/image/upload/sample.jpg"

@pytest.mark.asyncio
async def test_list_artworks(client: AsyncClient):
    response = await client.get("/api/v1/artworks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_delete_artwork(client: AsyncClient, auth_headers):
    image_content = get_image_content()
    # Create an artwork first
    with patch("api.v1.endpoints.artworks.upload_image") as mock_upload:
        mock_upload.return_value = "http://url"
        create_res = await client.post("/api/v1/artworks/", 
            data={"title": "To Delete"},
            files={"image": ("test_image.jpg", image_content, "image/jpeg")},
            headers=auth_headers
        )
        artwork_id = create_res.json()["_id"]
        
        # Delete it
        response = await client.delete(f"/api/v1/artworks/{artwork_id}", headers=auth_headers)
        assert response.status_code == 200
        
        # Verify it's gone
        get_res = await client.get(f"/api/v1/artworks/{artwork_id}")
        assert get_res.status_code == 404

@pytest.mark.asyncio
async def test_update_artwork(client: AsyncClient, auth_headers):
    image_content = get_image_content()
    # 1. Create Artwork
    with patch("api.v1.endpoints.artworks.upload_image") as mock_upload:
        mock_upload.return_value = "http://original-url"
        create_res = await client.post("/api/v1/artworks/", 
            data={"title": "Original"},
            files={"image": ("test_image.jpg", image_content, "image/jpeg")},
            headers=auth_headers
        )
        artwork_id = create_res.json()["_id"]

    # 2. Update Metadata only (using form data)
    response = await client.patch(f"/api/v1/artworks/{artwork_id}",
        data={"title": "Updated Title"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    
    # 3. Update File (using multipart)
    with patch("api.v1.endpoints.artworks.upload_image") as mock_upload_new:
        mock_upload_new.return_value = "http://new-url"
        response = await client.patch(f"/api/v1/artworks/{artwork_id}",
            files={"image": ("new_image.jpg", image_content, "image/jpeg")},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["image_url"] == "http://new-url"
