import sys
from agent import TradeAgent

def main():
    print("--- AI Trade Prediction & Confirmation Agent ---")
    print("Welcome, Senior Analyst. Please provide the market data for analysis.")
    print("(Press Ctrl+D or Ctrl+Z to finish input)")
    print("-" * 50)

    try:
        user_input = sys.stdin.read().strip()
        if not user_input:
            print("No data provided. Exiting.")
            return

        print("\nAnalyzing market data... Please wait.\n")

        agent = TradeAgent()
        # Note: In a real environment, we'd ensure the API key is set.
        # For demonstration purposes, we will try to call it.
        # If the key is missing, it will gracefully report the error.

        analysis = agent.analyze(user_input)

        print("--- ANALYSIS REPORT ---")
        print(analysis)
        print("-" * 50)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
