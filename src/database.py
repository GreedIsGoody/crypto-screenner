from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.config import settings
import os

print(f"--- DEBUG: DATABASE_URL IS '{settings.DATABASE_URL}' ---")
engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass
async def get_db():
    async with async_session() as session:
        yield session