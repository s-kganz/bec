import pymysql
import random
from secrets.dbconfig import db_pass, db_user

'''
Generate a decent-sized order database for testing.
'''

# First generate the database
places = ["Troy", "Redmond", "NYC", "SF", "China"]
fname = ["Joe", "John", "Mary", "Sue", "Beth"]
lname = ["Ganz", "Lee", "Smith", "Jenkins"]
times = ["08:00", "08:30", "09:00", "09:30"]

orders = []

for i in range(30):
    loc = random.choice(places)
    name = random.choice(fname) + random.choice(lname)
    time = random.choice(times)
    bec = random.randrange(0, 11)
    ec = random.randrange(0, 11)
    be = random.randrange(0, 11)
    rec = random.choice([False, False, False, True])
    line = " ".join([name, loc, time, str(bec), str(ec), str(be), str(int(rec))])
    orders.append(line)

connection = pymysql.connect(host='localhost',
                             user=db_user,
                             password=db_pass,
                             db="bec")


try:
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM orders;")
        connection.commit()
        for line in orders:
            fields = line.split(' ')
            command = """INSERT INTO orders 
                         (name, location, pickup_time, bec_count, ec_count, be_count, recurring)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(command, fields)
            connection.commit()
except Exception as e:
    print(e)
finally:
    connection.close()
