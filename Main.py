from datetime import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

end_date = datetime(year=2025, month=12, day=31)
start_date = datetime(year=2015, month=1, day=1)

#tickers = ["NVDA", "MSFT", "AAPL"]
tickers = "AAPL"
data = yf.download(tickers, start=start_date, end=end_date, interval="1d", auto_adjust=True,multi_level_index=False)

#12-1 trailing return
close21=data["Close"].shift(21)
close252=data["Close"].shift(252)
data["trailingReturn"] = ((close21 - close252) / close252 )*100

#generate signals
data["signal"] = 0
data.loc[data['trailingReturn'] > 0, 'signal'] = 1  # Buy

#backtest
data["return"]= data["Close"].pct_change() * data["signal"].shift(1)
data["cumulative_return"] = (1 + data["return"]).cumprod()
print(data.tail())