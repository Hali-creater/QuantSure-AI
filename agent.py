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

    def analyze(self, market_data, image_bytes=None, image_format="jpeg"):
        """
        Analyzes the provided market data and optional image using the system prompt.
        """
        try:
            content = []
            content.append({"type": "text", "text": f"Please analyze the following market data and provide a trade recommendation:\n\n{market_data}"})

            if image_bytes:
                import base64
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{image_format};base64,{base64_image}"
                    }
                })

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": content}
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
