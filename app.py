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
    .result-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }
    .result-header {
        color: #00ffcc;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2422/2422796.png", width=100)
    st.title("Settings")

    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo"], index=0)

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
        rsi = st.checkbox("RSI")
        macd = st.checkbox("MACD")
        ema_sma = st.checkbox("EMA/SMA")
    with col_ind2:
        fib = st.checkbox("Fibonacci")
        sr = st.checkbox("S/R Levels")
        patterns = st.checkbox("Chart Patterns")

# Main Content
st.title("💹 Institutional AI Trade Predictor")
st.markdown("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 Market Details")

    asset_name = st.text_input("Asset Name", placeholder="e.g. Bitcoin, EUR/USD, AAPL")

    market_data = st.text_area(
        "Market Context (Optional)",
        height=150,
        placeholder="Enter any additional market context, news, or observations..."
    )

    predict_button = st.button("🚀 PREDICT TRADE NOW", use_container_width=True)

with col2:
    st.subheader("🎯 Prediction Result")

    if predict_button:
        if not api_key:
            st.error("Please provide an OpenAI API Key in the sidebar.")
        elif not asset_name:
            st.warning("Please enter an Asset Name.")
        else:
            with st.spinner("Analyzing market structure and institutional flow..."):
                try:
                    # Prepare indicators string
                    selected_indicators = []
                    if rsi: selected_indicators.append("RSI")
                    if macd: selected_indicators.append("MACD")
                    if ema_sma: selected_indicators.append("EMA/SMA")
                    if fib: selected_indicators.append("Fibonacci")
                    if sr: selected_indicators.append("Support/Resistance")
                    if patterns: selected_indicators.append("Chart Patterns")

                    indicators_str = ", ".join(selected_indicators) if selected_indicators else "None selected"

                    # Construct full context
                    full_context = f"""
Asset: {asset_name}
Category: {category}
Market Type: {market_type}
Timeframe: {timeframe}
Risk Profile: {risk_profile}
Selected Indicators: {indicators_str}

Additional Context:
{market_data}
"""

                    agent = TradeAgent(api_key=api_key, model=model)

                    analysis = agent.analyze(full_context)

                    # Display the result
                    st.markdown(analysis)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.info("Fill in the parameters and press 'PREDICT TRADE NOW' to see the institutional analysis.")

# Disclaimer
st.divider()
st.caption("⚠️ **Disclaimer:** This AI agent is a decision-support system and NOT a financial advisor. Trading involves significant risk. Never trade more than you can afford to lose. Smart Money Concepts (SMC) are probabilistic frameworks.")
