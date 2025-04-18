import logging
from datetime import datetime, timedelta

from infrastructure.database.connection import Database
from config.settings import Settings

logger = logging.getLogger(__name__)


async def initialize_database(settings: Settings, db: Database):
    """Initialize the database connection and create tables if they don't exist"""
    try:
        logger.info("Initializing database...")
        await db.create_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def initialize_app(settings: Settings, db: Database):
    """Initialize the application"""
    # Initialize database
    await initialize_database(settings, db)
    
    # Clean up expired tokens
    # This would normally be done in a background task, but for simplicity we'll do it here
    try:
        logger.info("Cleaning up expired tokens...")
        from infrastructure.repositories.token_repository import SQLAlchemyTokenRepository
        async with db.session() as session:
            token_repository = SQLAlchemyTokenRepository(session)
            expiry_date = datetime.utcnow() - timedelta(days=7)  # Clean tokens older than 7 days
            removed_count = await token_repository.clean_expired_tokens(expiry_date)
            logger.info(f"Removed {removed_count} expired tokens")
    except Exception as e:
        logger.warning(f"Error cleaning expired tokens: {e}")
    
    # Add more initialization steps as needed
    
    logger.info("Application initialized successfully") 