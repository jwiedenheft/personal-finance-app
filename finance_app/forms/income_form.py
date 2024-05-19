from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    StringField,
    TextAreaField,
    DecimalField,
    SubmitField,
    SelectField,
)
from wtforms.validators import DataRequired


class IncomeForm(FlaskForm):
    title = StringField("Title:")
    date = DateField("Date:", validators=[DataRequired()])
    notes = TextAreaField("Notes:")
    amount = DecimalField("Amount:", default=0, validators=[DataRequired()])
    category = SelectField("Category")
    submit = SubmitField("Submit")
