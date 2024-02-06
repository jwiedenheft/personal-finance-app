from flask import redirect, render_template, url_for
from finance_app.main import main
from finance_app.models import Category


@main.route("/")
def index():
    return redirect(url_for("main.dashboard"))


@main.route("/list_categories")
def list_categories():
    categories = Category.query.all()
    return render_template("list_categories.html", categories=categories)


@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", categories=Category.query.all())
