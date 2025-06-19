import yfinance as yf
import pandas as pd

def load_prices(ticker: str, start: str = "2000-01-01") -> pd.Series:
    data = yf.download(ticker, start=start, progress=False)
    return data["Adj Close"].dropna()
