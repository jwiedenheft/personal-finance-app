from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    SelectField,
    StringField,
    TextAreaField,
    DecimalField,
    SubmitField,
)
from wtforms.validators import DataRequired


class IncomeForm(FlaskForm):
    title = StringField("Title:")
    date = DateField("Date:", validators=[DataRequired()])
    notes = TextAreaField("Notes:")
    amount = DecimalField("Amount:", default=0, validators=[DataRequired()])
    type = SelectField(
        "Income Type:",
        choices=[("standard", "Standard Split"), ("paycheck", "Paycheck")],
    )
    submit = SubmitField("Next")
