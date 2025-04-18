import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:postgres@postgres:5432/lms_course"
)

# Create an async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

# Create an async session factory
async_session_factory = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False, 
    autoflush=False
)

async def get_session() -> AsyncSession:
    """
    Dependency for getting an AsyncSession instance.
    """
    async with async_session_factory() as session:
        yield session

async def init_db():
    """Initialize the database with tables"""
    from ..infrastructure.repositories import Base
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all) 