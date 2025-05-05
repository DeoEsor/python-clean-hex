from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from kink import di

from ....domain.transaction import Transaction
from ....domain.portfolio import Portfolio
from ....domain.message import Message

async def init_db():
    # Create async engine
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/stock_service",
        echo=True
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Transaction.metadata.create_all)
        await conn.run_sync(Portfolio.metadata.create_all)
        await conn.run_sync(Message.metadata.create_all)
    
    # Create session factory
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Register session factory in DI container
    di[AsyncSession] = async_session

async def get_session() -> AsyncSession:
    session = di[AsyncSession]()
    try:
        yield session
    finally:
        await session.close() 