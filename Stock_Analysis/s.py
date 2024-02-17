from yahoo_fin import stock_info
from tkinter import *
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def stock_price():
    symbol = e1.get()
    price = stock_info.get_live_price(symbol)
    Current_stock.set(price)
    
    # Get selected time interval
    selected_interval = time_interval.get()
    start_date, end_date = get_start_end_dates(selected_interval)
    
    # Get historical data for the selected chart type
    chart_type = chart_type_var.get()
    if chart_type == "Candlestick":
        historical_data = stock_info.get_data(symbol, start_date=start_date, end_date=end_date, index_as_date=True)
        plot_candlestick_chart(historical_data)
    elif chart_type == "MACD vs Signal Line Graph":
        plot_macd_signal_chart(symbol, start_date, end_date)
    elif chart_type == "Line Graph":
        plot_line_chart(symbol, start_date, end_date)
    elif chart_type == "Bar":
        plot_bar_chart(symbol, start_date, end_date)
    elif chart_type == "Colored Bar":
        plot_colored_bar_chart(symbol, start_date, end_date)
    else:
        print("Invalid chart type selected.")

def plot_candlestick_chart(data):
    fig, ax = mpf.plot(data, type='candle', style='yahoo', title='Candlestick Chart', ylabel='Price',
                       datetime_format='%Y-%m-%d', show_nontrading=True, returnfig=True, figsize=(6, 4))

    # Embed the candlestick chart within the Tkinter application
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=6, column=0, columnspan=3, sticky="nsew")

    # Add navigation toolbar for zooming and panning
    toolbar = NavigationToolbar2Tk(canvas, master)
    toolbar.update()
    canvas_widget.grid(row=6, column=0, columnspan=3, sticky="nsew")

def plot_macd_signal_chart(symbol, start_date, end_date):
    data = stock_info.get_data(symbol, start_date=start_date, end_date=end_date, index_as_date=True)
    mpf.plot(data, type='line', title='MACD vs Signal Line Graph', ylabel='Price', mav=(12, 26), volume=False)

def plot_line_chart(symbol, start_date, end_date):
    data = stock_info.get_data(symbol, start_date=start_date, end_date=end_date, index_as_date=True)
    mpf.plot(data, type='line', title='Line Graph', ylabel='Price', volume=False)

def plot_bar_chart(symbol, start_date, end_date):
    data = stock_info.get_data(symbol, start_date=start_date, end_date=end_date, index_as_date=True)
    mpf.plot(data, type='ohlc', title='Bar Chart', ylabel='Price', volume=False)

def plot_colored_bar_chart(symbol, start_date, end_date):
    data = stock_info.get_data(symbol, start_date=start_date, end_date=end_date, index_as_date=True)
    mpf.plot(data, type='candle', style='charles', title='Colored Bar Chart', ylabel='Price', volume=False)

def get_start_end_dates(interval):
    import datetime
    today = datetime.date.today()
    if interval == "1 month":
        start_date = today - datetime.timedelta(days=30)
    elif interval == "3 months":
        start_date = today - datetime.timedelta(days=90)
    elif interval == "6 months":
        start_date = today - datetime.timedelta(days=180)
    elif interval == "1 year":
        start_date = today - datetime.timedelta(days=365)
    else:
        start_date = today - datetime.timedelta(days=365)
    return start_date, today

master = Tk()
master.title("Stock Analysis")
master.geometry("800x600")  # Set initial window size

Current_stock = StringVar()

Label(master, text="Company Symbol: ").grid(row=0, sticky=W)
Label(master, text="Stock Result:", font=("Arial", 12, "bold"), fg="blue").grid(row=3, sticky=W)

result2 = Label(master, text="", textvariable=Current_stock, font=("Arial", 12, "bold")).grid(row=3, column=1, sticky=W)

Label(master, text="Select the time interval:").grid(row=2, sticky=W)

e1 = Entry(master, width=50)
e1.grid(row=0, column=1)

time_interval = StringVar(master)
time_interval.set("1 year")

time_options = OptionMenu(master, time_interval, "1 month", "3 months", "6 months", "1 year")
time_options.grid(row=2, column=1, sticky=W)

chart_type_var = StringVar(master)
chart_type_var.set("Candlestick")

chart_options = OptionMenu(master, chart_type_var, "Candlestick", "MACD vs Signal Line Graph", "Line Graph", "Bar", "Colored Bar")
chart_options.grid(row=4, column=1, sticky=W)

b = Button(master, text="Show", command=stock_price)
b.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=5)

master.columnconfigure(0, weight=1)
master.rowconfigure(6, weight=1)

mainloop()
