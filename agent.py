import os
from openai import OpenAI
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT

load_dotenv()

class TradeAgent:
    def __init__(self, api_key=None, model="gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API Key is required. Set it in .env file or pass it to the constructor.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def analyze(self, market_data):
        """
        Analyzes the provided market data using the system prompt.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Please analyze the following market data and provide a trade recommendation:\n\n{market_data}"}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during analysis: {str(e)}"

if __name__ == "__main__":
    # Quick test
    try:
        agent = TradeAgent()
        print("TradeAgent initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize TradeAgent: {e}")
