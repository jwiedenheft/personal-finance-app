from flask import Flask, redirect, render_template, request, url_for
from flask_login import UserMixin, login_user, logout_user
import os


class User(UserMixin):
    id: str

    def __init__(self, id) -> None:
        self.id = id


users = {"main": User("main")}


def setup_login(app: Flask, login):

    @login.user_loader
    def load_user(user_id):
        return users[user_id]

    @app.route("/login", methods=["GET", "POST"])
    def login():
        password = request.form.get("password") or ""
        if password == os.environ.get("PASSWORD"):
            login_user(users["main"])
            return redirect(url_for("main.dashboard"))
        else:
            app.logger.info("Incorrect password or no password!")
            return render_template("login.html")

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("login"))
