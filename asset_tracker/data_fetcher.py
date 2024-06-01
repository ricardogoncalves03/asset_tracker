import yfinance as yf
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

def fetch_closing_prices(tickers: List[str], period: str) -> Tuple[Dict[str, float], Dict[str, float]]:
    today = datetime.today()
    # Determine the period to fetch data
    if period == 'daily':
        data = yf.download(tickers, period='5d')
    elif period == 'weekly':
        start_of_week = today - timedelta(days=today.weekday())
        data = yf.download(tickers, start=start_of_week.strftime('%Y-%m-%d'))
    elif period == 'monthly':
        if today.day == 1 or today.day == 2:
            start_of_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        else:
            today = datetime.today()
            start_of_month = today.replace(day=1)
        data = yf.download(tickers, start=start_of_month.strftime('%Y-%m-%d'))

    current_closing_prices = data['Close'].iloc[-1]
    first_closing_prices = data['Close'].iloc[0]

    return current_closing_prices.to_dict(), first_closing_prices.to_dict()
