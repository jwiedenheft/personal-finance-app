from flask import current_app, redirect, render_template, url_for, request
from finance_app.models import Category, Income
from finance_app import db
from . import income


@income.route("/list/")
def list():
    page = request.args.get("page", 1, type=int)
    items_per_page = current_app.config.get("RESULTS_PER_PAGE") or 10

    income = Income.query.order_by(Income.date.desc()).paginate(
        page=page, per_page=items_per_page
    )

    next_url = None
    if income.has_next:
        next_url = url_for("income.list", page=income.next_num)
    prev_url = None
    if income.has_prev:
        prev_url = url_for("income.list", page=income.prev_num)

    return render_template(
        "list_income.html",
        categories=Category.query.order_by(Category.code).all(),
        income_items=income.items,
        next_url=next_url,
        prev_url=prev_url,
    )


""" @income.route("/new", methods=["GET", "POST"])
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

"""


@income.route("/delete/<id>")
def delete(id: int):
    income = Income.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()
    return redirect(url_for("income.list"))
