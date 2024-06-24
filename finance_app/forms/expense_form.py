from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    StringField,
    TextAreaField,
    DecimalField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired


class ExpenseForm(FlaskForm):
    date = DateField("Date:", validators=[DataRequired()])
    title = StringField("Title:")
    notes = TextAreaField("Notes:")
    amount = DecimalField("Amount:", default=0, validators=[DataRequired()])
    category = SelectField("Category:")
    tags = StringField("Tags (seperate with semicolons):")
    submit = SubmitField("Submit")
