import os
import sqlite3
import requests

db_file = os.getenv("SQLITE_DB_FILE")
# db_file = "binance_data.db"


def create_table_if_not_exists():
    """
    Creates the binance_data table if it doesn't exist.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if the table exists, if not, create it
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='binance_data'"
    )
    table_exists = cursor.fetchone()
    if not table_exists:
        cursor.execute(
            "CREATE TABLE binance_data ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "symbol TEXT,"
            "interval TEXT,"
            "open_time INTEGER,"
            "open_price REAL,"
            "high_price REAL,"
            "low_price REAL,"
            "close_price REAL,"
            "volume REAL,"
            "close_time INTEGER"
            ")"
        )

    cursor.close()
    conn.close()


def save_binance_data_to_database(symbol, interval):
    """
    Saves Binance data to the binance_data table in the SQLite database.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
    response = requests.get(url)
    data = response.json()

    for row in data:
        (
            open_time,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
            close_time,
        ) = row

        # Insert the data into the table
        cursor.execute(
            "INSERT INTO binance_data (symbol, interval, open_time, open_price, high_price, low_price, close_price, volume, close_time) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                symbol,
                interval,
                open_time,
                open_price,
                high_price,
                low_price,
                close_price,
                volume,
                close_time,
            ),
        )

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = "1h"
    create_table_if_not_exists()
    save_binance_data_to_database(symbol, interval)
