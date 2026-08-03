from portfolio import buy_stock, sell_stock, display_portfolio


def menu():

    while True:

        print("\n====================")
        print("     NORTHSTAR")
        print("====================")

        print("1. Buy Stock")
        print("2. Sell Stock")
        print("3. Display Portfolio")
        print("4. Exit")


        choice = input("\nChoose option: ")


        if choice == "1":
            buy_stock()

        elif choice == "2":
            sell_stock()

        elif choice == "3":
            display_portfolio()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()