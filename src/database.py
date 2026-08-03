import sqlite3
from pathlib import Path


DATABASE_PATH = Path("database/northstar.db")


def create_database():
    """
    Creates the NorthStar database and tables.
    """

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

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("NorthStar database created.")