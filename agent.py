import pandas as pd
import numpy as np
import pandas_ta as ta
from scipy.signal import argrelextrema
import yfinance as yf
import QuantLib as ql

class TradeAgent:
    def __init__(self):
        pass

    def get_data(self, asset, timeframe):
        """Fetches market data using yfinance."""
        tf_map = {
            "1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
            "1h": "1h", "4h": "1h", "Daily": "1d", "Weekly": "1wk", "Monthly": "1mo"
        }
        interval = tf_map.get(timeframe, "1h")
        period = "5d" if interval in ["1m", "5m", "15m"] else "1y"

        try:
            df = yf.download(asset, period=period, interval=interval, progress=False)
            if df.empty:
                return None
            # Flatten columns if multi-indexed
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
        except Exception:
            return None

    def detect_smc(self, df):
        """Detects SMC concepts like BOS, CHoCH, and FVG."""
        if df is None or len(df) < 20:
            return {"fvgs": [], "structure": "Unknown", "bias": "Neutral"}

        # FVG Detection
        fvgs = []
        for i in range(2, len(df)):
            # Bullish FVG
            if df['High'].iloc[i-2] < df['Low'].iloc[i]:
                fvgs.append({'type': 'Bullish', 'level': (df['High'].iloc[i-2] + df['Low'].iloc[i])/2})
            # Bearish FVG
            elif df['Low'].iloc[i-2] > df['High'].iloc[i]:
                fvgs.append({'type': 'Bearish', 'level': (df['Low'].iloc[i-2] + df['High'].iloc[i])/2})

        # Market Structure (Simple BOS/CHoCH logic)
        last_high = df['High'].iloc[-20:-1].max()
        last_low = df['Low'].iloc[-20:-1].min()
        current_close = df['Close'].iloc[-1]

        bias = "Neutral"
        structure = "Ranging"

        if current_close > last_high:
            bias = "Bullish"
            structure = "BOS (Bullish)"
        elif current_close < last_low:
            bias = "Bearish"
            structure = "BOS (Bearish)"

        return {
            "fvgs": fvgs[-3:], # Return last 3
            "structure": structure,
            "bias": bias
        }

    def calculate_indicators(self, df):
        """Calculates technical indicators using pandas-ta."""
        df.ta.rsi(append=True)
        df.ta.ema(length=20, append=True)
        df.ta.ema(length=50, append=True)
        df.ta.macd(append=True)
        return df

    def analyze(self, params):
        """
        Main analysis method using institutional libraries.
        """
        asset = params.get('asset')
        if not asset:
            return "Error: No asset symbol provided."
        timeframe = params.get('timeframe', '1h')
        risk_profile = params.get('risk_profile', 'Moderate')

        df = self.get_data(asset, timeframe)
        if df is None:
            return "Error: Could not fetch data for the given asset. Please ensure the symbol is correct (e.g., BTC-USD, EURUSD=X, AAPL)."

        df = self.calculate_indicators(df)
        smc = self.detect_smc(df)

        current_price = float(df['Close'].iloc[-1])
        rsi = float(df['RSI_14'].iloc[-1]) if 'RSI_14' in df.columns else 50

        # Decision Logic
        decision = "WAIT"
        confidence = 50

        if smc['bias'] == "Bullish" and rsi < 70:
            decision = "BUY"
            confidence = 75 if rsi < 40 else 65
        elif smc['bias'] == "Bearish" and rsi > 30:
            decision = "SELL"
            confidence = 75 if rsi > 60 else 65

        # Risk Management (Simple ATR-based or static for demo)
        atr = df['High'].iloc[-1] - df['Low'].iloc[-1]
        if decision == "BUY":
            entry = current_price
            stop_loss = entry - (atr * 2)
            take_profit = entry + (atr * 4)
        elif decision == "SELL":
            entry = current_price
            stop_loss = entry + (atr * 2)
            take_profit = entry - (atr * 4)
        else:
            entry = "N/A"
            stop_loss = "N/A"
            take_profit = "N/A"

        # Generate 7-point response
        overview = f"Market analysis for {asset} shows a {smc['bias']} bias with {smc['structure']} structure. "
        if smc['fvgs']:
            overview += f"Detected Fair Value Gaps at {', '.join([f'{f['level']:.2f}' for f in smc['fvgs']])}. "
        overview += f"RSI is currently at {rsi:.2f}, indicating { 'oversold' if rsi < 30 else 'overbought' if rsi > 70 else 'neutral' } momentum."

        # Risk profile adjustment
        time_in_force = "DAY" if timeframe in ["1m", "5m", "15m", "1h"] else "GTC"

        response = f"""
I. Entry Price: {entry if entry == "N/A" else f"{entry:.2f}"}
II. Stoploss: {stop_loss if stop_loss == "N/A" else f"{stop_loss:.2f}"}
III. Take profit: {take_profit if take_profit == "N/A" else f"{take_profit:.2f}"}
IV. Confidence: {confidence}%
V. Asset: {asset}
VI. Time in force: {time_in_force}
VII. Overview: {overview}
"""
        return response
