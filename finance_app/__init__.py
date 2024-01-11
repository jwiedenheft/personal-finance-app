from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from finance_app.main import main as main_bp
    from finance_app.expenses import expenses as expenses_bp
    from finance_app.income import income as income_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(income_bp)

    @app.shell_context_processor
    def make_shell_context():
        return {"db": db}

    return app


from . import models  # noqa: E402, F401
