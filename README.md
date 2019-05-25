Flask application to handle breakfast sandwich orders.

Goals:

 - Make recurring, nonrecurring orders :white_check_mark:
 - Custom sandwiches (?)
 - Cancel orders :white_check_mark:
 - Administrative backend
   - Statistics
   - Generate list of orders :white_check_mark:
 - Cronjobs
   - Enforce time constraints on when orders can be placed
   - Purge database of nonrecurring orders weekly
 - Make decent-looking css

## Installation

Required packages (+ their dependencies):
 - pip
 - Flask
 - flask-login
 - flask-wtf
 - PyMySQL

Also need: MySQL

### Install Things

Pip ships with Python 3 on Windows by default. If you don`t have pip installed refer to [this page](https://pip.pypa.io/en/stable/installing/).

Install the above packages (in order!) with `pip install <package>` in Windows command prompt. Setting up a virtual environment for use with your IDE is useful.

MySQL runs in a standard linux terminal. Run the following to install it.
`sudo apt-get install mysql`

Start the server:
`sudo service mysql start`

Login as root user:
`mysql -u root -p`

Enter password when prompted (should be "" on startup, if not see [this guide](https://support.rackspace.com/how-to/mysql-resetting-a-lost-mysql-root-password/) on how to reset a MySQL password). If you reset the password, be sure to save it for db_config later.

### Configure the Database

In the directory where you cloned the repo create a folder called `secrets`. In it, create two Python files: `__init__.py` and `dbconfig.py`. This is where Flask will look for the password to login to the application and the MySQL server. The init file can remain empty. In `dbconfig.py` add the following:
```
db_user="root"
db_pass=""
bec_user="admin"
bec_pass=""
```
The passwords can be changed to whatever you want. Now with the MySQL server setup, we can setup the bec database. Run the `db_setup.py` script with:

```python db_setup.py```

### Set Flask Environment Variables

Flask can be started in multiple ways. You can either run `flask run bec.py` to start the app specifically or set the following environment variables to start in development mode with just `flask run`.
```
set FLASK_APP=bec.py
set FLASK_ENV=development
```

### View the Site!

Open your web browser and navigate to `127.0.0.1:5000` (or localhost) and you should see the page. To work with a larger database for testing run `make_db.py` to get a bunch of random names and orders.
