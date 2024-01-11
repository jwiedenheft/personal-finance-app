from flask import Blueprint

income = Blueprint(
    "income", __name__, url_prefix="/income", template_folder="templates"
)

from . import routes  # noqa: E402, F401
