from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_absolute_error
import pandas as pd

from agents.agent import Agent
from agents.prediction_market_adapter import ACCOUNT_0, NUM_PREDICTIONS, TOP_TIER_THRESHOLD


class ArRetrainDecisionAgent(Agent):
    """Agent that uses autoregression with public data only.
       It fits its model again after each day.
       It only bets if its new model returns similar results to the last
       successful model.

    Attributes:
        models: list of dictionaries of models, their train amount, and prediction for
                their respective betting round (in contrast to prediction_history, regardless
                of whether or not the agent bet). The list only contains models trained
                to predict for days that haven't passed yet. Newest first.
        last_successful_model: last model that would have won top tier.
        to_predict_for: first time slice to predict for.
    """
    MODEL_SIMILARITY_THRESHOLD = 70

    def __init__(self, account=ACCOUNT_0, logging=True, **kwargs):
        super(ArRetrainDecisionAgent, self).__init__(account, logging, **kwargs)
        # None as we are not predicting for first day or day before
        self.models = [None, None]
        self.last_successful_model = None
        self.to_predict_for = len(self.aggregate_history) + NUM_PREDICTIONS
        self.log('ArRetrainDecisionAgent')

    def predict_for_tomorrow(self):
        self.update_models()

        # corresponds to first time slice of next prediciton range
        self.to_predict_for += NUM_PREDICTIONS

        # predict all but only take last NUM_PREDICTIONS
        predictions = self.models[0]['model'].predict(
                                    start=self.models[0]['train_amt'],
                                    end=self.to_predict_for-1,
                                    dynamic=False)[-NUM_PREDICTIONS:]
        self.models[0]['predictions'] = predictions

        if self.last_successful_model is None:
            return None

        # predict using last successful model for comparision
        last_successful_model_predictions = self.last_successful_model['model'].predict(
                                         start=self.last_successful_model['train_amt'],
                                         end=self.to_predict_for-1,
                                         dynamic=False)[-NUM_PREDICTIONS:]

        mae = mean_absolute_error(predictions, last_successful_model_predictions)
        if mae > ArRetrainDecisionAgent.MODEL_SIMILARITY_THRESHOLD:
            return None

        return list(map(int, predictions))

    def update_models(self):
        """
        Updates current model and last successful model.
        """
        # only None at the start
        if self.models[-1] is not None:
            mae = mean_absolute_error(self.aggregate_history[-NUM_PREDICTIONS:],
                                      self.models[-1]['predictions'])
            if mae <= TOP_TIER_THRESHOLD:
                self.last_successful_model = self.models[-1]

        self.models = [{'model': AR(self.aggregate_history).fit(),
                        'train_amt': len(self.aggregate_history)}] + self.models[:-1]
