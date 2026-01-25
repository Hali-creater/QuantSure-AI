import streamlit as st
import os
from trade_engine import TradeAgent
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

# Load Bootstrap & Tailwind for custom styling
st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">', unsafe_allow_html=True)
st.markdown('<script src="https://cdn.tailwindcss.com"></script>', unsafe_allow_html=True)

# Custom CSS for a professional look matching the images
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    body {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .main-card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1rem;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(58, 123, 213, 0.4);
        color: white;
    }
    .result-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .metric-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #8b949e;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #58a6ff;
    }
    .info-box {
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 10px;
        font-weight: 600;
    }
    .bg-blue-custom { background-color: rgba(56, 139, 253, 0.15); border: 1px solid rgba(56, 139, 253, 0.4); color: #58a6ff; }
    .bg-green-custom { background-color: rgba(63, 185, 80, 0.15); border: 1px solid rgba(63, 185, 80, 0.4); color: #3fb950; }
    .bg-yellow-custom { background-color: rgba(210, 153, 34, 0.15); border: 1px solid rgba(210, 153, 34, 0.4); color: #d29922; }

    /* Input styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #0d1117 !important;
        border-color: #30363d !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2422/2422796.png", width=80)
    st.title("Institutional Agent")

    st.markdown("---")

    st.subheader("📋 Trade Parameters")
    category = st.selectbox("Trading Category", ["Options", "Futures", "Spot"])
    market_type = st.selectbox("Market/Exchange Type", ["Cryptos", "Stocks", "Commodity", "Forex", "Indices"])
    timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "30m", "1h", "4h", "Daily", "Weekly", "Monthly"])
    risk_profile = st.selectbox("Risk Profile", ["Conservative", "Moderate", "Aggressive"])

    st.markdown("---")

    st.subheader("🛠️ Indicators/Patterns")
    rsi = st.checkbox("RSI", value=True)
    macd = st.checkbox("MACD")
    ema_sma = st.checkbox("EMA/SMA", value=True)
    bb = st.checkbox("Bollinger Bands")
    fib = st.checkbox("Fibonacci")
    sr = st.checkbox("S/R Levels", value=True)
    patterns = st.checkbox("Chart Patterns")
    volume = st.checkbox("Volume Profile")

# Main Content
st.title("💹 Institutional AI Trade Predictor")
st.markdown("Experience institutional-grade Smart Money Concepts (SMC) and market analysis.")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("📝 Market Details")

    asset_name = st.text_input("Asset Name", placeholder="e.g. BTC-USD, AAPL, EURUSD=X")

    market_data = st.text_area(
        "Market Context (Optional)",
        height=80,
        placeholder="Enter news, institutional flow observations, etc."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    predict_button = st.button("🚀 PREDICT TRADE NOW")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if predict_button:
        if not asset_name:
            st.warning("Please enter an Asset Name.")
        else:
            with st.spinner("Analyzing market structure and institutional flow..."):
                try:
                    params = {
                        "asset": asset_name,
                        "category": category,
                        "market_type": market_type,
                        "timeframe": timeframe,
                        "risk_profile": risk_profile,
                        "context": market_data,
                        "indicators": {
                            "rsi": rsi, "macd": macd, "ema_sma": ema_sma, "fib": fib,
                            "sr": sr, "patterns": patterns, "bb": bb, "volume": volume
                        }
                    }

                    agent = TradeAgent()
                    res = agent.analyze(params)

                    if isinstance(res, str) and res.startswith("Error"):
                        st.error(res)
                    else:
                        st.markdown('<div class="main-card">', unsafe_allow_html=True)
                        st.markdown(f'<div class="result-header"><span style="color: #58a6ff;">📊</span> Prediction Result: {res["signal"]}</div>', unsafe_allow_html=True)

                        m1, m2, m3 = st.columns(3)
                        with m1:
                            st.markdown(f'<div class="metric-box"><div class="metric-label">I. Entry Zone</div><div class="metric-value">{res["entry_zone"]}</div></div>', unsafe_allow_html=True)
                        with m2:
                            st.markdown(f'<div class="metric-box"><div class="metric-label">II. Invalidation</div><div class="metric-value">{res["stop_loss"]}</div></div>', unsafe_allow_html=True)
                        with m3:
                            st.markdown(f'<div class="metric-box"><div class="metric-label">III. TP Target</div><div class="metric-value">{res["tp_target"]}</div></div>', unsafe_allow_html=True)

                        i1, i2, i3, i4 = st.columns(4)
                        with i1: st.markdown(f'<div class="info-box bg-blue-custom">Confidence: {res["confidence"]}</div>', unsafe_allow_html=True)
                        with i2: st.markdown(f'<div class="info-box bg-blue-custom">Conviction: {res["conviction"]}</div>', unsafe_allow_html=True)
                        with i3: st.markdown(f'<div class="info-box bg-green-custom">Asset: {res["asset"]}</div>', unsafe_allow_html=True)
                        with i4: st.markdown(f'<div class="info-box bg-yellow-custom">TIF: {res["time_in_force"]}</div>', unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="mt-4">
                            <h5 style="color: #8b949e; font-size: 0.9rem; text-transform: uppercase;">Detailed Overview</h5>
                            <div style="font-size: 0.95rem; line-height: 1.8;">
                                <p><strong>🌍 Market Regime:</strong> {res["market_regime"]}</p>
                                <p><strong>🔝 Higher TF Bias:</strong> {res["htf_bias"]}</p>
                                <p><strong>🛠️ Setup Type:</strong> {res["setup_type"]}</p>
                                <p><strong>📡 Signal:</strong> {res["signal"]}</p>
                                <p><strong>⚖️ Risk Model:</strong> Entry: {res["entry_zone"]} | Invalidation: {res["invalidation"]} | Potential: {res["rr_potential"]} | {res["risk_hint"]}</p>
                                <p><strong>📊 Historical Context:</strong> {res["historical_stats"]}</p>
                                <p><strong>📝 Notes:</strong> {res["notes"]}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown('<hr style="border-color: #30363d; margin: 20px 0;">', unsafe_allow_html=True)
                        st.markdown('<p style="font-size: 0.8rem; color: #8b949e; text-align: center;">🛑 This is NOT Financial Advice. Trading involves significant risk.</p>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.markdown('<div class="main-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px; color: #8b949e; text-align: center;">'
                    '<span style="font-size: 4rem; margin-bottom: 20px;">📈</span>'
                    '<h4>Ready for Analysis</h4>'
                    '<p>Enter market details and press "PREDICT TRADE NOW" to receive an institutional SMC prediction.</p>'
                    '</div>', unsafe_allow_html=True)

# Disclaimer
st.caption("⚠️ **Disclaimer:** This AI agent is a decision-support system based on Smart Money Concepts (SMC). Trading involves significant risk. Always use proper risk management.")
