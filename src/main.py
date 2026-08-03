from portfolio import buy_stock, sell_stock


def menu():

    while True:

        print("\n====================")
        print("     NORTHSTAR")
        print("====================")

        print("1. Buy Stock")
        print("2. Sell Stock")
        print("3. Exit")


        choice = input("\nChoose option: ")


        if choice == "1":
            buy_stock()

        elif choice == "2":
            sell_stock()

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()