from db_helper import login_manager
from flask import Flask, request, session, flash, redirect, render_template
from flask_login import current_user, login_user, login_required
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

login_manager.init_app(app)
login_manager.login_view = 'login'

DB = DBHelper()


@app.route('/login', methods=["POST", "GET"])
def login():
    ''' 
    Login view. Uses flask-wtf form to record user/pass in
    plaintext, then uses werkzeug hash function to 
    compare with hash stored in database. 
    '''
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
def get_order():
    ''' 
    Sandwich order view. Fill out simple form with name,
    pickup location, etc. and then add to DB.
    '''
    form = OrderForm()
    order_id = None
    if form.validate_on_submit():
        order_id = DB.add_order(form.name.data,
                                form.location.data,
                                form.pickup.data,
                                form.bec.data,
                                form.ec.data,
                                form.be.data,
                                form.comments.data,
                                form.recurring.data)
        flash("Thank you for your order! Your order number is {}".format(order_id))
        return redirect('/')
    return render_template("order.html", form=form)

@app.route('/cancel', methods=["GET", "POST"])
@login_required
def cancel_order():
    '''
    Search for order by name, cancel if desired.
    '''
    orderlist = []
    try:
        if request.form['name']:
            # Query database for order with that name, display
            orderlist = DB.get_orders_by_name(request.form['name'])
            if len(orderlist) == 0:
                flash("No orders found for {}".format(request.form['name']))
            else:
                # Store searched name as cookie to delete later
                session['search_name'] = request.form['name']
    except:
        pass
    
    return render_template('cancel.html', orderlist=orderlist)

@app.route('/cancelorder', methods=["GET"])
@login_required
def cancel_order_by_name():
    '''
    Call DB wrapper to remove all orders matching the given name
    '''
    if 'search_name' in session:
        DB.delete_orders_by_name(session['search_name'])
        flash("Order for {} deleted successfully.".format(session['search_name']))
    else:
        flash("Failed to delete order.")
    return redirect('/')

@app.route('/allorders', methods=["GET"])
@login_required
def show_all_orders():
    '''
    Retrieve all orders in database and present them as HTML table,
    ordered by time.
    '''
    orders_by_time = DB.get_orders_by_time()
    return render_template("all_orders.html", orders=orders_by_time)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host='localhost', port=5000)
