from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    formName = "Item form"
    itemType = SelectField(
        "Sandwich Type",
        choices=[
            ("bec", "Bacon Egg and Cheese"),
            ("ec", "Egg and Cheese"),
            ("other", "Custom Order"),
        ],
        validators=[DataRequired()]
    )
    comment = StringField("Requests", validators=None)
