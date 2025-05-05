from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kink import di

def init_fastapi():
    # Create FastAPI app
    app = FastAPI(
        title="Stock Service",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register app in DI container
    di[FastAPI] = app

def get_app() -> FastAPI:
    return di[FastAPI] 