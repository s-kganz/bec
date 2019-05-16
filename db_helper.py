from flask_login import LoginManager, UserMixin
import pymysql
from secrets.dbconfig import db_user, db_pass
from werkzeug.security import check_password_hash
import warnings

login_manager = LoginManager()

class User(UserMixin):
    ''' Class used to represent users '''

    def __init__(self, user, passhash):
        self.user = user
        self.passhash = passhash

    def get_id(self):
        # Strings in Python 3 are unicode by default, so
        # no need to encode
        return self.user


class DBHelper():
    ''' Helper class to run mysql operations in Python
        context '''

    @staticmethod
    def connection(database="bec"):
        ''' Create connection with database. Should
            be called for every change as opposed
            to having once continuous connection '''

        return pymysql.connect(user=db_user,
                               password=db_pass,
                               db=database)

    def add_order(self, name, location, pickup, bec, ec, be, comment):
        ''' Add a new sandwich order to database. '''
        sql = '''INSERT INTO orders (name, location, pickup_time, bec_count, ec_count, be_count, comment)
               VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        conn = self.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql, (name, location, pickup, bec, ec, be, comment))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def clear_all(self):
        ''' Clear all entries from database '''
        warnings.warn("REMOVING ALL ENTRIES FROM ORDERS TABLE")
        conn = self.connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM orders;"
                cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def check_passhash(self, user, password):
        # Get user object
        u = get_user(user)
        if not u:
            return u, False
        # Securely compare
        return u, check_password_hash(u.passhash, password)

class MockHelper():
    @staticmethod
    def connection():
        return None
    def add_order(self, name, location, pickup, bec, ec, be, comment):
        pass
    def clear_all(self):
        pass
    def check_passhash(self, user, password):
        return password == '1234'

@login_manager.user_loader
def get_user(username):
        ''' Query user table for username and return new User object if found '''
        conn = DBHelper.connection()
        if not conn:
            # Assume using dummy database
            return User("John Smith", '1234')
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM users WHERE user=%s;"
                # comma makes param a tuple, which is required
                cursor.execute(sql, (username,))
                result = cursor.fetchall()  # Returns a list of dicts
                if len(result) == 1:
                    # Make a user from columns
                    return User(result[0]['user'], result[0]['passhash'])
                else:
                    return None
        except Exception as e:
            print(e)
        finally:
            conn.close()
