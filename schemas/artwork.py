from beanie import PydanticObjectId
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from schemas.user import UserSummary

class ArtworkCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class ArtworkUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

class ArtworkResponse(BaseModel):
    id: PydanticObjectId = Field(validation_alias="_id")
    title: str
    description: Optional[str] = None
    image_url: str
    owner: UserSummary
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True
    )
