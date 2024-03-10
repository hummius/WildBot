import datetime
from typing import Dict, Any

from aiogram.types import Message
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from db import Request
from db.models import User


async def orm_request(session: AsyncSession, data: Dict, msg: Message) -> None:
    obj = Request(
        user_id=msg.from_user.id,
        vendor_code=data['code'],
        time=datetime.datetime.now(),
    )
    session.add(obj)
    await session.commit()
    await session.close()


async def orm_get_db(session: AsyncSession, msg: Message) -> Any:
    statement = select(Request).where(Request.user_id == msg.from_user.id).order_by(desc(Request.time))
    result = await session.execute(statement)
    await session.close()
    return result.scalars().all()[:5]


async def orm_add_user(session: AsyncSession, msg: Message) -> None:
    obj = User(
        user_id=msg.from_user.id,
    )
    session.add(obj)
    await session.commit()
    await session.close()


async def orm_update_user(session: AsyncSession, user_id: int, flag: bool) -> None:
    statement = select(User).where(User.user_id == user_id)
    result = await session.execute(statement)
    user = result.scalar()
    user.spam = flag
    await session.commit()
    await session.close()


async def orm_get_user(session: AsyncSession, user_id: int) -> Any:
    statement = select(User).where(User.user_id == user_id)
    result = await session.execute(statement)
    await session.close()
    return result.scalar()
