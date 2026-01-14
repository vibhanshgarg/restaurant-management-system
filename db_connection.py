import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # change if needed
        password="admin123",  # change if needed
        database="mydata"
    )
