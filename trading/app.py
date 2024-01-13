import sys
import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal

# Define the thread to fetch data
class FetchDataThread(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        try:
            df = yf.download(self.user_input, start='2023-01-01', end='2023-12-31')
            data = {
                'description': df.describe().to_string(),
                'columns': df.columns.tolist(),
                'close': df['Close'].tolist() if 'Close' in df.columns else None
            }
            self.signal.emit(data)
        except Exception as e:
            self.signal.emit({'error': str(e)})

# Candlestick chart in a separate window
class CandlestickWindow(QWidget):
    def __init__(self, df, ticker):
        super().__init__()
        self.setWindowTitle(f'Candlestick Chart for {ticker}')
        df.index.name = 'Date'
        mpf.plot(df, type='candle', style='yahoo', title=f'Candlestick Chart for {ticker}', volume=True, show_nontrading=True, axtitle=f"{ticker} Stock Price")
        layout = QVBoxLayout(self)
        self.setLayout(layout)

# Main application class
class StockPredictionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Stock Prediction Desktop App')
        self.setGeometry(100, 100, 1200, 800)

        self.input_label = QLabel('Enter Stock Ticker (e.g., HDFCBANK.NS):', self)
        self.input_text = QLineEdit(self)
        self.input_text.setText('HDFCBANK.NS')

        self.submit_button = QPushButton('Fetch Data', self)
        self.submit_button.clicked.connect(self.start_fetching_data)

        self.output_text = QTextEdit(self)

        self.macd_crossover_button = QPushButton('Show MACD Crossover Graph', self)
        self.macd_crossover_button.clicked.connect(self.plot_macd_crossover_graph)

        self.macd_signal_graph_button = QPushButton('Show MACD & Signal Line Graph', self)
        self.macd_signal_graph_button.clicked.connect(self.plot_macd_and_signal_line_graph)

        self.candlestick_chart_button = QPushButton('Show Candlestick Chart', self)
        self.candlestick_chart_button.clicked.connect(self.plot_candlestick_chart)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.output_text)
        self.layout.addWidget(self.macd_crossover_button)
        self.layout.addWidget(self.macd_signal_graph_button)
        self.layout.addWidget(self.candlestick_chart_button)
        self.setLayout(self.layout)

    def start_fetching_data(self):
        user_input = self.input_text.text()
        self.output_text.clear()
        self.output_text.append("Fetching data... Please wait.")
        self.thread = FetchDataThread(user_input)
        self.thread.signal.connect(self.display_data)
        self.thread.start()

    def display_data(self, data):
        self.output_text.clear()
        if 'error' in data:
            self.output_text.append(f"Error: {data['error']}")
        else:
            self.output_text.append(f"Data for 2023-01-01 to 2023-12-31:\n{data['description']}\n")
            self.output_text.append(f"Available Columns: {data['columns']}\n")

    def plot_macd_crossover_graph(self):
        user_input = self.input_text.text()
        df = yf.download(user_input, start='2023-01-01', end='2023-12-31')
        df['12_EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['26_EMA'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['12_EMA'] - df['26_EMA']
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

        # Simulate investing based on MACD crossovers
        df['Position'] = 0
        df.loc[df['MACD'] > df['Signal_Line'], 'Position'] = 1
        df['Investment'] = df['Position'].shift(1) * df['Close']

        # Calculate cumulative returns
        df['Cumulative_Returns'] = (1 + (df['Close'].pct_change() * df['Position'])).cumprod()

        # Plot cumulative returns
        plt.figure(figsize=(14, 7))
        plt.title('Cumulative Returns Based on MACD Crossovers')
        df['Cumulative_Returns'].plot()
        plt.ylabel('Cumulative Returns')
        plt.xlabel('Date')
        plt.grid(True)
        plt.show()
        
    def plot_macd_and_signal_line_graph(self):
        user_input = self.input_text.text()
        df = yf.download(user_input, start='2023-01-01', end='2023-12-31')
        df['12_EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['26_EMA'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['12_EMA'] - df['26_EMA']
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

        plt.figure(figsize=(14, 7))
        plt.title('MACD Crossover Graph')
        plt.plot(df.index, df['MACD'], label='MACD', color='blue')
        plt.plot(df.index, df['Signal_Line'], label='Signal Line', color='red')
        plt.legend()
        plt.show()
        
    def plot_candlestick_chart(self):
        user_input = self.input_text.text()
        df = yf.download(user_input, start='2023-01-01', end='2023-12-31')
        candlestick_window = CandlestickWindow(df, user_input)
        candlestick_window.setGeometry(200, 200, 1200, 600)
        candlestick_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = StockPredictionApp()
    ex.show()
    sys.exit(app.exec_())
