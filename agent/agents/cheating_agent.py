import numpy as np
from sklearn.metrics import mean_absolute_error

from agents.agent import Agent
from agents.prediction_market_adapter import NUM_PREDICTIONS, TOP_TIER_THRESHOLD, ACCOUNT_0


class CheatingAgent(Agent):
    """Agent that uses onther agents predictions
       and doesn't have its own model.
    """

    def __init__(self, account=ACCOUNT_0, logging=True, **kwargs):
        super(CheatingAgent, self).__init__(account, logging, **kwargs)
        self.log('CheatingAgent')

    def predict_for_tomorrow(self):
        cheat = self.cheat()
        if not cheat:
            return None

        predicted_consumptions, helpers = cheat
        self.log('Thanks :) {0}'.format(helpers))
        return predicted_consumptions

    def cheat(self):
        """
        Returns False if there is not enough information to cheat, otherwise median predictions
        of current particpants that ranked top tier in the last completed period.
        """
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
            mae = mean_absolute_error(self.aggregate_history[-NUM_PREDICTIONS:],
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
