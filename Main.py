from datetime import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

end_date = datetime(year=2025, month=12, day=31)
start_date = datetime(year=2000, month=1, day=1)

tickers = ["NVDA", "MSFT", "AAPL"]
data = yf.download(tickers, start=start_date, end=end_date, interval="1d", auto_adjust=True)
print(data.head())