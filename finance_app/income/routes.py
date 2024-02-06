from flask import current_app, redirect, render_template, url_for, request
from finance_app.income.forms.income_categories_form import CategoryIncomesForm
from finance_app.income.forms.income_form import IncomeForm
from finance_app.models import Category, CategoryIncome, Expense, Income
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


@income.route("/new", methods=["GET", "POST"])
def new():
    form = IncomeForm()
    form.type.choices += [
        (f"only-{cat.code}", f"Single-Category: {cat.code}")
        for cat in Category.query.all()
    ]
    if form.validate_on_submit():
        total = int(form.amount.data * 100)
        income = Income(
            date=form.date.data,
            title=form.title.data,
            notes=form.notes.data,
        )

        if form.type.data == "standard":
            god_amount = int(total / 10)
            save_amount = int(total * 0.8)
            spend_amount = total - (god_amount + save_amount)
            income.category_incomes.append(
                CategoryIncome(category=Category.query.get("GOD"), amount=god_amount)
            )
            income.category_incomes.append(
                CategoryIncome(
                    category=Category.query.get("SAVING"), amount=save_amount
                )
            )
            income.category_incomes.append(
                CategoryIncome(
                    category=Category.query.get("SPENDING"), amount=spend_amount
                )
            )
        elif form.type.data == "paycheck":
            rent_amount = 350 * 100
            insurance_amount = int(43.84 * 100)
            retirement_amount = int(106.60 * 100)
            full_total = total + rent_amount + insurance_amount + retirement_amount
            god_amount = int(full_total / 10)
            save_amount = int(full_total * 0.8)
            spend_amount = full_total - (god_amount + save_amount)
            income.category_incomes.append(
                CategoryIncome(category=Category.query.get("GOD"), amount=god_amount)
            )
            income.category_incomes.append(
                CategoryIncome(
                    category=Category.query.get("SAVING"), amount=save_amount
                )
            )
            income.category_incomes.append(
                CategoryIncome(
                    category=Category.query.get("SPENDING"), amount=spend_amount
                )
            )
            db.session.add(
                Expense(
                    title="Rent",
                    date=form.date.data,
                    category=Category.query.get("SAVING"),
                    # tags="Life; Housing",
                    amount=rent_amount,
                )
            )
            db.session.add(
                Expense(
                    title="Health Insurance",
                    date=form.date.data,
                    category=Category.query.get("SAVING"),
                    # tags="Life;Insurance",
                    amount=insurance_amount,
                )
            )
            db.session.add(
                Expense(
                    title="Retirement Investment",
                    date=form.date.data,
                    category=Category.query.get("SAVING"),
                    # tags="Life;Investment",
                    amount=retirement_amount,
                )
            )
        db.session.add(income)
        db.session.commit()

        return redirect(url_for("income.list"))
    return render_template("new_income.html", form=form)


@income.route("/delete/<id>")
def delete(id: int):
    income = Income.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()
    return redirect(url_for("income.list"))
