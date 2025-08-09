"""
Pilar2 Backend API
FastAPI application for financial report analysis
"""

import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings, ENGLISH_TEXTS
from backend.routes import upload, analysis, reports, qa, recommendations, enhanced_qa
from backend.utils.logger import setup_logging

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Pilar2 Backend API...")
    logger.info(f"Version: {settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Pilar2 Backend API...")

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    description="Intelligent system for financial report analysis and regulatory report generation",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix=f"{settings.API_V1_STR}/upload", tags=["Upload"])
app.include_router(analysis.router, prefix=f"{settings.API_V1_STR}/analysis", tags=["Analysis"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["Reports"])
app.include_router(qa.router, prefix=f"{settings.API_V1_STR}/qa", tags=["Q&A"])
app.include_router(enhanced_qa.router, prefix=f"{settings.API_V1_STR}/enhanced-qa", tags=["Enhanced Q&A"])
app.include_router(recommendations.router, prefix=f"{settings.API_V1_STR}/recommendations", tags=["Recommendations"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": ENGLISH_TEXTS['app_title'],
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "message": ENGLISH_TEXTS['error_occurred']
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"General Exception: {str(exc)}")
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "message": ENGLISH_TEXTS['error_occurred']
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
