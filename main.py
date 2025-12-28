from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
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
    lifespan=lifespan
)

templates = Jinja2Templates(directory="templates")

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

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("templates/favicon.ico")

@app.get("/", tags=["Root"], response_class=HTMLResponse)
async def root(request: Request):
    
    # Calculate Real API Stats
    total_endpoints = 0
    get_count = 0
    post_count = 0
    put_count = 0
    delete_count = 0
    
    for route in app.routes:
        if hasattr(route, "methods"):
            methods = route.methods
            total_endpoints += 1
            if "GET" in methods: get_count += 1
            if "POST" in methods: post_count += 1
            if "PUT" in methods or "PATCH" in methods: put_count += 1
            if "DELETE" in methods: delete_count += 1

    context_data = {
        "request": request,
        
        # PROJECT INFO
        "project_name": settings.PROJECT_NAME,
        "project_version": "v1.0.0",
        "project_description": "A robust, scalable backend system for a creative portfolio application, enabling artists to showcase their work and connect with a community.",
        "project_keywords": "fastapi, backend, api, mongodb, cloudinary, python",
        "project_repo_url": "https://github.com/saidulalimallick04/artfolio-creative-showcase-backend",
        
        # DEVELOPER INFO
        "developers": [
            {
                "name": "Saidul Ali Mallick (Sami)",
                "username": "saidulalimallick04",
                "role": "Backend Developer & AIML Engineer",
                "quote": "Building robust APIs, one endpoint at a time.",
                "github_url": "https://github.com/saidulalimallick04",
                "linkedin_url": "https://linkedin.com/in/saidulalimallick04",
                "twitter_url": "https://x.com/saidulmallick04"
            },
        ],
        
        # HERO SECTION
        "hero_badge_text": "v1.0.0 Live",
        "hero_title": "ArtFolio API",
        "hero_description": "Empowering artists to showcase their creativity through a high-performance, secure, and scalable REST API built with modern technologies.",
        
        # API STATS (Real Data)
        "api_total_endpoints": str(total_endpoints),
        "api_get_count": get_count,
        "api_post_count": post_count,
        "api_put_count": put_count,
        "api_delete_count": delete_count,
        
        # ABOUT SECTION
        "about_description": "ArtFolio is a production-ready RESTful API facilitating user management, secure authentication, and diverse artwork portfolios.",
        
        # TECH STACK
        "tech_stack": [
            {
                "icon": "fab fa-python", 
                "name": "Python"
            },
            {
                "icon": "fas fa-bolt", 
                "name": "FastAPI"
            },
            {
                "icon": "fas fa-database", 
                "name": "MongoDB"
            },
            {
                "icon": "fas fa-shield-alt", 
                "name": "JWT Auth"
            },
            {
                "icon": "fas fa-cloud", 
                "name": "Cloudinary"
            },
        ],
        
        # QUICK LINKS
        "quick_links": [
            {
                "icon": "fas fa-book", 
                "name": "Swagger UI", 
                "url": "/docs"
            },
            {
                "icon": "fas fa-file-alt", 
                "name": "ReDoc", 
                "url": "/redoc"
            },
            {
                "icon": "fab fa-github", 
                "name": "Repository", 
                "url": "https://github.com/saidulalimallick04/artfolio-creative-showcase-backend"
            },
        ],
        
        # SERVER STATUS
        "server_status": "All Systems Operational",
        "server_api_status": "Healthy",
        "server_db_status": "Connected"
    }

    return templates.TemplateResponse("index_jinja.html", context_data)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok"
    }
