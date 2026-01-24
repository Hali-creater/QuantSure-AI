import sys
from agent import TradeAgent

def main():
    print("--- Professional AI Trade Prediction & Confirmation Agent ---")

    agent = TradeAgent()

    asset = input("Enter Asset Symbol (e.g., BTC-USD): ").strip()
    if not asset:
        print("No asset symbol provided. Exiting.")
        sys.exit(0)

    print("\nAnalyzing market data for {}... Please wait.\n".format(asset))
    params = {
        "asset": asset,
        "timeframe": "1h",
        "risk_profile": "Moderate"
    }
    analysis = agent.analyze(params)

    print("-" * 50)
    print(analysis)
    print("-" * 50)

if __name__ == "__main__":
    main()
