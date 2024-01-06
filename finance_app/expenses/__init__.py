from flask import Blueprint

expenses = Blueprint(
    "expenses", __name__, url_prefix="/expenses", template_folder="templates"
)

from . import routes  # noqa: E402, F401
