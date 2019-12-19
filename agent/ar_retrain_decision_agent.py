from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_absolute_error
import pandas as pd

from agent import Agent
from prediction_market_adapter import ACCOUNT_0, NUM_PREDICTIONS, TOP_TIER_THRESHOLD


class ArRetrainDecisionAgent(Agent):
    """Agent that uses autoregression with public data only.
       It fits its model again after each day.
       It only bets if its new model returns similar results to the last
       successful model.

    Attributes:
        models: list of autoregression models trained each day on all available
               history and the length of that history. The list only contains models trained
               to predict for days that haven't passed yet. Newest first.
        last_successful_model: last model that would have won top tier.
        to_predict_for: first time slice to predict for.
        history: past aggregate energy consumption (as a list).
    """
    MODEL_SIMILARITY_THRESHOLD = 70

    def __init__(self, account=ACCOUNT_0):
        super(ArRetrainDecisionAgent, self).__init__(account)
        self.history = list(pd.read_pickle('./data/agg_history.pkl').aggregate_consumption)
        # None appended as we are not predicting for first day
        self.models = [{'model': AR(self.history).fit(), 'train_amt': len(self.history)}, None]
        self.last_successful_model = None
        self.to_predict_for = len(self.history) + NUM_PREDICTIONS

    def predict(self, n):
        if n != NUM_PREDICTIONS:
            return None

        # corresponds to first time slice of next prediciton range
        self.to_predict_for += NUM_PREDICTIONS

        # predict all but only take last n
        predictions = self.models[0]['model'].predict(
                                    start=self.models[0]['train_amt'],
                                    end=self.to_predict_for-1,
                                    dynamic=False)[-n:]
        self.models[0]['predictions'] = predictions

        if self.last_successful_model is None:
            return None

        # predict using last successful model for comparision
        last_successful_model_predictions = self.last_successful_model['model'].predict(
                                         start=self.last_successful_model['train_amt'],
                                         end=self.to_predict_for-1,
                                         dynamic=False)[-n:]

        mae = mean_absolute_error(predictions, last_successful_model_predictions)
        if mae > ArRetrainDecisionAgent.MODEL_SIMILARITY_THRESHOLD:
            return None

        return list(map(int, predictions))

    def update_aggregate_data(self):
        self.history += self.prediction_market.get_latest_aggregate_consumptions()
        self.update_models()

    def update_models(self):
        # only None at the start
        if self.models[-1] is not None:
            mae = mean_absolute_error(self.history[-NUM_PREDICTIONS:],
                                      self.models[-1]['predictions'])
            if mae <= TOP_TIER_THRESHOLD:
                self.last_successful_model = self.models[-1]

        self.models = [{'model': AR(self.history).fit(),
                        'train_amt': len(self.history)}] + self.models[:-1]
