from kivy.lang import Builder
from kivymd.app import MDApp
import mysql.connector
import hashlib

class StockPredictionApp(MDApp):

    def connect_to_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ankur123",
                database="StockPredictionAppDB",
                auth_plugin='mysql_native_password'
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            exit(1)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_credentials(self, username, password):
        try:
            hashed_password = self.hash_password(password)
            query = "SELECT username FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, hashed_password))
            user = self.cursor.fetchone()
            return user is not None
        except mysql.connector.Error as err:
            print(f"Error verifying credentials: {err}")
            return False

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.connect_to_database()
        return Builder.load_file('login.kv')

    def navigate_to_home(self):
        if self.root is not None:
            home_widget = Builder.load_file('home.kv')
            if home_widget is not None:
                self.root.add_widget(home_widget)
            else:
                print("Error loading 'home.kv'")
        else:
            print("Error: App root is None")


    def logger(self):
        username = self.root.ids.user.text
        password = self.root.ids.password.text
        if self.verify_credentials(username, password):
            self.root.ids.login_page.text = f'Welcome, {username}!'
            self.navigate_to_home()
        else:
            self.root.ids.login_page.text = "Invalid credentials!"

    def clear(self):
        self.root.ids.login_page.text = "Login Page"
        self.root.ids.user.text = ""
        self.root.ids.password.text = ""

if __name__ == "__main__":
    StockPredictionApp().run()
