from decimal import Decimal
from flask import redirect, render_template, request, url_for
from finance_app.main import main
from finance_app import db
from finance_app.main.forms.expense_form import ExpenseForm
from finance_app.models import Category, Expense


@main.route("/")
def index():
    return "Hello world!"


@main.route("/new_expense", methods=["GET", "POST"])
def new_expense():
    form = ExpenseForm()
    form.category.choices = [(cat.code, cat.title) for cat in Category.query.all()]
    if form.validate_on_submit():
        category = Category.query.get(form.category.data)
        expense = Expense(
            date=form.date.data,
            title=form.title.data,
            notes=form.notes.data,
            amount=int(form.amount.data * 100),
            category=category,
        )
        db.session.add(expense)
        db.session.commit()

        return redirect(url_for("main.list_expenses"))
    return render_template("new_expense_form.html", form=form)


@main.route("/list_expenses")
def list_expenses():
    expenses = Expense.query.all()
    return render_template("list_expenses.html", expenses=expenses)


@main.route("/list_categories")
def list_categories():
    categories = Category.query.all()
    return render_template("list_categories.html", categories=categories)
