# utils/db_utils.py

import mysql.connector

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="capstone_project"
    )
