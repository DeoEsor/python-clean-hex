from .database import init_db
from .temporal import init_temporal
from .fastapi import init_fastapi
from .logger import init_logger
from .kafka import init_kafka, cleanup_kafka

async def init_config():
    # Initialize logger first
    init_logger()
    
    # Initialize other components
    await init_db()
    await init_temporal()
    await init_kafka()
    init_fastapi()

async def cleanup():
    await cleanup_kafka() 