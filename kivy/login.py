from kivy.lang import Builder
from kivymd.app import MDApp
import mysql.connector
import hashlib
from kivy.uix.screenmanager import ScreenManager, Screen
from home import HomeScreen  # Importing our HomeScreen class

class StockPredictionApp(MDApp):

    def connect_to_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Shaurya@1234",  # You should never hardcode passwords; this is just for demonstration
                database="StockPredictionAppDB"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            exit(1)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_credentials(self, username, password):
        hashed_password = self.hash_password(password)
        query = "SELECT username FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, hashed_password))
        user = self.cursor.fetchone()
        return user is not None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.connect_to_database()
        
        # Load the KV file for the login screen
        return Builder.load_file('login.kv')

    def navigate_to_home(self):
        try:
            sm = self.root.ids.sm  # Assuming you have a ScreenManager in your kv file with an id of 'sm'
            sm.switch_to(HomeScreen())
        except Exception as e:
            print(f"An error occurred while navigating to home: {e}")

    def login(self):
        # Your login logic remains unchanged
        pass

    def clear_login_fields(self):
        # Your clearing fields logic remains unchanged
        pass

    def logger(self):
        print("Logger method called!")
        self.navigate_to_home()

if __name__ == "__main__":
    StockPredictionApp().run()
