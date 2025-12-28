from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: PydanticObjectId = Field(validation_alias="_id")
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True
    )

class UserSummary(BaseModel):
    username: str
    profile_image: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str
