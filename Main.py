from datetime import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np

end_date = datetime(year=2025, month=12, day=31)
start_date = datetime(year=2000, month=1, day=1)

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
data["cumulativeReturn"] = (1 + data["return"]).cumprod()
#print(data.tail())

#graph
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Stock Price', alpha=0.5)
plt.plot(data.loc[data['signal'] == 1, 'Close'], '^', markersize=3, color='g', label='Buy Signal')
plt.plot(data.loc[data['signal'] == 0, 'Close'], 'v', markersize=3, color='r', label='Sell Signal')

plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

#sharpe ratio
meanReturn = data["return"].mean()
stdReturn = data["return"].std(ddof=1)

dailyRiskFree=0.05/252
sharpeRatio = np.sqrt(len(data))*(meanReturn - dailyRiskFree) / stdReturn if stdReturn != 0 else 0
print("Sharpe Ratio:", sharpeRatio)

#max drawdown
data["drawdown"]=(data["cumulativeReturn"]/data["cumulativeReturn"].cummax())-1
mdd=data["drawdown"].min()*100
print("Max Drawdown:", mdd, "%")

