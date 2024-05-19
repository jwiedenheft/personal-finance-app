import os
import click
from flask import Blueprint
from finance_app.models import (
    Expense,
    Category,
    ExpenseTag,
    Income,
    Tag,
)
import csv
from finance_app import db
import datetime
from decimal import Decimal
import secrets

import_bp = Blueprint("import", __name__)


@import_bp.cli.command("income")
@click.argument("file_path")
def import_income(file_path):
    # Make sure user provided valid file path
    if not os.path.exists(file_path):
        print(f"Could not find file at {file_path}!")
        return

    with open(file_path) as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            title = row["Title"]
            date = datetime.datetime.strptime(row["Date"], "%m/%d/%Y")
            print(f"{title} - {date}")
            for category_name in ["God", "Save", "Spend"]:
                category = Category.query.where(Category.title == category_name).first()
                if category is None:
                    print(
                        f"Could not find category with name {category_name} for {title}!"
                    )
                    continue

                amount_string = row[category_name].strip()
                if amount_string == "":
                    amount_string = "0"
                amount_string = amount_string.removeprefix("$")
                amount_string = amount_string.replace(",", "")
                amount = Decimal(amount_string)
                amount_cents = int(amount * 100)

                income = Income(
                    title=title, category=category, amount=amount_cents, date=date
                )
                db.session.add(income)

        db.session.commit()


@import_bp.cli.command("expenses")
@click.argument("file_path")
def import_expenses(file_path):
    # Make sure user provided valid file path
    if not os.path.exists(file_path):
        print(f"Could not find file at {file_path}!")
        return

    with open(file_path) as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            title = row["Title"]
            print(title)
            date = datetime.datetime.strptime(row["Date"], "%m/%d/%Y")
            category_name = row["Category"].strip()
            category = Category.query.where(Category.title == category_name).first()
            if category is None:
                print(f"Could not find category with name {category_name} for {title}!")
                continue
            amount_string = row["Amount"]
            amount_string = amount_string.replace("$", "")
            amount_string = amount_string.removeprefix("-")
            amount_string = amount_string.replace(",", "")
            if amount_string == "":
                amount = 0
            else:
                print(amount_string)
                amount = Decimal(amount_string)
            amount_cents = int(amount * 100)
            expense = Expense(
                date=date, title=title, amount=amount_cents, category=category
            )

            tags_string = row["Tags"]
            for tag_string in tags_string.split(","):
                tag = Tag.query.where(Tag.name == tag_string).first()
                if tag is None:
                    tag = Tag(name=tag_string, color=secrets.token_hex(3))
                    db.session.add(tag)
                expense_tag = ExpenseTag(expense=expense, tag=tag)
                expense.tags.append(expense_tag)

            db.session.add(expense)

        db.session.commit()
