import unittest
from unittest import TestCase

from agents.agent_controller import AgentController
from agents.agent import Agent
from test.test_agent_controller_utils import *


class TestAgentController(TestCase):
    controller = AgentController(Agent())

    def test_is_betting_period(self):
        self.assertTrue(only_once_during_first_half_day(self.controller.is_betting_period))

    def test_is_ranking_period(self):
        self.assertTrue(only_once_during_first_half_day(self.controller.is_ranking_period))

    def test_is_collecting_period(self):
        self.assertTrue(only_once_during_second_half_day(self.controller.is_collecting_period))

    def test_bet_before_rank(self):
        self.assertTrue(first_this_then_that(self.controller.is_betting_period,
                        self.controller.is_ranking_period))


if __name__ == '__main__':
    unittest.main()
