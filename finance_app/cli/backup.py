from flask import Blueprint
import click
import os
import shutil
import gzip
from datetime import datetime
import config

backup_bp = Blueprint("backup", __name__)


@backup_bp.cli.command("db")
@click.argument("destination", required=False, default="backups")
def backup_db(destination):
    """Backup the SQLite database to the specified destination folder.
    The backup file is named {timestamp}.db.gz (gzip compressed).

    Usage: `flask backup db [DESTINATION]`
    """
    dest_path = os.path.abspath(destination)
    os.makedirs(dest_path, exist_ok=True)

    db_uri = config.Config.SQLALCHEMY_DATABASE_URI
    if db_uri.startswith("sqlite:///"):
        src_path = db_uri[len("sqlite:///") :]
    else:
        click.echo("Backup currently supports only SQLite databases.")
        return

    if not os.path.exists(src_path):
        click.echo(f"Source database not found at {src_path}")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(dest_path, f"{timestamp}.db.gz")

    try:
        # Copy and gzip compress
        with open(src_path, "rb") as f_in, gzip.open(backup_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        click.echo(f"Database backup created at {backup_file}")
    except Exception as e:
        click.echo(f"Failed to backup database: {e}")
