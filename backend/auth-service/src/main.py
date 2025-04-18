from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging

from config.settings import Settings
from interfaces.api.routes import router as api_router
from interfaces.api.middlewares.error_handler import error_handler_middleware
from interfaces.api.middlewares.request_logger import request_logger_middleware
from interfaces.api.dependencies import db
from infrastructure.startup import initialize_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Load settings
settings = Settings()

# Create FastAPI app
app = FastAPI(
    title="LMS Auth Service",
    description="Authentication and Authorization Service for the Learning Management System",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middlewares
app.middleware("http")(error_handler_middleware)
app.middleware("http")(request_logger_middleware)

# Include API routes
app.include_router(api_router, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "service": "auth-service"},
        status_code=200,
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize app on startup"""
    await initialize_app(settings, db)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    await db.close()

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
    ) 