from flask import current_app, redirect, render_template, url_for, request
from finance_app.models import Category, Expense
from .forms.expense_form import ExpenseForm
from finance_app import db
from . import expenses


@expenses.route("/list/")
def list():
    page = request.args.get("page", 1, type=int)
    items_per_page = current_app.config.get("RESULTS_PER_PAGE") or 10
    expenses = Expense.query.order_by(Expense.date.desc()).paginate(
        page=page, per_page=items_per_page
    )

    next_url = None
    if expenses.has_next:
        next_url = url_for("expenses.list", page=expenses.next_num)
    prev_url = None
    if expenses.has_prev:
        prev_url = url_for("expenses.list", page=expenses.prev_num)

    return render_template(
        "list_expenses.html",
        expenses=expenses.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@expenses.route("/new", methods=["GET", "POST"])
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


@expenses.route("/delete/<id>")
def delete(id: int):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("expenses.list"))
