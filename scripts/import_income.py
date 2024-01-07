from finance_app.models import (
    CategoryIncome,
    Category,
    Income,
)
import csv
from finance_app import db
import datetime
from decimal import Decimal


with open("income.csv") as file:
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        title = row["Title"]
        date = datetime.datetime.strptime(row["Date"], "%m/%d/%Y")
        print(f"{title} - {date}")
        income = Income(date=date, title=title)
        for category_name in ["God", "Save", "Spend"]:
            category = Category.query.where(Category.title == category_name).first()
            if category is None:
                print(f"Could not find category with name {category_name} for {title}!")
                continue

            amount_string = row[category_name].strip()
            if amount_string == "":
                amount_string = "0"
            amount_string = amount_string.removeprefix("$")
            amount_string = amount_string.replace(",", "")
            amount = Decimal(amount_string)
            amount_cents = int(amount * 100)

            ci = CategoryIncome(income=income, category=category, amount=amount_cents)
            income.category_incomes.append(ci)

        db.session.add(income)

    print(sum(i.total_amount for i in Income.query.all()))

    db.session.commit()
