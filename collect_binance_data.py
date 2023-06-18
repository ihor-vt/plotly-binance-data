import requests
import csv


# Example usage
SYMBOL = "BTCUSDT"
INTERVAL = "1h"
FILENAME = "binance_data.csv"


def read_csv_file(filename):
    """
    The read_csv_file function takes a filename as an argument and returns the contents of that file in a list.
    The function opens the file, reads it line by line, and appends each row to a list. The function then returns this
    list.

    :param filename: Specify the file to read from
    :return: A list of lists
    """
    data = []
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data


def collect_binance_data(symbol, interval, filename):
    """
    The collect_binance_data function takes in a symbol, interval, and filename.
    The function then uses the requests library to make an API call to Binance's REST API.
    The response is saved as JSON data and written into a CSV file with the given filename.

    :param symbol: Specify the symbol of the asset to collect data for
    :param interval: Specify the time interval for which we want to collect data
    :param filename: Specify the name of the file that will be created
    :return: Nothing
    """
    if not filename:
        filename = f"{symbol}_{interval}_binance.csv"
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
    response = requests.get(url)
    data = response.json()

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time"]
        )

        for row in data:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

    print(f"Data for symbol {symbol} collected and saved in {filename}")


if __name__ == "__main__":
    collect_binance_data(SYMBOL, INTERVAL, FILENAME)
