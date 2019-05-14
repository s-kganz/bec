import pymysql
from secrets.dbconfig import password, username

connection = pymysql.connect(host="localhost",
                             user=username,
                             password=password)

try:
    with connection.cursor() as cursor:
        # Create database
        sql = "DROP DATABASE IF EXISTS bec"
        cursor.execute(sql)
        sql = "CREATE DATABASE IF NOT EXISTS bec"
        cursor.execute(sql)
        # Create order table
        sql = """CREATE TABLE IF NOT EXISTS bec.orders(id int NOT NULL AUTO_INCREMENT,
                                                       name VARCHAR(50) NOT NULL,
                                                       location VARCHAR(50) NOT NULL,
                                                       pickup_time TIME NOT NULL,
                                                       bec_count int UNSIGNED NOT NULL,
                                                       ec_count int UNSIGNED NOT NULL,
                                                       be_count int UNSIGNED NOT NULL,
                                                       comment VARCHAR(1000),
                                                       ts TIMESTAMP NOT NULL,
                                                       PRIMARY KEY (id))
             """
        cursor.execute(sql)
        # Create user table
        sql = """CREATE TABLE IF NOT EXISTS bec.users(user VARCHAR(12) NOT NULL,
                                                      passhash VARCHAR(100) NOT NULL,
                                                      ts TIMESTAMP NOT NULL,
                                                      PRIMARY KEY (user))
              """
        cursor.execute(sql)
    connection.commit()
finally:
    connection.close()