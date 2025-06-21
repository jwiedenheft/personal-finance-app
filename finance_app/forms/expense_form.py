from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    StringField,
    TextAreaField,
    DecimalField,
    SelectField,
    SubmitField,
    BooleanField,
    IntegerField,
)
from wtforms.validators import DataRequired


class ExpenseForm(FlaskForm):
    date = DateField("Date:", validators=[DataRequired()])
    title = StringField("Title:")
    notes = TextAreaField("Notes:")
    amount = DecimalField("Amount:", default=0, validators=[DataRequired()])
    category = SelectField("Category:")
    tags = StringField("Tags (seperate with semicolons):")

    # Repeatable
    repeatable = BooleanField("Enable Repeat:", default=False)
    repeat_scale = SelectField(
        "Repeat Every:",
        choices=[
            ("days", "Day(s)"),
            ("weeks", "Week(s)"),
            ("months", "Month(s)"),
            ("years", "Year(s)"),
        ],
    )
    repeat_increment = IntegerField()

    def validate_repeatable(self, field):
        if field.data and not self.repeat_scale.data:
            raise ValueError("Please specify a repeat scale!")
        if field.data and not self.repeat_increment.data:
            raise ValueError("Please specify a repeat increment!")

    submit = SubmitField("Submit")
