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
                password="Shaurya@1234",
                database="StockPredictionAppDB"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            exit(1)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        try:
            hashed_password = self.hash_password(password)
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            self.cursor.execute(query, (username, hashed_password))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error registering user: {err}")
            return False

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.connect_to_database()
        return Builder.load_file('registration.kv')

    def navigate_to_login(self):
        self.root.clear_widgets()
        self.root.add_widget(Builder.load_file('login.kv'))

    def register(self):
        username = self.root.ids.reg_user.text
        password = self.root.ids.reg_password.text
        confirm_password = self.root.ids.confirm_password.text

        if password != confirm_password:
            self.root.ids.reg_page.text = "Passwords do not match!"
            return

        if self.register_user(username, password):
            self.root.ids.reg_page.text = f'Registration successful, {username}!'
            self.navigate_to_login()
        else:
            self.root.ids.reg_page.text = "Registration failed!"

    def clear_registration_fields(self):
        self.root.ids.reg_page.text = "Registration Page"
        self.root.ids.reg_user.text = ""
        self.root.ids.reg_password.text = ""
        self.root.ids.confirm_password.text = ""

if __name__ == "__main__":
    StockPredictionApp().run()
