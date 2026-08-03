import sqlite3
from pathlib import Path


DATABASE_PATH = Path("database/northstar.db")


def get_portfolio():

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ticker, action, shares, price
        FROM transactions
    """)

    transactions = cursor.fetchall()

    connection.close()

    portfolio = {}

    for ticker, action, shares, price in transactions:

        if ticker not in portfolio:
            portfolio[ticker] = {
                "shares": 0,
                "cost": 0
            }

        if action == "BUY":
            portfolio[ticker]["shares"] += shares
            portfolio[ticker]["cost"] += shares * price

        elif action == "SELL":
            portfolio[ticker]["shares"] -= shares
            portfolio[ticker]["cost"] -= shares * price


    for ticker in portfolio:

        shares = portfolio[ticker]["shares"]

        if shares > 0:
            portfolio[ticker]["average_price"] = (
                portfolio[ticker]["cost"] / shares
            )

    return portfolio


if __name__ == "__main__":

    holdings = get_portfolio()

    for ticker, data in holdings.items():
        print(ticker)
        print(data)