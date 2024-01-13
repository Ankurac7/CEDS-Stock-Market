from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.graphics import Color, Rectangle

class StockPredictionApp(MDApp):
<<<<<<< HEAD:kivy/temp/main.py
=======
    def connect_to_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ankur123",
                database="StockPredictionAppDB"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            exit(1)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
>>>>>>> ada92d98800f54fe98f0fb9fb99764da469f7037:home.py

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return RootLayout()

class RootLayout(MDBoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        
      
        self.search_bar = MDTextField(
            hint_text="Enter stock symbol...",
            helper_text="e.g., AAPL for Apple Inc.",
            mode="rectangle",
            line_color_normal=(0, 0, 0, 1),  
            line_color_focus=(0, 0, 0, 1)    
        )

        self.add_widget(self.search_bar)
        
        self.graph_placeholder = MDLabel(
            text="Graph will be plotted here",
            halign="center",
            valign="middle"
        )
        self.add_widget(self.graph_placeholder)
        
        self.current_stock_details = MDLabel(
            text="Current stock details will be shown here",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=100
        )
        self.add_widget(self.current_stock_details)
        
        fetch_button = MDRaisedButton(text="Fetch Stock Details", pos_hint={'center_x': 0.5})
        fetch_button.bind(on_release=self.fetch_stock_details)
        self.add_widget(fetch_button)

    def fetch_stock_details(self, instance):
        self.current_stock_details.text = "Example Stock Details:\nSymbol: AAPL\nPrice: $150.50\nVolume: 10M"

if __name__ == '__main__':
    StockPredictionApp().run()
