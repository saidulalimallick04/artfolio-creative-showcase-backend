from beanie import Document, Link
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone
from models.user import User

class Artwork(Document):
    title: str
    description: Optional[str] = None
    image_url: str
    owner: Link[User]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "artworks"
