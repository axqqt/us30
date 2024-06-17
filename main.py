import ccxt
import pandas as pd
from ta.trend import SMAIndicator

# Function to fetch historical OHLCV data
def fetch_historical_data(exchange, symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Function to implement trading strategy
def implement_strategy(df, exchange, symbol):
    # Calculate indicators (e.g., 50-period and 200-period SMAs)
    sma50 = SMAIndicator(df['close'], window=50)
    sma200 = SMAIndicator(df['close'], window=200)
    df['sma50'] = sma50.sma_indicator()
    df['sma200'] = sma200.sma_indicator()

    # Implement strategy (e.g., simple moving average crossover)
    position = None
    for index, row in df.iterrows():
        if row['sma50'] > row['sma200'] and position != 'BUY':
            # Execute buy order
            print(f"Buying at {row['close']}, timestamp: {row['timestamp']}")
            position = 'BUY'
            # Place order (simulated)
            order = exchange.create_market_buy_order(symbol, 1)  # Buy 1 contract
            print("Order placed:", order)
        elif row['sma50'] < row['sma200'] and position != 'SELL':
            # Execute sell order
            print(f"Selling at {row['close']}, timestamp: {row['timestamp']}")
            position = 'SELL'
            # Place order (simulated)
            order = exchange.create_market_sell_order(symbol, 1)  # Sell 1 contract
            print("Order placed:", order)

# Main function
def main():
    # Initialize exchange (example using Binance testnet for simulation)
    exchange = ccxt.binance({
        'apiKey': 'your_api_key',
        'secret': 'your_api_secret',
        'enableRateLimit': True,  # To ensure API rate limits are respected
        'options': {
            'defaultType': 'future',  # Use futures market
            'adjustForTimeDifference': True,  # Adjust for time difference
        }
    })

    # Fetch historical data for US30/USDT
    symbol = 'US30/USDT'
    timeframe = '1h'
    limit = 1000  # Number of candles to fetch
    df = fetch_historical_data(exchange, symbol, timeframe, limit)

    # Implement strategy
    implement_strategy(df, exchange, symbol)

if __name__ == "__main__":
    main()
