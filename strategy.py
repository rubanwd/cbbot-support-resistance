# strategy.py

import pandas as pd

class Strategies:
    def __init__(self):
        pass

    def prepare_dataframe(self, historical_data):
        df = pd.DataFrame(historical_data)
        df.columns = ["timestamp", "open", "high", "low", "close", "volume", "turnover"]
        df['close'] = df['close'].astype(float)
        df.sort_values('timestamp', inplace=True)
        return df

    def identify_support_resistance(self, df):
        # Identify the most recent support and resistance levels
        support = df['low'].rolling(window=20).min().iloc[-1]  # recent lowest low
        resistance = df['high'].rolling(window=20).max().iloc[-1]  # recent highest high
        return support, resistance

    def determine_market_trend(self, df, hours=5):
        # Analyze market movement over the last `hours`
        # Assuming the data points are in 1-hour intervals
        lookback_period = hours * 12  # 5 hours = 60 five-minute candles

        recent_data = df[-lookback_period:]  # get last N rows
        initial_price = recent_data['close'].iloc[0]
        final_price = recent_data['close'].iloc[-1]

        if final_price > initial_price:
            return 'bull'  # bullish trend
        else:
            return 'bear'  # bearish trend

    def support_resistance_strategy(self, current_price, support, resistance, trend):
        # If the trend is bullish, set a long position at support
        # If the trend is bearish, set a short position at resistance
        if trend == 'bull':
            return 'long', support
        elif trend == 'bear':
            return 'short', resistance
        return None, None
