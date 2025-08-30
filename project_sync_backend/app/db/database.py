from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.pool import NullPool
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from project_sync_backend.app.core.config import settings
import logging
import time

logger = logging.getLogger(__name__)

# Create engine with better connection parameters for Neon
engine = create_engine(
    settings.APP_DATABASE_URL,
    echo=False,
    # Disable connection pooling - better for serverless/cloud databases
    poolclass=NullPool,
    # Connection arguments for better reliability
    connect_args={
        "sslmode": "require",
        "connect_timeout": 30,  # Increased timeout
        "application_name": "ProjectSync",
        # Additional parameters for better connection stability
        "keepalives_idle": 600,
        "keepalives_interval": 30,
        "keepalives_count": 3,
    },
    # Pool settings (even though we're using NullPool, these are good to have)
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)

def create_db_and_tables():
    """Create database tables with retry logic"""
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to create database tables (attempt {attempt + 1}/{max_retries})")
            SQLModel.metadata.create_all(engine)
            logger.info("Database tables created successfully")
            return
        except OperationalError as e:
            logger.error(f"Database connection failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error("Failed to create database tables after all retries")
                raise
        except Exception as e:
            logger.error(f"Unexpected error creating database tables: {e}")
            raise

def get_session():
    """Get database session with connection validation"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            with Session(engine) as session:
                # Test the connection
                from sqlalchemy import text
                session.exec(text("SELECT 1"))
                yield session
                return
        except OperationalError as e:
            logger.warning(f"Database session failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                logger.error("Failed to establish database session after all retries")
                raise
        except Exception as e:
            logger.error(f"Unexpected error in database session: {e}")
            raise

def test_database_connection():
    """Test database connection - useful for health checks"""
    try:
        with Session(engine) as session:
            result = session.exec(text("SELECT version()"))
            version = result.first()
            logger.info(f"Database connection successful. PostgreSQL version: {version}")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

# Alternative async version (uncomment if you want to switch to async)
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Convert your connection string to async
ASYNC_DATABASE_URL = settings.APP_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    connect_args={
        "sslmode": "require",
        "server_settings": {
            "application_name": "ProjectSync",
        }
    }
)

AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def create_db_and_tables_async():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
"""
# from sqlmodel import create_engine, SQLModel, Session
# from project_sync_backend.app.core.config import settings

# engine = create_engine(settings.APP_DATABASE_URL, echo=False)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session