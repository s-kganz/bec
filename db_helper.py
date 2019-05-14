import pymysql
from secrets.dbconfig import username, password
import warnings

class DBHelper():
    ''' Helper class to run mysql operations in Python
        script '''
    
    def connection(self, database="bec"):
        ''' Create connection with database. Should
            be called for every change as opposed
            to having once continuous connection '''

        return pymysql.connect(user=username,
                               password=password,
                               db=database)
    
    def add_order(self, name, location, bec, ec, be, comment):
        ''' Add a new sandwich order to database. '''
        sql = '''INSERT INTO orders (name, location, bec_count, ec_count, be_count, comment)
               VALUES (%s, %s, %s, %s, %s, %s);'''
        conn = self.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (name, loc, bec, ec, be, comment))
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
