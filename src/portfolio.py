import sqlite3

from database import DATABASE_PATH
from database import add_transaction
from market_data import get_current_price


def buy_stock():

    ticker = input("\nTicker: ").upper().strip()

    try:
        shares = float(input("Shares: "))

    except ValueError:
        print("\nInvalid number entered.")
        return

    price = get_current_price(ticker)

    if price is None:
        print("\nUnable to retrieve stock price.")
        return

    add_transaction(
        ticker,
        "BUY",
        shares,
        price
    )

    print(
        f"\n✓ Purchased {shares:.2f} shares of {ticker} "
        f"at ${price:.2f}"
    )


def sell_stock():

    ticker = input("\nTicker: ").upper().strip()

    try:
        shares = float(input("Shares sold: "))

    except ValueError:
        print("\nInvalid number entered.")
        return

    price = get_current_price(ticker)

    if price is None:
        print("\nUnable to retrieve stock price.")
        return

    add_transaction(
        ticker,
        "SELL",
        shares,
        price
    )

    print(
        f"\n✓ Sold {shares:.2f} shares of {ticker} "
        f"at ${price:.2f}"
    )


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


def display_portfolio():

    portfolio = get_portfolio()

    print("\n")
    print("=" * 110)
    print("                              NORTHSTAR PORTFOLIO")
    print("=" * 110)

    print(
        f"{'Ticker':<10}"
        f"{'Shares':>12}"
        f"{'Price':>15}"
        f"{'Value':>18}"
        f"{'Gain/Loss':>18}"
        f"{'Return':>12}"
    )

    print("-" * 110)

    total_value = 0
    total_cost = 0


    for ticker, data in portfolio.items():

        shares = data["shares"]
        cost = data["cost"]

        price = get_current_price(ticker)

        if price is None:
            continue


        value = shares * price

        gain_loss = value - cost

        if cost != 0:
            gain_percent = (gain_loss / cost) * 100
        else:
            gain_percent = 0


        total_value += value
        total_cost += cost


        print(
            f"{ticker:<10}"
            f"{shares:>12.2f}"
            f"{'':>4}"
            f"${price:>10,.2f}"
            f"{'':>4}"
            f"${value:>13,.2f}"
            f"{'':>4}"
            f"${gain_loss:>13,.2f}"
            f"{'':>4}"
            f"{gain_percent:>8.2f}%"
        )


    total_gain_loss = total_value - total_cost

    if total_cost != 0:
        total_return = (total_gain_loss / total_cost) * 100
    else:
        total_return = 0


    print("-" * 110)

    print(
        f"{'Portfolio Value:':>85}"
        f" ${total_value:,.2f}"
    )

    print(
        f"{'Total Cost Basis:':>85}"
        f" ${total_cost:,.2f}"
    )

    print(
        f"{'Total Gain/Loss:':>85}"
        f" ${total_gain_loss:,.2f}"
    )

    print(
        f"{'Total Return:':>85}"
        f" {total_return:.2f}%"
    )

    print()