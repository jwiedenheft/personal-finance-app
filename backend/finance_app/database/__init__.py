from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from . import models  # noqa: F401, E402
