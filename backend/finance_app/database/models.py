import enum
from typing import List
from . import db
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
        DateTime, nullable=False, default=datetime.now()
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    percent_spend: Mapped[int] = mapped_column(Integer, nullable=False, default=80)


class Expense(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    notes: Mapped[str] = mapped_column(String(4000), nullable=False, default="")
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category: Mapped[Category] = mapped_column(Enum(Category))
    tags: Mapped[List["ExpenseTag"]] = relationship()


class Tag(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)


class ExpenseTag(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expense_id: Mapped[int] = mapped_column(ForeignKey(f"{Expense.__tablename__}.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey(f"{Tag.__tablename__}.id"))
    tag: Mapped["Tag"] = relationship()
