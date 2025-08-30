import asyncio
import os
import sys
import ssl
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from alembic import context
from project_sync_backend.app.models.user import User
from project_sync_backend.app.models.projects import Project  
from project_sync_backend.app.models.issue import Issue

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import app settings and models
from project_sync_backend.app.core.config import settings
from project_sync_backend.app.models import *

# Alembic Config
config = context.config
config.set_main_option("sqlalchemy.url", settings.ALEMBIC_DATABASE_URL)
fileConfig(config.config_file_name)
target_metadata = SQLModel.metadata

# ✅ Create an SSL context required by Neon
ssl_context = ssl.create_default_context()

connectable = create_async_engine(
    settings.ALEMBIC_DATABASE_URL,
    connect_args={"ssl": ssl_context},
)

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_online():
    asyncio.run(run_async_migrations())

run_migrations_online()
