import asyncio
import pandas as pd
from lightweight_charts import Chart

from ib_insync import *
import nest_asyncio
nest_asyncio.apply()

def calculate_sma(df, period: int = 50):
    df['SMA'] = df['close'].rolling(window=period).mean()
    return df.dropna()

def get_data(symbol, timeframe):
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=13)

    contract = Stock(symbol, 'SMART', 'USD')
    bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='90 D',
            barSizeSetting=timeframe,
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1)
    ib.disconnect()
    df = util.df(bars)

    return df

class API:
    def __init__(self):
        self.chart = Chart()

    async def update_chart(self, symbol, timeframe):
        data = get_data(symbol, timeframe)
        self.chart.set(data)
        # For demonstration purposes, setting a title (you may need to adjust based on the library's API)
        self.chart.set_title(f"{symbol} - {timeframe}")
        # Additional logic to update the chart based on the symbol and timeframe can be added here.

async def main():
    api_instance = API()
    
    symbol = 'AAPL'
    timeframe = '15 mins'
    await api_instance.update_chart(symbol, timeframe)

    await api_instance.chart.show_async(block=True)

if __name__ == '__main__':
    asyncio.run(main())
