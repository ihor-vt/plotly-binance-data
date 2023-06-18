import os

import psycopg2
import requests

db_database = os.getenv("POSTGRES_DB_DATABASE")
db_host = os.getenv("POSTGRES_DB_HOST")
db_port = os.getenv("POSTGRES_DB_PORT")
db_name = os.getenv("POSTGRES_DB_NAME")
db_user = os.getenv("POSTGRES_DB_USER")
db_password = os.getenv("POSTGRES_DB_PASSWORD")

symbol = "BTCUSDT"
interval = "1h"

def create_database_if_not_exists():
    """
    The create_database_if_not_exists function checks if the database exists, and if not, creates it.

    :return: None
    """
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_host, port=db_port, user=db_user, password=db_password
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Check if the database exists, if not, create it
    cursor.execute(
        f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_database}'"
    )
    database_exists = cursor.fetchone()
    if not database_exists:
        cursor.execute(f"CREATE DATABASE {db_database}")

    cursor.close()
    conn.close()


def create_table_if_not_exists():
    """
    The create_table_if_not_exists function creates a table in the PostgreSQL database if it does not already exist.
    The function connects to the database, then checks if the binance_data table exists. If it does not, then it is created.

    :return: Nothing, but it creates the table if it doesn't exist
    """
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_database,
        user=db_user,
        password=db_password,
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Check if the table exists, if not, create it
    cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'binance_data')"
    )
    table_exists = cursor.fetchone()[0]
    if not table_exists:
        cursor.execute(
            "CREATE TABLE binance_data ("
            "id SERIAL PRIMARY KEY,"
            "symbol VARCHAR(10),"
            "interval VARCHAR(10),"
            "open_time BIGINT,"
            "open_price NUMERIC(20, 8),"
            "high_price NUMERIC(20, 8),"
            "low_price NUMERIC(20, 8),"
            "close_price NUMERIC(20, 8),"
            "volume NUMERIC(20, 8),"
            "close_time BIGINT"
            ")"
        )

    cursor.close()
    conn.close()


def save_binance_data_to_database(symbol, interval):
    """
    The save_binance_data_to_database function saves Binance data to a PostgreSQL database.

    :param symbol: Specify the symbol for which we want to retrieve data
    :param interval: Specify the time interval of the data
    :return: Nothing
    """
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_database,
        user=db_user,
        password=db_password,
    )

    # Create a cursor object to execute SQL queries
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

        # Insert the data into the database
        cursor.execute(
            "INSERT INTO binance_data (symbol, interval, open_time, open_price, high_price, low_price, close_price, volume, close_time) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
    create_database_if_not_exists()
    create_table_if_not_exists()
    save_binance_data_to_database(symbol, interval)
