# database.py

import mysql.connector
import hashlib

class DatabaseHandler:
    def __init__(self):
        self.connect_to_database()

    def connect_to_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Shaurya@1234",
                database="StockPredictionAppDB"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            exit(1)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
