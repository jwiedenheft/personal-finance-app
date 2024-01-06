from flask import render_template
from finance_app.main import main
from finance_app.models import Category, Expense


@main.route("/")
def index():
    return "Hello world!"


@main.route("/list_expenses")
def list_expenses():
    expenses = Expense.query.all()
    return render_template("list_expenses.html", expenses=expenses)


@main.route("/list_categories")
def list_categories():
    categories = Category.query.all()
    return render_template("list_categories.html", categories=categories)
