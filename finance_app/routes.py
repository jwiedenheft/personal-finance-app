import csv
from io import StringIO
from flask import (
    Blueprint,
    Response,
    current_app,
    redirect,
    render_template,
    url_for,
    request,
)
from finance_app.forms.expense_form import ExpenseForm
from finance_app.forms.income_form import IncomeForm
from finance_app.models import Category, Expense, Income
from finance_app import db
from finance_app.utils import int_to_money
from flask_login import login_required


main = Blueprint("main", __name__, template_folder="templates")


@main.route("/")
@login_required
def index():
    return redirect(url_for("main.dashboard"))


@main.route("/list_categories")
@login_required
def list_categories():
    categories = Category.query.all()
    return render_template("list_categories.html", categories=categories)


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", categories=Category.query.all())


income = Blueprint(
    "income", __name__, url_prefix="/income", template_folder="templates"
)


@income.route("/list/")
@login_required
def list_income():
    page = request.args.get("page", 1, type=int)
    items_per_page = current_app.config.get("RESULTS_PER_PAGE") or 10

    income = Income.query.order_by(Income.date.desc()).paginate(
        page=page, per_page=items_per_page
    )

    next_url = None
    if income.has_next:
        next_url = url_for("income.list_income", page=income.next_num)
    prev_url = None
    if income.has_prev:
        prev_url = url_for("income.list_income", page=income.prev_num)

    return render_template(
        "list_income.html",
        income_items=income.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@income.route("/new", methods=["GET", "POST"])
@login_required
def new_income():
    form = IncomeForm()
    form.category.choices = [(c.code, c.title) for c in Category.query.all()]
    if form.validate_on_submit():
        total = int(form.amount.data * 100)
        income = Income(
            date=form.date.data,
            title=form.title.data,
            notes=form.notes.data,
            amount=total,
            category_code=form.category.data,
        )
        db.session.add(income)
        db.session.commit()

        return redirect(url_for("income.list_income"))
    return render_template("new_income.html", form=form)


@income.route("/new_paycheck", methods=["GET", "POST"])
@login_required
def new_paycheck():
    form: IncomeForm = IncomeForm()
    form.title.data = "Paycheck"
    form.category.choices = [(c.code, c.title) for c in Category.query.all()]
    form.category.data = "SPENDING"
    if form.validate_on_submit():
        total = int(form.amount.data * 100)
        adjusted_total = total + 35000 + 4384 + 10960
        god_amount = int(adjusted_total / 10)
        save_amount = int(total * 0.775)
        spend_amount = total - (god_amount + save_amount)

        db.session.add(
            Income(
                date=form.date.data,
                title=form.title.data,
                notes=form.notes.data,
                amount=god_amount,
                category_code="GOD",
            )
        )
        db.session.add(
            Income(
                date=form.date.data,
                title=form.title.data,
                notes=form.notes.data,
                amount=spend_amount,
                category_code="SPENDING",
            )
        )
        db.session.add(
            Income(
                date=form.date.data,
                title=form.title.data,
                notes=form.notes.data,
                amount=save_amount,
                category_code="SAVING",
            )
        )
        db.session.commit()

        return redirect(url_for("income.list_income"))
    return render_template("new_paycheck.html", form=form)


@income.route("/delete/<id>")
@login_required
def delete_income(id: int):
    income = Income.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()
    return redirect(url_for("income.list_income"))


expenses = Blueprint(
    "expenses", __name__, url_prefix="/expenses", template_folder="templates"
)


@expenses.route("/")
@login_required
def list_expenses():
    page = request.args.get("page", 1, type=int)
    items_per_page = current_app.config.get("RESULTS_PER_PAGE") or 10
    expenses = Expense.query.order_by(Expense.date.desc()).paginate(
        page=page, per_page=items_per_page
    )

    next_url = None
    if expenses.has_next:
        next_url = url_for("expenses.list_expenses", page=expenses.next_num)
    prev_url = None
    if expenses.has_prev:
        prev_url = url_for("expenses.list_expenses", page=expenses.prev_num)

    return render_template(
        "list_expenses.html",
        expenses=expenses.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@expenses.route("/new", methods=["GET", "POST"])
@login_required
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

        return redirect(url_for("expenses.list_expenses"))
    return render_template("new_expense.html", form=form)


@expenses.route("/delete/<id>")
@login_required
def delete_expense(id: int):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("expenses.list_expenses"))


@expenses.route("/export")
@login_required
def export_expenses():
    expenses: list[Expense] = Expense.query.all()  # noqa: F821
    csv_rows = [
        {
            "Date": expense.date.strftime("%m/%d/%Y"),
            "Title": expense.title,
            "Category": expense.category.title,
            "Amount": "-" + int_to_money(expense.amount),
            "Tags": ",".join([et.tag.name for et in expense.tags]),
        }
        for expense in expenses
    ]
    with StringIO() as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(csv_rows)
        return Response(file, mimetype="text/csv")
    # send_file(
    #        file, download_name="expenses.csv", , as_attachment=True
    #    )
