from portfolio import get_portfolio
from market_data import get_current_price


portfolio = get_portfolio()


print("\nNORTHSTAR PORTFOLIO")
print("------------------")


total_value = 0


for ticker, data in portfolio.items():

    current_price = get_current_price(ticker)

    shares = data["shares"]

    value = shares * current_price

    gain_loss = (
        value -
        data["cost"]
    )

    total_value += value


    print(f"\n{ticker}")
    print(f"Shares: {shares}")
    print(
        f"Current Price: ${current_price:.2f}"
    )
    print(
        f"Value: ${value:.2f}"
    )
    print(
        f"Gain/Loss: ${gain_loss:.2f}"
    )


print("\n------------------")
print(
    f"Portfolio Value: ${total_value:.2f}"
)