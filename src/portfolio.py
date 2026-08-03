import sqlite3

from database import DATABASE_PATH
from database import add_transaction


def buy_stock():

    ticker = input("\nTicker: ").upper().strip()

    try:
        shares = float(input("Shares: "))
        price = float(input("Purchase price: "))
    except ValueError:
        print("\nInvalid number entered.")
        return

    add_transaction(
        ticker,
        "BUY",
        shares,
        price
    )

    print(f"\n✓ Purchased {shares:.2f} shares of {ticker} at ${price:.2f}")


def sell_stock():

    ticker = input("\nTicker: ").upper().strip()

    try:
        shares = float(input("Shares sold: "))
        price = float(input("Sale price: "))
    except ValueError:
        print("\nInvalid number entered.")
        return

    add_transaction(
        ticker,
        "SELL",
        shares,
        price
    )

    print(f"\n✓ Sold {shares:.2f} shares of {ticker} at ${price:.2f}")


def get_portfolio():

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ticker,
               action,
               shares,
               price
        FROM transactions
        ORDER BY timestamp
    """)

    rows = cursor.fetchall()
    connection.close()

    portfolio = {}

    for ticker, action, shares, price in rows:

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

    return portfolio