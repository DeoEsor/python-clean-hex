from temporalio.client import Client
from kink import di

async def init_temporal():
    # Create Temporal client
    client = await Client.connect("localhost:7233")
    
    # Register client in DI container
    di[Client] = client

async def get_client() -> Client:
    return di[Client] 