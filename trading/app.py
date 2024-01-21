import sys
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import qApp
import qdarkstyle  # Import QDarkStyle

class FetchDataThread(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, user_input, time_span):
        super().__init__()
        self.user_input = user_input
        self.time_span = time_span

    def run(self):
        try:
            # Modify the start and end dates based on the selected time span
            end_date = pd.to_datetime('today').strftime('%Y-%m-%d')
            if self.time_span == '1d':
                start_date = pd.to_datetime('today').strftime('%Y-%m-%d')
            elif self.time_span == '1wk':
                start_date = (pd.to_datetime('today') - pd.DateOffset(weeks=1)).strftime('%Y-%m-%d')
            elif self.time_span == '1mo':
                start_date = (pd.to_datetime('today') - pd.DateOffset(months=1)).strftime('%Y-%m-%d')
            elif self.time_span == '1y':
                start_date = (pd.to_datetime('today') - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
            elif self.time_span == '5y':
                start_date = (pd.to_datetime('today') - pd.DateOffset(years=5)).strftime('%Y-%m-%d')
            else:
                start_date = '1970-01-01'  # Show all data

            df = yf.download(self.user_input, start=start_date, end=end_date)
            data = {
                'description': df.describe().to_string(),
                'columns': df.columns.tolist(),
                'close': df['Close'].tolist() if 'Close' in df.columns else None
            }
            self.signal.emit(data)
        except Exception as e:
            self.signal.emit({'error': str(e)})

class CandlestickWindow(QWidget):
    def __init__(self, df, ticker):
        super().__init__()
        self.setWindowTitle(f'Candlestick Chart for {ticker}')
        df.index.name = 'Date'
        mpf.plot(df, type='candle', style='yahoo', title=f'Candlestick Chart for {ticker}', volume=True,
                 show_nontrading=True, axtitle=f"{ticker} Stock Price")
        layout = QVBoxLayout(self)
        self.setLayout(layout)

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
        self.input_text.setFixedSize(200, 30)

        self.time_span_label = QLabel('Select Time Span:', self)
        self.time_span_combobox = QComboBox(self)
        self.time_span_combobox.addItems(['1 day', '1 week', '1 month', '1 year', '5 years', 'All'])
        self.time_span_combobox.setFixedSize(200, 30)

        self.submit_button = QPushButton('Fetch Data', self)
        self.submit_button.clicked.connect(self.start_fetching_data)
        self.submit_button.setFixedSize(200, 30)

        self.output_text = QTextEdit(self)
        self.output_text.setFont(QFont("Arial", 12))

        self.macd_crossover_button = QPushButton('Show MACD Crossover Graph', self)
        self.macd_crossover_button.clicked.connect(self.plot_macd_crossover_graph)
        self.macd_crossover_button.setFixedSize(200, 30)

        self.macd_signal_graph_button = QPushButton('Show MACD & Signal Line Graph', self)
        self.macd_signal_graph_button.clicked.connect(self.plot_macd_and_signal_line_graph)
        self.macd_signal_graph_button.setFixedSize(200, 30)

        self.candlestick_chart_button = QPushButton('Show Candlestick Chart', self)
        self.candlestick_chart_button.clicked.connect(self.plot_candlestick_chart)
        self.candlestick_chart_button.setFixedSize(200, 30)
        
        self.RSI_button = QPushButton('RSI', self)
        self.RSI_button.clicked.connect(self.plot_RSI_graph)
        self.RSI_button.setFixedSize(200, 30)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.time_span_label)
        self.layout.addWidget(self.time_span_combobox)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.output_text)
        self.layout.addWidget(self.macd_crossover_button)
        self.layout.addWidget(self.macd_signal_graph_button)
        self.layout.addWidget(self.candlestick_chart_button)
        self.layout.addWidget(self.RSI_button)
        self.setLayout(self.layout)

    def start_fetching_data(self):
        user_input = self.input_text.text()
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        self.output_text.clear()
        self.output_text.append("Fetching data... Please wait.")
        self.thread = FetchDataThread(user_input, time_span)
        self.thread.signal.connect(self.display_data)
        self.thread.start()

    def display_data(self, data):
        self.output_text.clear()
        if 'error' in data:
            self.output_text.append(f"Error: {data['error']}")
        else:
            self.output_text.append(f"Data for the selected time span:\n{data['description']}\n")
            self.output_text.append(f"Available Columns: {data['columns']}\n")

    def plot_macd_crossover_graph(self):
        user_input = self.input_text.text()
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        df = yf.download(user_input, start='2023-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))
        self.plot_macd_crossover_graph_method(df)  # Corrected method name

    def plot_macd_and_signal_line_graph(self):
        user_input = self.input_text.text()
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        df = yf.download(user_input, start='2023-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))
        self.plot_macd_and_signal_line_graph_method(df)

    def plot_candlestick_chart(self):
        user_input = self.input_text.text()
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        df = yf.download(user_input, start='2023-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))
        candlestick_window = CandlestickWindow(df, user_input)
        candlestick_window.setGeometry(200, 200, 1200, 600)
        candlestick_window.show()

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

    def plot_macd_and_signal_line_graph_method(self, df):  # Renamed method
        df['12_EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['26_EMA'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['12_EMA'] - df['26_EMA']
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

        plt.figure(figsize=(14, 7))
        plt.title('MACD & Signal Line Graph')
        plt.plot(df.index, df['MACD'], label='MACD', color='blue')
        plt.plot(df.index, df['Signal_Line'], label='Signal Line', color='red')
        plt.legend()
        plt.show()
        
    def plot_RSI_graph(self):
        user_input = self.input_text.text()
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        df = yf.download(user_input, start='2023-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))

    # Replace the line causing the warning
        df['Close'] = df['Close'].ffill()

    # Calculate RSI
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=14, min_periods=1).mean()
        avg_loss = loss.rolling(window=14, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    # Plot RSI
        plt.figure(figsize=(14, 7))
        plt.title('Relative Strength Index (RSI)')
        plt.plot(df.index, rsi, label='RSI', color='purple')
        plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
        plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = StockPredictionApp()
    ex.show()
    sys.exit(app.exec_())


