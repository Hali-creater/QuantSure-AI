from trade_engine import TradeAgent

def test_analyze():
    agent = TradeAgent()
    params = {
        "asset": "BTC-USD",
        "timeframe": "1h",
        "risk_profile": "Moderate"
    }
    res = agent.analyze(params)
    print(res)
    assert isinstance(res, dict)
    assert "market_regime" in res
    assert "signal" in res

if __name__ == "__main__":
    test_analyze()
    print("Test passed!")
