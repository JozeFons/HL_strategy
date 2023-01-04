import ccxt
import numpy as np
import time

# Initialize the Binance exchange with API key and secret
binance = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_API_SECRET',
})

# Set your trade symbol, the amount you want to trade, and the timeframe
symbol = 'BTC/USDT'
amount = 1
timeframe = '1h' # can be '1m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'

# Fetch the most recent candles for the symbol and timeframe
candles = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=2)

# Extract the open and close times from the candles
open_time = candles[0][0]
close_time = candles[1][0]

# Calculate the interval in seconds
interval = close_time - open_time

# Calculate the highest high and lowest low over the past 1000 candles
highestHigh = np.max(high)
lowestLow = np.min(low)

while True:
    # Fetch the current ticker information
    ticker = binance.fetch_ticker(symbol)

    # Get the current high and low prices
    currentHigh = ticker['high']
    currentLow = ticker['low']

    # Get the current order book
    order_book = binance.fetch_order_book(symbol)

    # Calculate the ratio of buy orders to sell orders
    buy_orders = 0
    sell_orders = 0
    for order in order_book['bids']:
        buy_orders += order[1]
    for order in order_book['asks']:
        sell_orders += order[1]
    order_ratio = buy_orders / sell_orders

    # Check if the current high is higher than the highest high and the order ratio is less than 2
    if currentHigh > highestHigh and order_ratio < 2:
        # Place a buy limit order
        binance.create_order(symbol, 'limit', 'buy', amount, currentHigh)
        print(f'Placed a buy limit order for {amount} {symbol} at {currentHigh}')
    
    # Check if the current low is lower than the lowest low and the order ratio is greater than 0.5
    if currentLow < lowestLow and order_ratio > 0.5:
        # Place a sell limit order
        binance.create_order(symbol, 'limit', 'sell', amount, currentLow)
        print(f'Placed a sell limit order for {amount} {symbol} at {currentLow}')
    
    # Sleep for the calculated interval
    time.sleep(interval)
