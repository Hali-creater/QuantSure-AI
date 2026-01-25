# Institutional AI Trade Prediction & Confirmation Agent

A professional AI agent for market analysis and trade confirmation. This agent follows institutional-grade analysis frameworks, including Smart Money Concepts (SMC), Market Regime Detection, and Multi-Timeframe Analysis to provide objective market insights.

## Features

- **Market Regime Detection:** Analyzes trend strength (ADX), volatility (ATR%), and direction (EMA Slopes).
- **Multi-Timeframe Analysis:** Aligns current timeframe setups with higher timeframe bias.
- **SMC Concepts:** Detects Break of Structure (BOS) and Fair Value Gaps (FVG).
- **Conviction Grading:** Grades setups (High A, Medium B, Low C) based on confluence factors.
- **Risk Management:** Standardized risk models with Entry Zones, Invalidation levels, and RR potential.
- **"Why Not" Logic:** Detailed explanations for "WAIT" signals explaining which conditions failed.

## Project Structure

- `trade_engine.py`: The core analysis engine (formerly `agent.py`).
- `app.py`: Streamlit web dashboard with professional dark theme.
- `main.py`: CLI entry point for terminal-based analysis.
- `requirements.txt`: Project dependencies (institutional trading libraries).

## Setup

1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Web Interface (Streamlit) - Recommended
Run the professional web dashboard:
```bash
streamlit run app.py
```

### Option 2: CLI Tool
Run the agent via the command line:
```bash
python main.py
```

## 🎯 Example Strategies & Testing Guide

To verify that the agent is working correctly, try the following test cases in the **Asset Name** input:

### 1. Trend Continuation Setup
*   **Asset:** `BTC-USD`
*   **Timeframe:** `1h` or `4h`
*   **Expected Result:** Likely a **Bullish/Bearish Continuation** if the market has a clear direction.
*   **Check:** See if the **Market Regime** shows "Trending" and the **Higher TF Bias** aligns.

### 2. Commodity Normalization (Gold)
*   **Asset:** `XAU/USD` or `Gold`
*   **Timeframe:** `1h`
*   **Expected Result:** The agent should automatically normalize this to `GC=F` (Gold Futures) and fetch data correctly.

### 3. Forex Market
*   **Asset:** `EUR/USD`
*   **Timeframe:** `15m`
*   **Expected Result:** Should normalize to `EURUSD=X` and provide a "Range Trade" or "Momentum" setup depending on current volatility.

### 4. Interpretation of "WAIT" Signals
If the agent returns a **WAIT** signal, check the **Notes** at the bottom. It will explain specifically why it isn't taking a trade:
*   "Higher timeframe bias conflicts with current structure."
*   "Market is in a ranging regime."
*   "RSI is in neutral territory."

## Disclaimer

🛑 **This is NOT Financial Advice.** This AI agent is a decision-support system. Trading involves significant risk. Always use proper risk management and never trade more than you can afford to lose.
