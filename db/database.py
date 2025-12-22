import os
import logging
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
<<<<<<< Updated upstream
from sqlalchemy.orm import declarative_base
=======
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

# ------------------------------------------------------------------------------------

# This tells SQLAlchemy exactly how to name constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s", # Unique Constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)
>>>>>>> Stashed changes

# ------------------------------------------------------------------------------------

load_dotenv()
<<<<<<< Updated upstream
DB_URL: str | None = os.getenv("DATABASE_URL")
=======
DB_URL: str | None = os.getenv("DATABASE_URL") # DB_URL for local setup, DATABASE_URL for Docker
>>>>>>> Stashed changes

# ------------------------------------------------------------------------------------

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
<<<<<<< Updated upstream
=======
if not DB_URL:
    raise ValueError("CRITICAL: DATABASE_URL environment variable is required.")

>>>>>>> Stashed changes
engine: AsyncEngine = create_async_engine(DB_URL, echo=False)

# ------------------------------------------------------------------------------------

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
<<<<<<< Updated upstream
Base = declarative_base()
=======
>>>>>>> Stashed changes

# ------------------------------------------------------------------------------------

async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
<<<<<<< Updated upstream
=======
        except Exception:
            await db.rollback()
            raise
>>>>>>> Stashed changes
        finally:
            await db.close()
