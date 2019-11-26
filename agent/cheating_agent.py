import numpy as np
from sklearn.metrics import mean_absolute_error

from agent import Agent
from prediction_market_adapter import NUM_PREDICTIONS, TOP_TIER_THRESHOLD, ACCOUNT_0


class CheatingAgent(Agent):
    """Agent that uses onther agents predictions
       and doesn't have its own model.

    Attributes:
        has_bet: list of booleans indicating whether or not the agent bet the last time
                 place_bet was called
        history: past aggregate energy consumption (as a list)
    """

    def __init__(self, account=ACCOUNT_0):
        super(CheatingAgent, self).__init__(account)
        self.has_bet = [False]
        self.history = []

    """
    Note that the cheating agent assumes that rank_bet is called after place_bet on any day.
    """

    def place_bet(self):
        """
        Override place_bet to cheat.
        """
        cheat = self.cheat()
        if not cheat:
            self.has_bet += [False]
            self.log('Will not bet during current betting round.')
            return

        predicted_consumptions, helpers = cheat

        self.log('Placing a bet. Predictions: {0}.'.format(predicted_consumptions))
        self.log('Thanks :) {0}'.format(helpers))
        self.prediction_market.place_bet(self.account, Agent.DEFAULT_BETTING_AMOUNT,
                                         predicted_consumptions)
        self.has_bet += [True]

    def rank_bet(self):
        if self.has_bet[-3]:
            super(CheatingAgent, self).rank_bet()

    def collect_reward(self):
        if self.has_bet[-3]:
            super(CheatingAgent, self).collect_reward()

    def cheat(self):
        """
        Returns False if there is not enough information to cheat, otherwise median predictions
        of current particpants that ranked top tier in the last completed period.
        """
        if len(self.history) < NUM_PREDICTIONS:
            return False

        participants = self.prediction_market.get_current_participants()
        if len(participants) == 0:
            return False

        # fetch predictions for all partipants
        others_predictions = \
            {participant: {'new': self.prediction_market.get_predictions_for_agent(participant)}
             for participant in participants}

        # fetch predictions from last completed round for current participants
        for participant in participants:
            try:
                old_preds = self.prediction_market.get_predictions_for_agent(participant, 2)
                others_predictions[participant]['old'] = old_preds
            except Exception:
                del others_predictions[participant]

        participants = list(others_predictions.keys())
        if len(participants) == 0:
            return False

        # rank participants based on performance in last completed round
        # and remove unless in top_tier
        for participant in participants:
            mae = mean_absolute_error(self.history[-NUM_PREDICTIONS:],
                                      others_predictions[participant]['old'])
            if mae > TOP_TIER_THRESHOLD:
                del others_predictions[participant]

        participants = list(others_predictions.keys())
        if len(participants) == 0:
            return False

        others_predictions_new = list(map(lambda entry: entry.get('new'),
                                          others_predictions.values()))

        predictions = list(map(np.median, zip(*others_predictions_new)))
        return list(map(int, predictions)), list(others_predictions.keys())

    def update_aggregate_data(self):
        self.history += self.prediction_market.get_latest_aggregate_consumptions()
