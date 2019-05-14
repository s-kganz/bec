from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional, NumberRange

MAX_SANDWICHES = 10

class OrderForm(FlaskForm):
    name = StringField("Order Name", validators=[DataRequired()])
    location = StringField("Delivery Location", validators=[DataRequired()])

    sandChoices = [(str(i), i) for i in range(0, MAX_SANDWICHES+1)]

    bec = SelectField(label="BECs: ", choices=sandChoices)
    ec = SelectField(label="ECs: ", choices=sandChoices)
    be = SelectField(label="BEs: ", choices=sandChoices)

    comments = TextAreaField(
        "Other comments/requests:", validators=[Optional()])
