from random import randint

from agents.agent_controller import AgentController
from agents.prediction_market_adapter import NUM_PREDICTIONS


class LastChanceAgentController(AgentController):
    """Chooses last allowed periods for betting, ranking and collecting.
    """
    def is_betting_period(self, period):
        return period % NUM_PREDICTIONS == NUM_PREDICTIONS // 2 - 1

    def is_ranking_period(self, period):
        return self.is_betting_period(period)

    def is_collecting_period(self, period):
        return period % NUM_PREDICTIONS == NUM_PREDICTIONS - 1
