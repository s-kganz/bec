import pymysql
from secrets.dbconfig import db_pass, db_user, bec_user, bec_pass
from werkzeug.security import generate_password_hash, check_password_hash

connection = pymysql.connect(host="localhost",
                             user=db_user,
                             password=db_pass)

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
                                                       recurring BOOLEAN DEFAULT FALSE,
                                                       ts TIMESTAMP NOT NULL,
                                                       PRIMARY KEY (id))
             """
        cursor.execute(sql)
        # Create user table
        # These are all trusted users that can access the backend
        sql = """CREATE TABLE IF NOT EXISTS bec.users(user VARCHAR(12) NOT NULL,
                                                      passhash VARCHAR(200) NOT NULL,
                                                      ts TIMESTAMP NOT NULL,
                                                      id INT AUTO_INCREMENT NOT NULL,
                                                      PRIMARY KEY (id))
              """
        cursor.execute(sql)

        # Add admin user to table, for now this will be the only entry for
        # using backend operations
        sql = """ INSERT INTO bec.users (user, passhash) VALUES
                  (%s, %s); """
        cursor.execute(sql, (bec_user, generate_password_hash(bec_pass)))

        # Create statistics table, this tracks how many sandwiches were ordered from
        # week to week

        # New rows should be inserted here whenever non-recurring orders are purged
        # Thursday night.
        #TODO make script that purges orders, updates this table
        sql = """CREATE TABLE IF NOT EXISTS bec.stats(id INT AUTO_INCREMENT NOT NULL,
                                                      week DATE NOT NULL,
                                                      bec_count INT UNSIGNED NOT NULL,
                                                      ec_count INT UNSIGNED NOT NULL,
                                                      be_count INT UNSIGNED NOT NULL,
                                                      custom_count INT UNSIGNED NOT NULL,
                                                      PRIMARY KEY (id))
              """

    connection.commit()
finally:
    connection.close()