from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.api import routes_verify, routes_pdf

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Official Tahsildar Community Certificate Application Verification and Request Generation System"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(routes_verify.router, prefix=settings.API_PREFIX)
app.include_router(routes_pdf.router, prefix=settings.API_PREFIX)

@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "system": settings.APP_NAME,
        "version": settings.VERSION
    }

# Mount Frontend static files
frontend_dir = settings.BASE_DIR.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
