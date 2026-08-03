import yfinance as yf


def get_current_price(ticker):

    stock = yf.Ticker(ticker)

    price = stock.history(
        period="1d"
    )["Close"].iloc[-1]

    return float(price)


if __name__ == "__main__":

    price = get_current_price("AAPL")

    print(
        f"AAPL current price: ${price:.2f}"
    )