from fastapi import APIRouter
from api.v1.endpoints import auth, users, artworks, account

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(artworks.router, prefix="/artworks", tags=["Artworks"])
api_router.include_router(account.router, prefix="/account-details", tags=["Account Details"])
