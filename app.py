import streamlit as st
import os
from agent import TradeAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Trade Prediction & Confirmation Agent",
    page_icon="📈",
    layout="wide"
)

# Professional Header
st.title("📈 AI Trade Prediction & Confirmation Agent")
st.markdown("""
*Institutional-grade market analysis and trade confirmation powered by GPT-4o.*
""")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)

    st.divider()
    st.markdown("""
    ### About this Agent
    This agent uses **Smart Money Concepts (SMC)** and institutional analysis frameworks to evaluate market data.
    It focuses on:
    - Market Context & Bias
    - Structure & Price Action
    - Liquidity & FVGs
    - Risk Management
    """)

# Main Content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Market Data Input")
    market_data = st.text_area(
        "Paste market data here (e.g., price action, RSI, levels, etc.):",
        height=300,
        placeholder="Example: EURUSD 1H - Bullish trend, just swept liquidity at 1.0850, FVG formed above..."
    )

    analyze_button = st.button("🚀 Analyze & Confirm Trade", use_container_width=True)

with col2:
    st.subheader("Analysis & Recommendation")

    if analyze_button:
        if not api_key:
            st.error("Please provide an OpenAI API Key in the sidebar.")
        elif not market_data.strip():
            st.warning("Please enter market data to analyze.")
        else:
            with st.spinner("Analyzing market data..."):
                try:
                    agent = TradeAgent(api_key=api_key, model=model)
                    analysis = agent.analyze(market_data)

                    # Displaying the analysis in a professional format
                    st.markdown("---")
                    st.markdown(analysis)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.info("Awaiting market data input for analysis...")

# Disclaimer
st.divider()
st.caption("⚠️ **Disclaimer:** This AI agent is a decision-support system and NOT a financial advisor. Trading involves significant risk. Never trade more than you can afford to lose.")
