from random import randint

from agents.agent_controller import AgentController
from agents.prediction_market_adapter import NUM_PREDICTIONS


class RandomAgentController(AgentController):
    """Chooses random periods during allowed ranges for betting, ranking and
    collecting.

    Attributes:
        next_bet:     next period modulo NUM_PREDICTIONS for betting.
        next_rank:    next period modulo NUM_PREDICTIONS for ranking.
        next_collect: next period modulo NUM_PREDICTIONS for collecting.
    """
    def __init__(self, agent):
        super(RandomAgentController, self).__init__(agent)
        self.next_bet = randint(0, NUM_PREDICTIONS // 2 - 1)
        self.next_rank = randint(self.next_bet, NUM_PREDICTIONS // 2 - 1)
        self.next_collect = randint(NUM_PREDICTIONS // 2, NUM_PREDICTIONS - 1)

    def is_betting_period(self, period):
        if period % NUM_PREDICTIONS == NUM_PREDICTIONS // 2:
            self.next_bet = randint(0, NUM_PREDICTIONS // 2 - 1)
        return period % NUM_PREDICTIONS == self.next_bet

    def is_ranking_period(self, period):
        if period % NUM_PREDICTIONS == NUM_PREDICTIONS // 2:
            self.next_rank = randint(self.next_bet, NUM_PREDICTIONS // 2 - 1)
        return period % NUM_PREDICTIONS == self.next_rank

    def is_collecting_period(self, period):
        if period % NUM_PREDICTIONS == 0:
            self.next_collect = randint(NUM_PREDICTIONS // 2, NUM_PREDICTIONS - 1)
        return period % NUM_PREDICTIONS == self.next_collect
