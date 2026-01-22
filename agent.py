import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT

load_dotenv()

class TradeAgent:
    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.system_prompt = SYSTEM_PROMPT

    def analyze(self, market_data: str) -> str:
        """
        Analyzes the provided market data using the AI Trade Prediction Agent.

        Args:
            market_data (str): A string containing market information, price action, and indicators.

        Returns:
            str: The structured analysis response from the agent.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Please analyze the following market data and provide your professional assessment:\n\n{market_data}"}
                ],
                temperature=0.2, # Low temperature for more objective analysis
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during analysis: {str(e)}"

if __name__ == "__main__":
    # Example usage
    agent = TradeAgent()
    sample_data = "BTC/USDT 1H timeframe. Current price 65000. Trend is bullish on 1D. Price just swept liquidity below 64500 and showed a CHoCH on 15m. RSI is at 45. FVG located at 64800-64900."
    # Note: This requires an API key in .env
    # print(agent.analyze(sample_data))
