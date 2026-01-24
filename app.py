import streamlit as st
import os
from agent import TradeAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Institutional AI Trade Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #00ffcc;
        color: #0e1117;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00ccaa;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2422/2422796.png", width=100)
    st.title("Institutional Agent")

    st.markdown("""
    ### Local Analysis Engine
    The agent is now powered by local institutional libraries including:
    - **Pandas-TA** (Technical Analysis)
    - **QuantLib** (Risk Management)
    - **Scipy/Numpy** (SMC Logic)
    - **YFinance** (Market Data)
    """)

    st.divider()

    st.subheader("📋 Trade Parameters")
    category = st.selectbox("Trading Category", ["Options", "Futures", "Spot"])
    market_type = st.selectbox("Market/Exchange Type", ["Cryptos", "Stocks", "Commodity", "Forex", "Indices"])
    timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "30m", "1h", "4h", "Daily", "Weekly", "Monthly"])
    risk_profile = st.selectbox("Risk Profile", ["Conservative", "Moderate", "Aggressive"])

    st.divider()

    st.subheader("🛠️ Indicators/Patterns")
    col_ind1, col_ind2 = st.columns(2)
    with col_ind1:
        rsi = st.checkbox("RSI", value=True)
        macd = st.checkbox("MACD")
        ema_sma = st.checkbox("EMA/SMA", value=True)
    with col_ind2:
        fib = st.checkbox("Fibonacci")
        sr = st.checkbox("S/R Levels", value=True)
        patterns = st.checkbox("Chart Patterns")

# Main Content
st.title("💹 Institutional AI Trade Predictor")
st.markdown("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 Market Details")

    asset_name = st.text_input("Asset Symbol", placeholder="e.g. BTC-USD, AAPL, EURUSD=X")
    st.caption("Use Yahoo Finance symbols (e.g., BTC-USD for Bitcoin, EURUSD=X for Euro/Dollar)")

    market_data = st.text_area(
        "Market Context (Optional)",
        height=150,
        placeholder="Enter any additional market context, news, or observations..."
    )

    predict_button = st.button("🚀 PREDICT TRADE NOW", use_container_width=True)

with col2:
    st.subheader("🎯 Prediction Result")

    if predict_button:
        if not asset_name:
            st.warning("Please enter an Asset Symbol.")
        else:
            with st.spinner("Analyzing market structure and institutional flow..."):
                try:
                    params = {
                        "asset": asset_name,
                        "category": category,
                        "market_type": market_type,
                        "timeframe": timeframe,
                        "risk_profile": risk_profile,
                        "context": market_data
                    }

                    agent = TradeAgent()
                    analysis = agent.analyze(params)

                    # Display the result
                    st.markdown(analysis)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.info("Fill in the parameters and press 'PREDICT TRADE NOW' to see the institutional analysis.")

# Disclaimer
st.divider()
st.caption("⚠️ **Disclaimer:** This AI agent is a decision-support system and NOT a financial advisor. Trading involves significant risk. Never trade more than you can afford to lose. Smart Money Concepts (SMC) are probabilistic frameworks.")
