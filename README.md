## Usage
1. Clone this repository to your local machine or server.
2. Install the dependencies using `pip` or any other Python package manager:
    ```
    pip install -r requirements.txt
3. Set the required environment variable values in the `.env` file. Specify the connection details for the PostgreSQL database or the filename for the SQLite database.

## collect_binance_data.py

This script provides a convenient way to collect historical candlestick data from Binance's REST API and save it as a CSV file. The data is retrieved for a specific symbol and time interval.

## Usage

To use this script, follow steps:

1. Modify the `SYMBOL`, `INTERVAL`, and `FILENAME` variables in the script according to your preferences.

- `SYMBOL`: Specify the symbol of the asset for which you want to collect data (e.g., "BTCUSDT").
- `INTERVAL`: Specify the time interval for which you want to collect data (e.g., "1h" for 1 hour).
- `FILENAME`: Specify the name of the CSV file that will be created to store the data. If not provided, a default filename will be generated based on the symbol and interval.

2. Run the script using the following command:
    ```
    python collect_binance_data.py

## Functionality

This script provides the following functionality:

- Making an API call to Binance's REST API to retrieve candlestick data for a specific symbol and interval.
- Saving the retrieved data as a CSV file, with each row representing a candlestick with fields: "Open Time", "Open", "High", "Low", "Close", "Volume", and "Close Time".
- Optional customization of the filename for the generated CSV file.

Please note that the script requires an internet connection to access Binance's API and retrieve the data.

**Disclaimer:** Make sure to comply with Binance's API usage policies and terms of service while using this script.
## Deploying the Script

To deploy this script to collect relevant data at regular intervals, you can use a task scheduler like `cron` on Linux or `Task Scheduler` on Windows. Here's an example using `cron` on Linux:

1. Save the script to a file, for example, `collect_binance_data.py`.
2. Open a terminal and run the command `crontab -e` to edit the cron jobs for the current user.
3. Add a new line to the crontab file with the schedule you want. For example, to run the script every 4 hours, you can add the following line:

Replace `/path/to/collect_binance_data.py` with the actual path to the script file.

4. Save the crontab file and exit the editor.

This configuration will schedule the script to run every 4 hours and collect data from the Binance API.

### Here's an example using `Task Scheduler` on Windows:

1. Save the script to a file, for example, `collect_binance_data.py`.
2. Open the `Task Scheduler` application.
3. Click on "Create Basic Task" or "Create Task" to create a new task.
4. Provide a name and description for the task.
5. Set the trigger for the task. For example, you can schedule it to run every 4 hours.
6. Choose "Start a program" as the action for the task.
7. Browse and select the script file, `collect_binance_data.py`, as the program/script to run.
8. Configure any additional settings or arguments required for the script.
9. Save the task.

This configuration will schedule the script to run every 4 hours and collect data from the Binance API.

Note: The exact steps may vary depending on the version of Windows you are using. Please refer to the documentation or search for specific instructions based on your Windows version.

## Instructions for Saving Data to a Database

1. Install the necessary dependencies by running the command `pip install -r requirements.txt`.
2. Run `save_data_to_postgres.py` to save the data to a PostgreSQL database or `save_data_to_sqllite.py` to save the data to an SQLite database.
3. Binance data will be retrieved with the specified symbol and interval and saved in the database.

### `create_database_if_not_exists()`

This function checks the existence of the PostgreSQL database. If the database does not exist, it will be created.

### `create_table_if_not_exists()`

This function checks the existence of the `binance_data` table in the PostgreSQL database. If the table does not exist, it will be created with the required fields.

### `save_binance_data_to_database(symbol, interval)`

This function retrieves Binance data for the specified symbol and interval and saves the data in the `binance_data` table of the PostgreSQL database.

Note: Ensure that the database is installed and configured before using these functions.

# Candlestick Chart and Pie Chart

This is a simple Flask application that demonstrates the use of candlestick and pie charts using Plotly.js. The application fetches data from the Binance API for candlestick data and market capitalization and displays them as charts on a webpage.


## Usage

1. Run the application using the command:
    ```
    python app.py
2. Open your web browser and navigate to `http://localhost:5000`. You should see the candlestick and pie charts.

## Making Changes

If you want to modify the list of symbols or the candlestick interval, edit the `index` function in the `app.py` file. You can also customize the appearance of the charts by modifying the `candlestick_layout` and `market_cap_layout` objects.
