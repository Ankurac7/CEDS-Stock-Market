import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder

SYMBOL = 'HDFCBANK.NS'
START_DATE = '2023-01-01'
END_DATE = '2023-12-31'

Builder.load_file("home.kv")

class StockPredictionApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        return RootLayout()

class RootLayout(MDBoxLayout):
    
    class RootLayout(MDBoxLayout):
        # ... (other methods)

        def show_stock_dropdown(self):
            stock_items = ["HDFC"]

        # Create menu items with on_release set appropriately
            menu_items = [{"viewclass": "OneLineListItem", "text": f"{item}", "on_release": lambda x=item: self.on_stock_dropdown_select(x)} for item in stock_items]

            menu = MDDropdownMenu(
                caller=self.ids.search_bar,
                items=menu_items,
                width_mult=4,
            )

            menu.open()



    def on_stock_dropdown_select(self, instance_menu_item):
        selected_stock = instance_menu_item.text
        stock_symbol = selected_stock.split(" - ")[0]
        self.ids.search_bar.text = stock_symbol


    def fetch_stock_details(self):
        stock_symbol = self.ids.search_bar.text

        if not stock_symbol:
            self.show_error_popup("Please enter a stock symbol.")
            return

        try:
            stock_data = data.DataReader(stock_symbol, 'yahoo', START_DATE, END_DATE)
            prediction = np.random.randn(len(stock_data))
            self.update_stock_ui(stock_data, prediction)

        except Exception as e:
            self.show_error_popup(f"Error fetching stock details: {str(e)}")

    @mainthread
    def update_stock_ui(self, stock_data, prediction):
        self.ids.current_stock_details.text = f"Current stock details for {stock_data.index[-1].strftime('%Y-%m-%d')}:\n" \
                                              f"Close Price: {stock_data['Close'].iloc[-1]:.2f}\n" \
                                              f"Prediction: {prediction[-1]:.2f}"
        self.plot_stock_data(stock_data.index, stock_data['Close'], prediction)

    def plot_stock_data(self, dates, close_prices, predictions):
        plt.figure(figsize=(10, 5))
        plt.plot(dates, close_prices, label='Actual Close Price')
        plt.plot(dates, predictions, label='Predicted Close Price', linestyle='dashed')
        plt.title('Stock Price Prediction')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.grid(True)
        plt.savefig('stock_prediction_plot.png')
        plt.close()
        self.show_plot_popup()

    def show_plot_popup(self):
        popup = Popup(title='Stock Prediction Plot', size_hint=(None, None), size=(400, 400))
        plot_image = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    Image:
        source: 'stock_prediction_plot.png'
''')
        popup.content = plot_image
        popup.open()

    def show_error_popup(self, message):
        popup = Popup(title='Error', content=MDLabel(text=message), size_hint=(None, None), size=(300, 150))
        popup.open()

if __name__ == '__main__':
    StockPredictionApp().run()
