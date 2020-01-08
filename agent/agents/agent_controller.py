import time
from datetime import datetime
import pandas as pd

from agents.prediction_market_adapter import PERIOD_LENGTH, NUM_PREDICTIONS


class AgentController:
    """Simple controller for Agent.

    The AgentController calls Agent's functions according to the timings
    decriped at the top of the Agent class.

    Attributes:
        agent:        the Agent to control.
    """
    OFFSET = pd.Timedelta('5s')  # wait for oracle to act

    def __init__(self, agent):
        self.agent = agent

    def run(self, start_time, end_time, time_delta=PERIOD_LENGTH):
        """
        Calls schedules all decisions of agent and interactions with the prediction market
        from start_time to end_time.

        Args:
            start_time: actual date and time corresponding to 2014-01-28 00:00:00
            end_time:   actual date and time for last agent actions
            time_delta: how long to actually wait for 30mins to pass
        """
        now = datetime.now()
        if now < start_time:
            time.sleep((start_time - now).seconds)
        elif start_time < now:
            raise ValueError('Start time cannot be in the past!')

        start_time += AgentController.OFFSET
        end_time += AgentController.OFFSET

        now = datetime.now()
        next_time = start_time + time_delta
        period = 0
        while now <= end_time:
            self.act_during(period)
            period += 1
            time.sleep((next_time - now).seconds)
            next_time += time_delta
            now = datetime.now()

    def act_during(self, period):
        if period > 0:
            self.agent.update_per_period()
            if period % NUM_PREDICTIONS == 0:
                print('-' * 59)
                print(' ' * 20 + 'DAY {0}'.format(period // NUM_PREDICTIONS))
                print('-' * 59)
                self.agent.update_daily()

        if self.is_betting_period(period):
            self.agent.place_bet()

        if self.is_ranking_period(period):
            self.agent.rank_bet()

        if self.is_collecting_period(period):
            self.agent.collect_reward()

    def is_betting_period(self, period):
        """
        Returns True at midnight.

        Can be overridden for controllers with other timings.
        Must be between 00:00 and 12:00 (i.e. period 0-23 of each day).
        Must be <= to period picked for rank_bet.
        """
        return period % NUM_PREDICTIONS == 0

    def is_ranking_period(self, period):
        """
        Returns True at midnight.

        Can be overridden for controllers with other timings.
        Must be between 00:00 and 12:00 (i.e. period 0-23 of each day).
        Must be <= to period picked for rank_bet.
        """
        return period % NUM_PREDICTIONS == 0

    def is_collecting_period(self, period):
        """
        Returns True at noon.

        Can be overridden for controllers with other timings.
        Must be between 12:00 and 00:00 (i.e. period 24-47 of each day).
        Must be <= to period picked for rank_bet.
        """
        return period % NUM_PREDICTIONS == NUM_PREDICTIONS // 2
