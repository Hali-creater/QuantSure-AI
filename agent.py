import pandas as pd
import numpy as np
import pandas_ta as ta
from scipy.signal import argrelextrema
import yfinance as yf

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

        # Market Structure (Swing-based BOS logic)
        highs = df['High'].values
        lows = df['Low'].values

        # Find local peaks/valleys
        order = 5
        peaks = argrelextrema(highs, np.greater, order=order)[0]
        valleys = argrelextrema(lows, np.less, order=order)[0]

        last_peak = highs[peaks[-1]] if len(peaks) > 0 else df['High'].iloc[-20:-1].max()
        last_valley = lows[valleys[-1]] if len(valleys) > 0 else df['Low'].iloc[-20:-1].min()

        current_close = df['Close'].iloc[-1]
        bias = "Neutral"
        structure = "Ranging"

        if current_close > last_peak:
            bias = "Bullish"
            structure = "BOS (Bullish)"
        elif current_close < last_valley:
            bias = "Bearish"
            structure = "BOS (Bearish)"

        return {
            "fvgs": fvgs[-3:], # Return last 3
            "structure": structure,
            "bias": bias
        }

    def calculate_indicators(self, df, indicators=None):
        """Calculates technical indicators using pandas-ta."""
        if indicators is None or indicators.get('rsi', True):
            df.ta.rsi(append=True)
        if indicators is None or indicators.get('ema_sma', True):
            df.ta.ema(length=20, append=True)
            df.ta.ema(length=50, append=True)
        if indicators is None or indicators.get('macd', False):
            df.ta.macd(append=True)
        if indicators is not None and indicators.get('bb', False):
            df.ta.bbands(append=True)

        df.ta.atr(append=True)
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

        df = self.calculate_indicators(df, params.get('indicators'))
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

        # Risk Management (Institutional ATR-based)
        atr = float(df['ATR_14'].iloc[-1]) if 'ATR_14' in df.columns and not np.isnan(df['ATR_14'].iloc[-1]) else (df['High'].iloc[-1] - df['Low'].iloc[-1])
        if atr == 0:
            atr = current_price * 0.01 # Fallback to 1%

        # Risk Multipliers based on profile
        multipliers = {
            'Conservative': {'sl': 1.5, 'tp': 3.0},
            'Moderate': {'sl': 2.0, 'tp': 4.0},
            'Aggressive': {'sl': 2.5, 'tp': 6.0}
        }
        mult = multipliers.get(risk_profile, multipliers['Moderate'])

        if decision == "BUY":
            entry = current_price
            stop_loss = entry - (atr * mult['sl'])
            take_profit = entry + (atr * mult['tp'])
        elif decision == "SELL":
            entry = current_price
            stop_loss = entry + (atr * mult['sl'])
            take_profit = entry - (atr * mult['tp'])
        else:
            entry = "N/A"
            stop_loss = "N/A"
            take_profit = "N/A"

        # Generate 7-point response
        trade_nature = "Wait and Watch"
        if decision == "BUY":
            trade_nature = "Bullish Continuation" if smc['structure'] == "BOS (Bullish)" else "Potential Mean Reversion"
        elif decision == "SELL":
            trade_nature = "Bearish Continuation" if smc['structure'] == "BOS (Bearish)" else "Potential Mean Reversion"

        overview = f"Market analysis for {asset} shows a {smc['bias']} bias with {smc['structure']} structure. This trade has the nature of a **{trade_nature}**. "
        if smc['fvgs']:
            overview += f"Detected Fair Value Gaps at {', '.join([f'{f['level']:.2f}' for f in smc['fvgs']])}. "
        overview += f"RSI is currently at {rsi:.2f}, indicating { 'oversold' if rsi < 30 else 'overbought' if rsi > 70 else 'neutral' } momentum."

        # Risk profile adjustment
        time_in_force = "DAY" if timeframe in ["1m", "5m", "15m", "1h"] else "GTC"

        response = f"**I. Entry Price:** {entry if entry == 'N/A' else f'{entry:.2f}'}\n\n"
        response += f"**II. Stoploss:** {stop_loss if stop_loss == 'N/A' else f'{stop_loss:.2f}'}\n\n"
        response += f"**III. Take profit:** {take_profit if take_profit == 'N/A' else f'{take_profit:.2f}'}\n\n"
        response += f"**IV. Confidence:** {confidence}%\n\n"
        response += f"**V. Asset:** {asset}\n\n"
        response += f"**VI. Time in force:** {time_in_force}\n\n"
        response += f"**VII. Overview:** {overview}"
        return response
