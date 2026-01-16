import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysqlm@0nty",  # replace with your actual Workbench password
        database="register",
        port=3306
    )
    return conn



