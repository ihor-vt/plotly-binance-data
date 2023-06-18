from flask import Flask, render_template
import requests
import plotly.graph_objs as go

app = Flask(__name__)

# here you can insert your data
SYMBOL = "BTCUSDT"
INTERVAL= "1h"
SYMBOLS= [
    "BTCUSDT",
    "ETHUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "LTCUSDT",
    "BCHUSDT",
    "LINKUSDT",
    "XLMUSDT",
    "XMRUSDT",
]


def collect_binance_data(symbol, interval):
    """
    The collect_binance_data function takes in a symbol and an interval,
        then returns the data from Binance's API.

    :param symbol: Specify the trading pair
    :param interval: Specify the time interval for which we want to collect data
    :return: A list of lists
    """
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
    response = requests.get(url)
    data = response.json()
    return data


def get_market_caps(symbols):
    """
    The get_market_caps function takes in a list of symbols and returns a list of market caps.
        The function uses the Binance API to get the 24 hour quote volume for each symbol,
        which is then used as an approximation for market cap.

    :param symbols: Pass in the list of symbols to get market caps for
    :return: A list of market caps
    :doc-author: Trelent
    """
    market_caps = []
    for symbol in symbols:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        market_cap = float(data["quoteVolume"])
        market_caps.append(market_cap)
    return market_caps


@app.route("/")
def index():
    # Collect candlestick data from Binance API
    candlestick_data = collect_binance_data(SYMBOL, INTERVAL)

    # Process candlestick data for plotting
    x = [item[0] for item in candlestick_data]
    open_values = [float(item[1]) for item in candlestick_data]
    high_values = [float(item[2]) for item in candlestick_data]
    low_values = [float(item[3]) for item in candlestick_data]
    close_values = [float(item[4]) for item in candlestick_data]

    # Create candlestick trace
    candlestick_trace = go.Candlestick(
        x=x,
        open=open_values,
        high=high_values,
        low=low_values,
        close=close_values,
        name="Candlestick",
    )

    market_cap_data = get_market_caps(SYMBOLS)

    # Create market cap pie chart trace
    market_cap_trace = go.Pie(labels=SYMBOLS, values=market_cap_data, name="Market Cap")

    # Create candlestick chart layout
    candlestick_layout = go.Layout(title="Candlestick Chart")

    # Create market cap pie chart layout
    market_cap_layout = go.Layout(title="Market Cap")

    # Create candlestick chart figure
    candlestick_figure = go.Figure(data=[candlestick_trace], layout=candlestick_layout)

    # Create market cap pie chart figure
    market_cap_figure = go.Figure(data=[market_cap_trace], layout=market_cap_layout)

    # Convert the figures to JSON for passing to the template
    candlestick_chart_data = candlestick_figure.to_json()
    market_cap_pie_chart_data = market_cap_figure.to_json()

    return render_template(
        "/index.html",
        candlestick_chart=candlestick_chart_data,
        market_cap_pie_chart=market_cap_pie_chart_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
