import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional, NumberRange

MAX_SANDWICHES = 10

class OrderForm(FlaskForm):
    name = StringField("Order Name", validators=[DataRequired()])
    location = StringField("Delivery Location", validators=[DataRequired()])

    sandChoices = [(str(i), i) for i in range(0, MAX_SANDWICHES+1)]
    timeChoices = []
    # 7:30 AM start time, have deliveries every half-hour
    start = datetime.datetime(2000, 1, 1, 7, 30, 0)
    for i in range(0, 4):
        start = start + datetime.timedelta(minutes=30)
        timestr = start.strftime("%H:%M")
        timeChoices.append((timestr, timestr)) # needs to be tuple of str
    
    pickup = SelectField(label="Pickup time: ", 
                         choices=timeChoices,
                         validators=[DataRequired()])


    bec = SelectField(label="BECs: ", choices=sandChoices)
    ec = SelectField(label="ECs: ", choices=sandChoices)
    be = SelectField(label="BEs: ", choices=sandChoices)

    comments = TextAreaField(
        "Other comments/requests:", validators=[Optional()])
