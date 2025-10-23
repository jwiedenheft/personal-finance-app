from typing import List
from finance_app import db
from sqlalchemy import DateTime, ForeignKey, Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from dateutil import relativedelta
from finance_app.utils import int_to_money


class Category(db.Model):
    code: Mapped[str] = mapped_column(String(10), nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(String(60), nullable=False, default="")
    color: Mapped[str] = mapped_column(String(6), default="ffffff", nullable=False)

    expenses: Mapped[List["Expense"]] = relationship(back_populates="category")
    income: Mapped[List["Income"]] = relationship(back_populates="category")

    def balance_current(self):
        total_expense = sum(
            [e.amount for e in self.expenses if e.date <= datetime.today()]
        )
        total_income = sum(
            [i.amount for i in self.income if i.date <= datetime.today()]
        )
        return total_income - total_expense

    def balance(self):
        return self.income_total - self.expenses_total

    @property
    def expenses_total(self):
        return sum([e.amount for e in self.expenses])

    @property
    def income_total(self):
        return sum([i.amount for i in self.income])

    def balance_for_month(self, year: int, month: int):
        month_start = datetime(year=year, month=month, day=1)
        next_month = month + 1
        if next_month > 12:
            next_month = next_month - 12
        next_month_start = datetime(
            year=year + 1 if month == 12 else year,
            month=next_month,
            day=1,
        )
        month_income = (
            db.session.execute(
                select(Income.amount).where(
                    Income.category == self,
                    Income.date >= month_start,
                    Income.date < next_month_start,
                )
            )
            .scalars()
            .all()
        )
        month_expense = (
            db.session.execute(
                select(Expense.amount).where(
                    Expense.category == self,
                    Expense.date >= month_start,
                    Expense.date < next_month_start,
                )
            )
            .scalars()
            .all()
        )
        return sum(month_income) - sum(month_expense)


class Income(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(256), nullable=False, default="")

    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @property
    def date_string(self):
        return self.date.strftime("%m/%d/%y")

    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def formatted_amount(self) -> str:
        return int_to_money(self.amount)

    notes: Mapped[str] = mapped_column(String(4000), nullable=False, default="")

    create_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    category_code: Mapped[str] = mapped_column(
        ForeignKey(f"{Category.__tablename__}.code"), nullable=False
    )
    category: Mapped["Category"] = relationship(back_populates="income")


class Expense(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    notes: Mapped[str] = mapped_column(String(4000), nullable=False, default="")
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category_code: Mapped[str] = mapped_column(
        ForeignKey(f"{Category.__tablename__}.code")
    )
    category: Mapped["Category"] = relationship(back_populates="expenses")
    tags: Mapped[List["ExpenseTag"]] = relationship(
        back_populates="expense",
        cascade="delete",
    )

    def formatted_amount(self):
        return f"-{int_to_money(self.amount)}"

    def tag_string(self):
        tags = [et.tag.name for et in self.tags]
        return ";".join(tags)

    def has_tag(self, tag: str):
        return any(t.tag.name == tag for t in self.tags)


class Tag(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    color: Mapped[str] = mapped_column(
        String(6), server_default="6C757D", nullable=False
    )


class ExpenseTag(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    expense_id: Mapped[int] = mapped_column(ForeignKey(f"{Expense.__tablename__}.id"))
    expense: Mapped["Expense"] = relationship()

    tag_id: Mapped[int] = mapped_column(ForeignKey(f"{Tag.__tablename__}.id"))
    tag: Mapped["Tag"] = relationship()
