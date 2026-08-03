import yfinance as yf
from datetime import datetime

from database import add_price


def get_current_price(ticker):
    """
    Gets the current market price of a stock.
    """

    stock = yf.Ticker(ticker)

    price = stock.history(
        period="1d"
    )["Close"].iloc[-1]

    return float(price)


def track_stock(ticker):
    """
    Gets price and saves it to NorthStar database.
    """

    price = get_current_price(ticker)

    add_price(
        ticker,
        price
    )

    print(
        f"{ticker}: ${price:.2f} saved."
    )


if __name__ == "__main__":

    track_stock("NVDA")