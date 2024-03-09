from typing import Dict

from aiogram.types import Message
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from config import DB_URL
from . import BaseModel
from .models import Request


# def create_async_engine(url: URL | str) -> AsyncEngine:
#     return _create_async_engine(url, echo=True, pool_pre_ping=True)
#
#
# async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(metadata.create_all)
#
#
# def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
#     return async_sessionmaker(engine)

engine = _create_async_engine(DB_URL, echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
