from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class CategoryIncomeForm(FlaskForm):
    category_name: str = ""
    percentage = IntegerField(
        label=f"Percentage for {category_name}:",
        validators=[DataRequired(), NumberRange(min=0, max=100)],
    )


class CategoryIncomesForm(FlaskForm):
    categories = FieldList(FormField(CategoryIncomeForm))
