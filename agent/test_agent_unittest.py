import unittest
from unittest import TestCase, mock

from agent import Agent
from prediction_market_adapter import NUM_PREDICTIONS


class TestAgent(TestCase):

    def test_place_bet(self):
        with mock.patch('agent.PredictionMarketAdapter', autospec=True) as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account)
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
        with mock.patch('agent.PredictionMarketAdapter', autospec=True) as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account)

            agent.rank_bet()

            mock_prediction_market.rank.assert_called_once_with(account)

    def test_collect_reward(self):
        with mock.patch('agent.PredictionMarketAdapter', autospec=True) as MockPredictionMarket:
            mock_prediction_market = MockPredictionMarket.return_value
            account = '42'
            agent = Agent(account)

            agent.collect_reward()

            mock_prediction_market.transfer_reward.assert_called_once_with(account)

    def test_run_for_1_round(self):
        agent = Agent()

        with mock.patch('agent.time.sleep') as mock_time_sleep, \
                mock.patch('agent.Agent.place_bet') as mock_place_bet, \
                mock.patch('agent.Agent.rank_bet') as mock_rank_bet, \
                mock.patch('agent.Agent.collect_reward') as mock_collect_reward:
            agent.run(period_length=1, rounds=1, logging=False)

            mock_place_bet.assert_called_once()
            mock_rank_bet.assert_called_once()
            mock_collect_reward.assert_called_once()
            # off-set, 1 betting round, 2 more rounds for waiting and claiming
            self.assertEqual(mock_time_sleep.call_count, 1 + (1 + 2) * NUM_PREDICTIONS)

    def test_run_for_10_rounds(self):
        agent = Agent()

        with mock.patch('agent.time.sleep') as mock_time_sleep, \
                mock.patch('agent.Agent.place_bet') as mock_place_bet, \
                mock.patch('agent.Agent.rank_bet') as mock_rank_bet, \
                mock.patch('agent.Agent.collect_reward') as mock_collect_reward:
            agent.run(period_length=1, rounds=10, logging=False)

            self.assertEqual(mock_place_bet.call_count, 10)
            self.assertEqual(mock_rank_bet.call_count, 10)
            self.assertEqual(mock_collect_reward.call_count, 10)
            # off-set, 10 betting rounds, 2 more rounds for waiting and claiming
            self.assertEqual(mock_time_sleep.call_count, 1 + (10 + 2) * NUM_PREDICTIONS)


if __name__ == '__main__':
    unittest.main()
