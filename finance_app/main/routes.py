from flask import render_template
from finance_app.main import main
from finance_app.models import Category
from finance_app.utils import int_to_money


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/list_categories")
def list_categories():
    categories = Category.query.all()
    return render_template("list_categories.html", categories=categories)


@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", categories=Category.query.all())
