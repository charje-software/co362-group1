import unittest
from unittest import TestCase, mock

from agents.prediction_market_adapter import NUM_PREDICTIONS
from agents.agent import Agent


class TestAgent(TestCase):

    def test_place_bet(self):
        with mock.patch('agents.agent.PredictionMarketAdapter', autospec=True) \
                    as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account, logging=False)
            predictions = [agent.DEFAULT_PREDICTION] * NUM_PREDICTIONS

            agent.place_bet()

            mock_prediction_market.place_bet.assert_called_with(account,
                                                                Agent.DEFAULT_BETTING_AMOUNT,
                                                                predictions)
            agent.place_bet()

            mock_prediction_market.place_bet.assert_called_with(account,
                                                                Agent.DEFAULT_BETTING_AMOUNT,
                                                                predictions)

    def test_rank_bet(self):
        with mock.patch('agents.agent.PredictionMarketAdapter', autospec=True) \
                    as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account, logging=False)
            agent.prediction_history = [[75] * NUM_PREDICTIONS, None, None]
            agent.aggregate_history = [75] * NUM_PREDICTIONS

            agent.rank_bet()

            mock_prediction_market.rank.assert_called_once_with(account)

    def test_collect_reward(self):
        with mock.patch('agents.agent.PredictionMarketAdapter', autospec=True) \
                    as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account, logging=False)
            agent.prediction_history = [[75] * NUM_PREDICTIONS, None, None]
            agent.aggregate_history = [75] * NUM_PREDICTIONS
            mock_prediction_market.get_winning_tier.return_value = 'top'

            agent.collect_reward()

            mock_prediction_market.transfer_reward.assert_called_once_with(account)

    def test_no_rank_if_no_bet(self):
        with mock.patch('agents.agent.PredictionMarketAdapter', autospec=True) \
                    as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account, logging=False)
            agent.prediction_history = [None, None, None]

            agent.rank_bet()

            mock_prediction_market.rank.assert_not_called()

    def test_no_rank_if_lost(self):
        with mock.patch('agents.agent.PredictionMarketAdapter', autospec=True) \
                    as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account, logging=False)
            agent.prediction_history = [[1000] * NUM_PREDICTIONS,
                                        [75] * NUM_PREDICTIONS, [75] * NUM_PREDICTIONS]
            agent.aggregate_history = [75] * NUM_PREDICTIONS

            agent.rank_bet()

            mock_prediction_market.rank.assert_not_called()

    def test_no_transfer_if_no_bet(self):
        with mock.patch('agents.agent.PredictionMarketAdapter', autospec=True) \
                    as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account, logging=False)
            agent.prediction_history = [None, None, None]

            agent.collect_reward()

            mock_prediction_market.transfer_reward.assert_not_called()


if __name__ == '__main__':
    unittest.main()
