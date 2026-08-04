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
        price REAL,
        realized_gain REAL DEFAULT 0
    )
    """)


    connection.commit()
    connection.close()

    upgrade_database()



def upgrade_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()


    cursor.execute("""
        PRAGMA table_info(transactions)
    """)


    columns = [
        column[1]
        for column in cursor.fetchall()
    ]


    if "realized_gain" not in columns:

        cursor.execute("""
            ALTER TABLE transactions
            ADD COLUMN realized_gain REAL DEFAULT 0
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
            datetime.now().replace(microsecond=0),
            ticker,
            price
        )
    )


    connection.commit()
    connection.close()



def add_transaction(
    ticker,
    action,
    shares,
    price,
    realized_gain=0
):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO transactions
        (
            timestamp,
            ticker,
            action,
            shares,
            price,
            realized_gain
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().replace(microsecond=0),
            ticker,
            action,
            shares,
            price,
            realized_gain
        )
    )


    connection.commit()
    connection.close()



def wipe_portfolio():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()


    cursor.execute("""
        DELETE FROM transactions
    """)


    connection.commit()
    connection.close()


    print("\n✓ Portfolio successfully wiped.")



if __name__ == "__main__":

    create_database()

    print("NorthStar database ready.")