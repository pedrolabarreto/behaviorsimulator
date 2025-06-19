import yfinance as yf
import pandas as pd

def load_prices(ticker: str, start: str = "2000-01-01") -> pd.Series:
    """Baixa preços ajustados via yfinance e devolve Series."""
    data = yf.download(ticker, start=start, progress=False)
    if "Adj Close" not in data.columns:
        raise ValueError("Ticker não possui coluna 'Adj Close'")
    return data["Adj Close"].dropna()
