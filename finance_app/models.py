from decimal import Decimal
from typing import List
from finance_app import db
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from finance_app.utils import int_to_money


class Category(db.Model):
    code: Mapped[str] = mapped_column(String(10), nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(String(60), nullable=False, default="")
    color: Mapped[str] = mapped_column(String(6), default="ffffff", nullable=False)
    expenses: Mapped[List["Expense"]] = relationship()


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
    category_code: Mapped[str] = mapped_column(
        ForeignKey(f"{Category.__tablename__}.code")
    )
    category: Mapped["Category"] = relationship(back_populates="expenses")
    tags: Mapped[List["ExpenseTag"]] = relationship()

    def formatted_amount(self):
        return f"-{int_to_money(self.amount)}"

    def tag_string(self):
        return "; ".join([tag.name for tag in self.tags])


class Tag(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)


class ExpenseTag(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expense_id: Mapped[int] = mapped_column(ForeignKey(f"{Expense.__tablename__}.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey(f"{Tag.__tablename__}.id"))
    tag: Mapped["Tag"] = relationship()
