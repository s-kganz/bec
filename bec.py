from flask import Flask, request, session, flash, redirect, render_template

from forms import OrderForm

from secrets.config import Config, TestingConfig, DebugConfig

app = Flask(__name__)
app.secret_key = "Who knows?"
app.config.from_object(TestingConfig)

# Conditional import for working with dummy database
if app.config["DEBUG"]:
    from db_helper import MockHelper as DBHelper
else:
    from db_helper import DBHelper

DB = DBHelper()

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