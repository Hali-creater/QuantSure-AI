import unittest
from unittest.mock import MagicMock, patch
from agent import TradeAgent

class TestTradeAgent(unittest.TestCase):

    @patch('agent.OpenAI')
    @patch('agent.os.getenv')
    def test_initialization_with_api_key(self, mock_getenv, mock_openai):
        mock_getenv.return_value = "test_key"
        agent = TradeAgent()
        self.assertEqual(agent.api_key, "test_key")

    @patch('agent.os.getenv')
    def test_initialization_without_api_key(self, mock_getenv):
        mock_getenv.return_value = None
        with self.assertRaises(ValueError):
            TradeAgent()

    @patch('agent.OpenAI')
    def test_analyze_success(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "✅ BUY\nTarget reached"
        mock_client.chat.completions.create.return_value = mock_response

        agent = TradeAgent(api_key="test_key")
        result = agent.analyze("EURUSD Bullish context")

        self.assertIn("✅ BUY", result)
        mock_client.chat.completions.create.assert_called_once()

    @patch('agent.OpenAI')
    def test_analyze_error(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        agent = TradeAgent(api_key="test_key")
        result = agent.analyze("BTC data")

        self.assertIn("Error during analysis", result)

if __name__ == '__main__':
    unittest.main()
