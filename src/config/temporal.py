from temporalio.client import Client
from kink import di

from .settings import get_settings

async def init_temporal():
    settings = get_settings()
    
    # Create Temporal client
    client = await Client.connect(settings.TEMPORAL_HOST)
    
    # Register client in DI container
    di[Client] = client

async def get_client() -> Client:
    return di[Client] 