from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from config.settings import Settings


class Database:
    def __init__(self, settings: Settings):
        # Convert SQLAlchemy URL to asyncpg format (postgresql:// -> postgresql+asyncpg://)
        if settings.DATABASE_URL.startswith("postgresql://"):
            db_url = settings.DATABASE_URL.replace(
                "postgresql://", "postgresql+asyncpg://", 1
            )
        else:
            db_url = settings.DATABASE_URL
        
        self.engine = create_async_engine(
            db_url,
            echo=settings.DEBUG,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800
        )
        
        self.session_factory = sessionmaker(
            self.engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
    
    @asynccontextmanager
    async def session(self):
        """Get a database session"""
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
    
    async def create_tables(self):
        """Create database tables"""
        from infrastructure.database.models import Base
        
        async with self.engine.begin() as conn:
            # Uncomment to recreate tables on startup (for development only)
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    
    async def close(self):
        """Close database connection"""
        await self.engine.dispose() 