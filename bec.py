from flask import Flask, request, session, flash, redirect, render_template
from forms import OrderForm

app = Flask(__name__)
app.secret_key = "Who knows?"

@app.route('/order', methods=["POST", "GET"])
def getOrder():
    form = OrderForm()
    if form.validate_on_submit():
        #TODO add order to database
        flash("Thank you for your order!")
        return redirect('/')
    return render_template("order.html", form=form)


@app.route('/', methods=['GET'])
def hello():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host='localhost', port=5000)