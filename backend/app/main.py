"""
DealLens API - Main Application Entry Point
AI-Powered Startup Research Tool for VC Analysts
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time

from app.config import settings
from app.database import init_db
from app.routes import auth, analyze, history, profiles

# Configure loguru
logger.add(
    "logs/deallens_{time}.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Startup/shutdown lifecycle."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    init_db()
    logger.info("Database initialized successfully")
    yield
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    description="""
    ## DealLens API
    
    AI-Powered Startup Research Tool for VC Analysts.
    
    ### Features
    - 🔍 Analyze startups with GLM-5.1 or OpenAI GPT-4
    - 📊 Generate structured VC-style investment snapshots
    - 📋 Multiple fund profile support
    - 📜 Analysis history with statistics
    - 🔐 JWT Authentication
    
    ### Quick Start
    1. Create an account: `POST /auth/signup`
    2. Login: `POST /auth/login`
    3. Analyze a startup: `POST /analyze`
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 3))
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)} | Path: {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again.", "success": False},
    )


# Register routers
app.include_router(auth.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(profiles.router, prefix="/api")


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API info."""
    return {
        "message": "Welcome to DealLens API",
        "docs": "/docs",
        "health": "/health",
        "version": settings.APP_VERSION,
    }