from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
import logging

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    ASYNC_DRIVER: str
    SYNC_DRIVER: str
    USER: str
    PASSWORD: str
    HOST: str
    NAME: str
    PORT: int

    model_config = SettingsConfigDict(env_file=".env.database", env_prefix="DATABASE_")

database_settings = DatabaseSettings()

DATABASE_URL = f"{database_settings.ASYNC_DRIVER}://{database_settings.USER}:{database_settings.PASSWORD}@{database_settings.HOST}:{database_settings.PORT}/{database_settings.NAME}"

engine_parameters = {
    "pool_pre_ping": True,
    "echo": True,
}

engine = create_async_engine(DATABASE_URL, **engine_parameters)

constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=constraint_naming_conventions)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_database_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error(e)
            await session.rollback()
        finally:
            await session.close()
