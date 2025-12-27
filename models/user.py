from typing import Optional
from beanie import Document, Indexed
from pydantic import EmailStr

class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: bool = True

    class Settings:
        name = "users"
