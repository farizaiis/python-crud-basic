import mysql.connector

def db_connect():
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'learning_mysql'
    )
    return db