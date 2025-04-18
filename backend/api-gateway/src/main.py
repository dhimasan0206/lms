from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn

from config.settings import Settings
from interfaces.api.routes import router as api_router
from interfaces.api.middlewares.error_handler import error_handler_middleware
from interfaces.api.middlewares.request_logger import request_logger_middleware
from interfaces.api.middlewares.tenant_resolver import tenant_resolver_middleware

# Load settings
settings = Settings()

# Create FastAPI app
app = FastAPI(
    title="LMS API Gateway",
    description="API Gateway for the Learning Management System",
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
app.middleware("http")(tenant_resolver_middleware)

# Include API routes
app.include_router(api_router, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "service": "api-gateway"},
        status_code=200,
    )

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
    ) 