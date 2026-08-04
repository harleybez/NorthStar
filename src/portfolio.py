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
        price,
        0
    )

    print(
        f"\n✓ Purchased {shares:.2f} shares of {ticker} "
        f"at ${price:.2f}"
    )



def sell_stock():

    ticker = input("\nTicker: ").upper().strip()

    portfolio = get_portfolio()

    if ticker not in portfolio:
        print("\nYou do not own this stock.")
        return


    owned_shares = portfolio[ticker]["shares"]


    try:
        shares = float(input("Shares sold: "))

    except ValueError:
        print("\nInvalid number entered.")
        return


    if shares > owned_shares:
        print(
            f"\nCannot sell {shares:.2f} shares."
            f" You only own {owned_shares:.2f} shares."
        )
        return


    price = get_current_price(ticker)

    if price is None:
        print("\nUnable to retrieve stock price.")
        return


    # Calculate realized gain

    average_cost = (
        portfolio[ticker]["cost"]
        /
        portfolio[ticker]["shares"]
    )


    realized_gain = (
        price - average_cost
    ) * shares


    add_transaction(
        ticker,
        "SELL",
        shares,
        price,
        realized_gain
    )


    print(
        f"\n✓ Sold {shares:.2f} shares of {ticker} "
        f"at ${price:.2f}"
    )

    print(
        f"  Realized Gain/Loss: ${realized_gain:,.2f}"
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
        ORDER BY id
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

            portfolio[ticker]["cost"] += (
                shares * price
            )



        elif action == "SELL":

            current_shares = portfolio[ticker]["shares"]


            if current_shares > 0:

                average_cost = (
                    portfolio[ticker]["cost"]
                    /
                    current_shares
                )


                portfolio[ticker]["shares"] -= shares


                portfolio[ticker]["cost"] -= (
                    average_cost * shares
                )


    return portfolio



def display_portfolio():

    portfolio = get_portfolio()

    print("\n")
    print("=" * 130)
    print("                              NORTHSTAR PORTFOLIO")
    print("=" * 130)


    print(
        f"{'Ticker':<10}"
        f"{'Shares':>12}"
        f"{'Weight':>10}"
        f"{'Avg Cost':>15}"
        f"{'Price':>15}"
        f"{'Value':>18}"
        f"{'Gain/Loss':>18}"
        f"{'Return':>12}"
    )


    total_value = 0
    total_cost = 0

    holdings = []


    for ticker, data in portfolio.items():

        shares = data["shares"]

        cost = data["cost"]


        if shares <= 0:
            continue


        price = get_current_price(ticker)


        if price is None:
            continue


        average_cost = cost / shares

        value = shares * price

        gain_loss = value - cost


        if cost != 0:

            gain_percent = (
                gain_loss / cost
            ) * 100

        else:

            gain_percent = 0


        total_value += value

        total_cost += cost


        holdings.append(
            {
                "ticker": ticker,
                "shares": shares,
                "avg_cost": average_cost,
                "price": price,
                "value": value,
                "gain": gain_loss,
                "return": gain_percent
            }
        )


    # Sort largest holdings first

    holdings.sort(
        key=lambda h: h["value"],
        reverse=True
    )


    print("-" * 130)


    for stock in holdings:


        weight = (
            stock["value"] / total_value * 100
            if total_value > 0
            else 0
        )


        print(
            f"{stock['ticker']:<10}"
            f"{stock['shares']:>12.2f}"
            f"{weight:>9.2f}%"
            f"${stock['avg_cost']:>13,.2f}"
            f"${stock['price']:>13,.2f}"
            f"${stock['value']:>16,.2f}"
            f"${stock['gain']:>16,.2f}"
            f"{stock['return']:>10.2f}%"
        )


    total_gain_loss = (
        total_value - total_cost
    )


    if total_cost != 0:

        total_return = (
            total_gain_loss / total_cost
        ) * 100

    else:

        total_return = 0


    print("-" * 130)


    print(
        f"{'Portfolio Value:':>100}"
        f" ${total_value:,.2f}"
    )


    print(
        f"{'Total Cost Basis:':>100}"
        f" ${total_cost:,.2f}"
    )


    print(
        f"{'Unrealized Gain/Loss:':>100}"
        f" ${total_gain_loss:,.2f}"
    )


    print(
        f"{'Unrealized Return:':>100}"
        f" {total_return:.2f}%"
    )


    print()



def display_transactions():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()


    cursor.execute("""
        SELECT timestamp,
               action,
               ticker,
               shares,
               price,
               realized_gain
        FROM transactions
        ORDER BY id
    """)


    transactions = cursor.fetchall()

    connection.close()



    print("\n")
    print("=" * 120)
    print("                         NORTHSTAR TRANSACTION HISTORY")
    print("=" * 120)



    print(
        f"{'Date':<28}"
        f"{'Action':<10}"
        f"{'Ticker':<10}"
        f"{'Shares':>12}"
        f"{'Price':>15}"
        f"{'Realized Gain':>18}"
    )


    print("-" * 120)



    if not transactions:

        print("No transactions found.")


    else:

        for timestamp, action, ticker, shares, price, realized_gain in transactions:

            if realized_gain is None:
                realized_gain = 0

            clean_timestamp = str(timestamp).split(".")[0]


            print(
                f"{clean_timestamp:<28}"
                f"{action:<10}"
                f"{ticker:<10}"
                f"{shares:>12.2f}"
                f"${price:>12,.2f}"
                f"${realized_gain:>16,.2f}"
            )


    print("-" * 120)
    print()

def display_summary():

    portfolio = get_portfolio()

    total_value = 0
    total_cost = 0

    # Current Portfolio
    for ticker, data in portfolio.items():

        shares = data["shares"]

        if shares <= 0:
            continue

        price = get_current_price(ticker)

        if price is None:
            continue

        total_value += shares * price
        total_cost += data["cost"]

    unrealized_gain = total_value - total_cost

    if total_cost > 0:
        unrealized_return = (
            unrealized_gain / total_cost
        ) * 100
    else:
        unrealized_return = 0


    # Realized Gains
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(realized_gain), 0)
        FROM transactions
    """)

    realized_gain = cursor.fetchone()[0]

    connection.close()


    total_profit = realized_gain + unrealized_gain


    # Calculate total money ever invested
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(shares * price), 0)
        FROM transactions
        WHERE action = 'BUY'
    """)

    lifetime_cost = cursor.fetchone()[0]

    connection.close()

    if lifetime_cost > 0:
        lifetime_return = (
            total_profit / lifetime_cost
        ) * 100
    else:
        lifetime_return = 0

    print()
    print("=" * 70)
    print("                    NORTHSTAR PERFORMANCE")
    print("=" * 70)

    print()

    print(f"{'Current Portfolio Value':<35}${total_value:>15,.2f}")
    print(f"{'Current Cost Basis':<35}${total_cost:>15,.2f}")

    print()

    print(f"{'Unrealized Gain/Loss':<35}${unrealized_gain:>15,.2f}")
    print(f"{'Unrealized Return':<35}{unrealized_return:>15.2f}%")

    print()

    print(f"{'Realized Gain/Loss':<35}${realized_gain:>15,.2f}")

    print("-" * 70)

    print(f"{'Total Lifetime Profit':<35}${total_profit:>15,.2f}")
    print(f"{'Total Lifetime Return':<35}{lifetime_return:>15.2f}%")

    print("=" * 70)
    print()