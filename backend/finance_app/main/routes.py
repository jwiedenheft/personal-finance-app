from finance_app.main import main
from finance_app.database.models import Expense


@main.route("/")
def index():
    spends = Expense.query.all()
    out = ""
    spend: Expense
    for spend in spends:
        out += f"{spend.title} | "
        +f"Amount: {spend.amount} "
        +f"Category: {spend.category} "
        +f"Tags: {", ".join([t.tag.name for t in spend.tags])}<br>"
    return out
