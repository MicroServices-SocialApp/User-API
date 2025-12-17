import os
import logging
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import declarative_base

# ------------------------------------------------------------------------------------

load_dotenv()
DB_URL: str | None = os.getenv("DB_URL")

# ------------------------------------------------------------------------------------

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
engine: AsyncEngine = create_async_engine(f"{DB_URL}", echo=False)

# ------------------------------------------------------------------------------------

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

# ------------------------------------------------------------------------------------

async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
