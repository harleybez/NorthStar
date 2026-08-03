import sqlite3
from pathlib import Path
from datetime import datetime


DATABASE_PATH = Path("database/northstar.db")


def create_database():

    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        ticker TEXT,
        price REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        ticker TEXT,
        action TEXT,
        shares REAL,
        price REAL
    )
    """)

    connection.commit()
    connection.close()



def add_price(ticker, price):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO price_history
        (timestamp, ticker, price)
        VALUES (?, ?, ?)
        """,
        (
            datetime.now(),
            ticker,
            price
        )
    )

    connection.commit()
    connection.close()



def add_transaction(ticker, action, shares, price):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO transactions
        (timestamp, ticker, action, shares, price)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            datetime.now(),
            ticker,
            action,
            shares,
            price
        )
    )

    connection.commit()
    connection.close()



if __name__ == "__main__":

    create_database()

    print("NorthStar database ready.")