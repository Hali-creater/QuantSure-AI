import unittest
from agent import TradeAgent

class TestTradeAgent(unittest.TestCase):

    def test_initialization(self):
        agent = TradeAgent()
        self.assertIsNotNone(agent)

    def test_analyze_empty_asset(self):
        agent = TradeAgent()
        result = agent.analyze({})
        self.assertIn("Error", result)

if __name__ == '__main__':
    unittest.main()
