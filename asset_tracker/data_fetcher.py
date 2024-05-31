import yfinance as yf
import pandas as pd
from typing import List, Dict, Tuple


def fetch_closing_prices(tickers: List[str]) -> Tuple[Dict[str, float], Dict[str, float]]:
    data = yf.download(tickers, period="5d")
    current_closing_prices = data["Close"].iloc[-1]  # Get the closing prices for the last day
    previous_current_closing_prices = data["Close"].iloc[-2]  # Get the closing prices for the day before last

    return current_closing_prices.to_dict(), previous_current_closing_prices  # Convert to dictionary
