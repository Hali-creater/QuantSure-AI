import sys
from agent import TradeAgent

def main():
    print("--- Professional AI Trade Prediction & Confirmation Agent ---")

    try:
        agent = TradeAgent()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nPlease enter the market data for analysis (Enter 'DONE' on a new line when finished):")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)

    market_data = "\n".join(lines)

    if not market_data.strip():
        print("No market data provided. Exiting.")
        sys.exit(0)

    print("\nAnalyzing market data... Please wait.\n")
    analysis = agent.analyze(market_data)

    print("-" * 50)
    print(analysis)
    print("-" * 50)

if __name__ == "__main__":
    main()
