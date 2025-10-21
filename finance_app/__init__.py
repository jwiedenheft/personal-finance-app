import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from finance_app.login import setup_login
from config import Config
import logging
from finance_app.scheduler import FlaskScheduler

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
scheduler = FlaskScheduler()


def create_app(config_class=Config):
    if not os.path.exists("logs"):
        os.mkdir("logs")

    logging.basicConfig(filename="logs/finance_app.log", level=logging.INFO)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)
    login.init_app(app)
    setup_login(app, login)

    from finance_app.routes import main as main_bp
    from finance_app.routes import expenses as expenses_bp
    from finance_app.routes import income as income_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(income_bp)

    @app.shell_context_processor
    def make_shell_context():
        return {"db": db}

    @app.template_filter("int_to_money")
    def int_to_money(cents: int):  # noqa: F811
        amt = cents / 100
        if amt < 0:
            return f"-${abs(amt):,.2f}"
        else:
            return f"${amt:,.2f}"

    @app.template_filter("format_date")
    def format_date(date):  # noqa: F811
        if date:
            return date.strftime("%m/%d/%y")
        return ""

    return app


from . import models  # noqa: E402, F401
