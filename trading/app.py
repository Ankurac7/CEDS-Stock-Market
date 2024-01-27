<<<<<<< HEAD
import sys
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QDateEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import qdarkstyle
import os

# List of Nifty 50 stock symbols
nifty_50_symbols = [
    "ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","ASIANPAINT.NS","AXISBANK.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","BAJFINANCE.NS","BHARTIARTL.NS","BPCL.NS","BRITANNIA.NS","CIPLA.NS","COALINDIA.NS","DIVISLAB.NS","DRREDDY.NS","EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFCLIFE.NS","HDFCBANK.NS","HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS","ICICIBANK.NS","INDUSINDBK.NS","INFY.NS","ITC.NS","JSWSTEEL.NS","KOTAKBANK.NS","LT.NS","LTIM.NS","M&M.NS","MARUTI.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS","POWERGRID.NS","RELIANCE.NS","SBILIFE.NS","SBIN.NS","SUNPHARMA.NS","TATACONSUM.NS","TATAMOTORS.NS","TATASTEEL.NS","TCS.NS","TECHM.NS","TITAN.NS","ULTRACEMCO.NS","UPL.NS","WIPRO.NS"
]

# Function to calculate Exponential Moving Average (EMA)
def calculate_ema(data, ema_period):
    data['EMA'] = data['Close'].ewm(span=ema_period, adjust=False).mean()
    return data

class FetchDataThread(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, user_input, start_date, end_date):
        super().__init__()
        self.user_input = user_input
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        try:
            df = yf.download(self.user_input, start=self.start_date, end=self.end_date)
            data = {
                'description': df.describe().to_string(),
                'columns': df.columns.tolist(),
                'close': df['Close'].tolist() if 'Close' in df.columns else None
            }
            self.signal.emit(data)
        except Exception as e:
            self.signal.emit({'error': str(e)})

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(fig)

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

        self.date_label = QLabel('Select Start Date:', self)
        self.date_picker = QDateEdit(self)
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate().addDays(-365))  # Default to one year ago
        self.date_picker.setFixedSize(200, 30)

        self.time_span_label = QLabel('Select Time Span:', self)
        self.time_span_combobox = QComboBox(self)
        self.time_span_combobox.addItems(['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'])
        self.time_span_combobox.setFixedSize(200, 30)

        self.submit_button = QPushButton('Fetch Data', self)
        self.submit_button.clicked.connect(self.start_fetching_data)
        self.submit_button.setFixedSize(200, 30)

        self.output_text = QTextEdit(self)
        self.output_text.setFont(QFont("Arial", 12))

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        self.analysis_options_label = QLabel('Select Analysis:', self)
        self.analysis_options_combobox = QComboBox(self)
        self.analysis_options_combobox.addItems(['MACD Crossover', 'MACD & Signal Line', 'Candlestick Chart', 'RSI', 'EMA'])
        self.analysis_options_combobox.setFixedSize(200, 30)
        self.analysis_options_combobox.currentIndexChanged.connect(self.handle_analysis_selection)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date_picker)
        self.layout.addWidget(self.time_span_label)
        self.layout.addWidget(self.time_span_combobox)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.output_text)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.analysis_options_label)
        self.layout.addWidget(self.analysis_options_combobox)
        self.setLayout(self.layout)

    def start_fetching_data(self):
        user_input = self.input_text.text()
        start_date = self.date_picker.date().toPyDate().strftime('%Y-%m-%d')
        end_date = pd.to_datetime('today').strftime('%Y-%m-%d')
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        self.output_text.clear()
        self.output_text.append("Fetching data... Please wait.")
        self.thread = FetchDataThread(user_input, start_date, end_date)
        self.thread.signal.connect(self.display_data)
        self.thread.start()

    def display_data(self, data):
        self.output_text.clear()
        if 'error' in data:
            self.output_text.append(f"Error: {data['error']}")
        else:
            self.output_text.append(f"Data for the selected time span:\n{data['description']}\n")
            self.output_text.append(f"Available Columns: {data['columns']}\n")

    def handle_analysis_selection(self):
        selected_option = self.analysis_options_combobox.currentText()

        if selected_option == 'MACD Crossover':
            self.plot_macd_crossover_graph()
        elif selected_option == 'MACD & Signal Line':
            self.plot_macd_and_signal_line_graph()
        elif selected_option == 'Candlestick Chart':
            self.plot_candlestick_chart()
        elif selected_option == 'RSI':
            self.plot_RSI_graph()
        elif selected_option == 'EMA':
            self.plot_ema_graph()
            
    def plot_macd_crossover_graph(self):
        user_input = self.input_text.text()
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        df = yf.download(user_input, start='2023-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))
        self.plot_macd_crossover_graph_method(df)

    def plot_macd_and_signal_line_graph(self):
        user_input = self.input_text.text()
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        df = yf.download(user_input, start='2023-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))
        self.plot_macd_and_signal_line_graph_method(df)

    def plot_candlestick_chart(self):
        user_input = self.input_text.text()
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        df = yf.download(user_input, start='2023-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))
        self.plot_candlestick_chart_method(df)

    def plot_RSI_graph(self):
        user_input = self.input_text.text()
        time_span = self.time_span_combobox.currentText().split()[0].lower()
        df = yf.download(user_input, start='2023-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))
        self.plot_RSI_graph_method(df)

    def plot_ema_graph(self):
        user_input = self.input_text.text()
        ema_period = 14  # Adjust this value as needed
        df = yf.download(user_input, start='2023-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))
        df = calculate_ema(df, ema_period)

        self.canvas.axes.clear()

        self.canvas.axes.set_title(f'Exponential Moving Average (EMA) for {user_input}')
        self.canvas.axes.plot(df.index, df['Close'], label='Close Price')
        self.canvas.axes.plot(df.index, df['EMA'], label=f'EMA-{ema_period} Days')
        self.canvas.axes.legend()
        self.canvas.axes.set_ylabel('Price')
        self.canvas.axes.set_xlabel('Date')
        self.canvas.axes.grid(True)
        self.canvas.draw()

    def plot_macd_crossover_graph_method(self, df):
        df['12_EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['26_EMA'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['12_EMA'] - df['26_EMA']
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
        df['Cumulative_Returns'] = (1 + df['Close'].pct_change()).cumprod() - 1

        self.canvas.axes.clear()

        self.canvas.axes.set_title('Cumulative Returns Based on MACD Crossovers')
        self.canvas.axes.plot(df.index, df['Cumulative_Returns'])
        self.canvas.axes.set_ylabel('Cumulative Returns')
        self.canvas.axes.set_xlabel('Date')
        self.canvas.axes.grid(True)
        self.canvas.draw()

    def plot_macd_and_signal_line_graph_method(self, df):
        df['12_EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['26_EMA'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['12_EMA'] - df['26_EMA']
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

        self.canvas.axes.clear()

        self.canvas.axes.set_title('MACD & Signal Line Graph')
        self.canvas.axes.plot(df.index, df['MACD'], label='MACD', color='blue')
        self.canvas.axes.plot(df.index, df['Signal_Line'], label='Signal Line', color='red')
        self.canvas.axes.legend()
        self.canvas.draw()
    
    

    def plot_candlestick_chart_method(self, df):
        df.index.name = 'Date'

        self.canvas.axes.clear()

        mpf.plot(df, type='candle', ax=self.canvas.axes, style='yahoo', volume=False)

        self.canvas.axes.set_title(f'Candlestick Chart for {self.input_text.text()}', fontsize=16)

        toolbar = NavigationToolbar(FigureCanvas(self.canvas.figure), self)
        layout = QVBoxLayout(self)
        layout.addWidget(toolbar)
        layout.addWidget(FigureCanvas(self.canvas.figure))
        self.setLayout(layout)

        self.canvas.draw()

    def plot_RSI_graph_method(self, df):
        df['Close'] = df['Close'].ffill()

        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=14, min_periods=1).mean()
        avg_loss = loss.rolling(window=14, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        self.canvas.axes.clear()

        self.canvas.axes.set_title('Relative Strength Index (RSI)')
        self.canvas.axes.plot(df.index, rsi, label='RSI', color='purple')
        self.canvas.axes.axhline(70, color='red', linestyle='--', label='Overbought (70)')
        self.canvas.axes.axhline(30, color='green', linestyle='--', label='Oversold (30)')
        self.canvas.axes.legend()
        self.canvas.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = StockPredictionApp()
    ex.show()
    sys.exit(app.exec_())
=======
import sys
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import mplfinance as mpf
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal, QUrl
from PyQt5.QtWidgets import qApp, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView  
from lightweight_charts import Chart
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

# class ChartWidget(QWidget):
#     def __init__(self, chart):
#         super().__init__()
#         self.chart = chart
#         self.layout = QVBoxLayout(self)
#         self.layout.addWidget(self.chart)
#         self.setLayout(self.layout)

class CandlestickWindow(QWidget):
    def __init__(self, user_input):
        super().__init__()

        # Set up the lightweight chart
        self.chart = Chart()

        # Create custom widget for the chart
        # self.chart_widget = ChartWidget(self.chart)

        layout = QVBoxLayout(self)
        layout.addWidget(self.chart)
        self.setLayout(layout)

        # Load TradingView chart data
        self.load_tradingview_chart(user_input)

    def load_tradingview_chart(self, user_input):
        # Replace 'symbol' with the desired stock symbol (e.g., 'AAPL')
        symbol = user_input

        msft = yf.Ticker(symbol)
        df = msft.history(period="1y")

        # prepare indicator values
        sma = df.ta.sma(length=20).to_frame()
        sma = sma.reset_index()
        sma = sma.rename(columns={"Date": "time", "SMA_20": "value"})
        sma = sma.dropna()

        # this library expects lowercase columns for date, open, high, low, close, volume
        df = df.reset_index()
        df.columns = df.columns.str.lower()
        self.chart.set(df)

        # add sma line
        line = self.chart.create_line()
        line.set(sma)

        self.chart.watermark(symbol)
        self.chart.show(block=True)

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
        self.candlestick_window = None
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
        if self.candlestick_window is not None:
            self.candlestick_window.close()  # Close previous window if any
        self.candlestick_window = CandlestickWindow(user_input)
        self.candlestick_window.setGeometry(200, 200, 1200, 600)
        self.candlestick_window.show()

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


>>>>>>> 64eda5360f4ce2861416383e853bb34b43bc3c6d
