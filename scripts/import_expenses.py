from finance_app.models import Expense, Category, ExpenseTag, Tag
import csv
from finance_app import db
import datetime
from decimal import Decimal


with open("expenses.csv") as file:
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
        amount_string = amount_string.removeprefix("-$")
        amount_string = amount_string.replace(",", "")
        amount = Decimal(amount_string)
        amount_cents = int(amount * 100)
        expense = Expense(
            date=date, title=title, amount=amount_cents, category=category
        )

        tags_string = row["Tags"]
        for tag_string in tags_string.split(","):
            tag = Tag.query.where(Tag.name == tag_string).first()
            if tag is None:
                tag = Tag(name=tag_string)
                db.session.add(tag)
            expense_tag = ExpenseTag(expense=expense, tag=tag)
            expense.tags.append(expense_tag)

        db.session.add(expense)

    db.session.commit()
