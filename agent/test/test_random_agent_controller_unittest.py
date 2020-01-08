import unittest
from unittest import TestCase

from agents.random_agent_controller import RandomAgentController
from agents.agent import Agent
from agents.prediction_market_adapter import NUM_PREDICTIONS
from test.test_agent_controller_utils import *


class TestRandomAgentController(TestCase):
    N = 10  # repeat checks several times because of randomness
    controller = RandomAgentController(Agent())

    def test_is_betting_period(self):
        for n in range(self.N):
            self.assertTrue(only_once_during_first_half_day(self.controller.is_betting_period,
                            n*NUM_PREDICTIONS))

    def test_is_ranking_period(self):
        for n in range(self.N):
            self.assertTrue(only_once_during_first_half_day(self.controller.is_ranking_period,
                            n*NUM_PREDICTIONS))

    def test_is_collecting_period(self):
        for n in range(self.N):
            self.assertTrue(only_once_during_second_half_day(self.controller.is_collecting_period,
                            n*NUM_PREDICTIONS))

    def test_bet_before_rank(self):
        for n in range(self.N):
            self.assertTrue(first_this_then_that(self.controller.is_betting_period,
                            self.controller.is_ranking_period, n*NUM_PREDICTIONS))


if __name__ == '__main__':
    unittest.main()
