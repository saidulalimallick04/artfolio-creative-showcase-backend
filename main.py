from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config import settings
from db.mongodb import init_db
import importlib
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    # openapi_url will default to /openapi.json which is fine for all versions
    lifespan=lifespan
)

def include_api_versions(application: FastAPI):
    api_dir = Path(__file__).parent / "api"
    for item in api_dir.iterdir():
        if item.is_dir() and item.name.startswith("v"):
            version = item.name
            try:
                # Assuming structure: api.v1.api.api_router
                module_path = f"api.{version}.api"
                module = importlib.import_module(module_path)
                if hasattr(module, "api_router"):
                    application.include_router(
                        module.api_router, 
                        prefix=f"/api/{version}"
                    )
            except ImportError as e:
                print(f"Warning: Could not import API version {version}: {e}")
            except Exception as e:
                print(f"Error loading API version {version}: {e}")

include_api_versions(app)

@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Welcome to ArtFolio API", 
        "status": "running"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok"
    }
