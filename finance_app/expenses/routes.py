from flask import redirect, render_template, url_for
from finance_app.models import Category, Expense
from .forms.expense_form import ExpenseForm
from finance_app import db
from . import expenses


@expenses.route("/new/", methods=["GET", "POST"])
def new():
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

        return redirect(url_for("expenses.list"))
    return render_template("new_expense.html", form=form)


@expenses.route("/list/")
def list():
    expenses = Expense.query.all()
    return render_template("list_expenses.html", expenses=expenses)
