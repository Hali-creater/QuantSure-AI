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

    def test_analyze_return_format(self):
        agent = TradeAgent()
        result = agent.analyze({'asset': 'BTC-USD'})
        self.assertIsInstance(result, dict)
        self.assertIn('entry', result)
        self.assertIn('stop_loss', result)
        self.assertIn('take_profit', result)
        self.assertIn('confidence', result)
        self.assertIn('asset', result)
        self.assertIn('time_in_force', result)
        self.assertIn('overview', result)

if __name__ == '__main__':
    unittest.main()
