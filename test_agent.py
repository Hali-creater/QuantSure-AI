import unittest
from unittest.mock import MagicMock, patch
from agent import TradeAgent

class TestTradeAgent(unittest.TestCase):
    @patch('agent.OpenAI')
    def test_analyze_success(self, mock_openai):
        # Mocking the OpenAI client and its response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="🔍 Market Overview\nMarket bias: Bullish"))]
        mock_client.chat.completions.create.return_value = mock_response

        agent = TradeAgent()
        result = agent.analyze("Test market data")

        self.assertIn("🔍 Market Overview", result)
        self.assertIn("Bullish", result)
        mock_client.chat.completions.create.assert_called_once()

    @patch('agent.OpenAI')
    def test_analyze_error(self, mock_openai):
        # Mocking an exception
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Key Error")

        agent = TradeAgent()
        result = agent.analyze("Test market data")

        self.assertIn("Error during analysis: API Key Error", result)

if __name__ == "__main__":
    unittest.main()
