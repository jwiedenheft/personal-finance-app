import enum
from . import db
from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Category(enum.Enum):
    GOD = 1
    SAVING = 2
    SPENDING = 3
    OTHER = 4


class Income(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default_factory=datetime.now
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    percent_spend: Mapped[int] = mapped_column(Integer, nullable=False, default=80)


class Spend(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default_factory=datetime.now
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    notes: Mapped[str] = mapped_column(String(4000), nullable=False, default="")
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category: Mapped[Category] = mapped_column(Enum(Category))
