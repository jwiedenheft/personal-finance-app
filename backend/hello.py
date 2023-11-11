from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)

password = ""
with open("/run/secrets/db-password") as file:
    password = file.read()

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{password}@db/finances"

db = SQLAlchemy(app)


class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(60))


@app.route("/")
def listBlog():
    out = "Blog posts:"
    for blog_post in BlogPost.query.all():
        out += blog_post.title
        out += "<br>"
    return out


if __name__ == "__main__0":
    with app.app_context():
        db.create_all()

    app.run()
