import yfinance as yf


def get_current_price(ticker):

    try:

        stock = yf.Ticker(ticker)

        history = stock.history(
            period="1d"
        )

        if history.empty:

            return None

        price = history["Close"].iloc[-1]

        return float(price)


    except Exception:

        return None