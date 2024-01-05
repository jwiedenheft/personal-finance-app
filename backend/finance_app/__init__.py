from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    password = ""
    try:
        with open("/run/secrets/db-password") as file:
            password = file.read()
    except:
        pass

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://root:{password}@db/finances"

    db.init_app(app)
    migrate.init_app(app, db)

    from finance_app.main import main as main_bp

    app.register_blueprint(main_bp)

    return app


from . import models  # noqa: E402, F401
