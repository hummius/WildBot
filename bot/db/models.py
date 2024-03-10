import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Request(BaseModel):
    __tablename__ = 'request'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    time: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now())
    vendor_code: Mapped[str] = mapped_column(String(150), nullable=False)


class User(BaseModel):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    spam: Mapped[bool] = mapped_column(default=False)
