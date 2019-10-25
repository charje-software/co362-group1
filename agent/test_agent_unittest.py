import unittest
from unittest import TestCase, mock

from agent import Agent


class TestAgent(TestCase):

    def test_place_bet(self):
        with mock.patch('agent.PredictionMarketAdapter', autospec=True) as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account)

            agent.place_bet()

            mock_prediction_market.place_bet.assert_called_once_with(account,
                                                                     Agent.DEFAULT_BETTING_AMOUNT)

    def test_collect_reward(self):
        with mock.patch('agent.PredictionMarketAdapter', autospec=True) as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account)

            agent.collect_reward()

            mock_prediction_market.transfer_reward.assert_called_once_with(account)


if __name__ == '__main__':
    unittest.main()
