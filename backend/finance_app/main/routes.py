from finance_app.main import main


@main.route("/")
def index():
    return "Hello world!"
