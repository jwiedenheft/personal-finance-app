from flask import Flask
from finance_app.database import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    password = ""
    with open("/run/secrets/db-password") as file:
        password = file.read()

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://root:{password}@db/finances"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from finance_app.main import main as main_bp

    app.register_blueprint(main_bp)

    return app
