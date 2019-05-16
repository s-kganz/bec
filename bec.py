from flask import Flask, request, session, flash, redirect, render_template
from flask_login import current_user, login_user
from forms import OrderForm, LoginForm
from os import urandom as make_key

from secrets.config import Config, TestingConfig, DebugConfig

app = Flask(__name__)
app.secret_key = make_key(16)
app.config.from_object(TestingConfig)

# Conditional import for working with dummy database
if app.config["DEBUG"]:
    from db_helper import MockHelper as DBHelper
else:
    from db_helper import DBHelper

from db_helper import login_manager
login_manager.init_app(app)
login_manager.login_view='login'

DB = DBHelper()

@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check credentials
        user, result = DB.check_passhash(form.user.data, form.password.data)
        if not result:
            flash("Invalid login credentials.")
            return render_template("login.html", form=form)
        else:
            # Credentials passed!
            login_user(user)
            flash("Successfully logged in.")
            return render_template("home.html")
    return render_template("login.html", form=form)

@app.route('/order', methods=["POST", "GET"])
def getOrder():
    form = OrderForm()
    if form.validate_on_submit():
        DB.add_order(form.name.data,
                     form.location.data,
                     form.pickup.data,
                     form.bec.data,
                     form.ec.data,
                     form.be.data,
                     form.comments.data)
        flash("Thank you for your order!")
        return redirect('/')
    return render_template("order.html", form=form)


@app.route('/', methods=['GET'])
def hello():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='localhost', port=5000)