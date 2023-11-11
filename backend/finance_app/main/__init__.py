from flask import Blueprint

main = Blueprint("main", __name__)

from finance_app.main import routes  # noqa: E402, F401
