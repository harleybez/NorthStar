from portfolio import get_portfolio


portfolio = get_portfolio()


print("\nNORTHSTAR PORTFOLIO")
print("------------------")


for ticker, data in portfolio.items():

    print(
        f"{ticker}: "
        f"{data['shares']} shares "
        f"@ ${data['average_price']:.2f}"
    )