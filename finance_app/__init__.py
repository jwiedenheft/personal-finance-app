from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from finance_app.login import setup_login
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
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
        return "$" + str(cents / 100)

    return app


from . import models  # noqa: E402, F401
