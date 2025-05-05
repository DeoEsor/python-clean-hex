import asyncio
import uvicorn
from kink import di

from src.config.database import init_db
from src.config.temporal import init_temporal
from src.entrypoints.api import app

async def main():
    # Initialize database
    await init_db()
    
    # Initialize Temporal
    await init_temporal()
    
    # Start FastAPI application
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
