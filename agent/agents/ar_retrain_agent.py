import pandas as pd
from statsmodels.tsa.ar_model import AR

from agents.agent import Agent
from agents.prediction_market_adapter import ACCOUNT_0, NUM_PREDICTIONS


class ArRetrainAgent(Agent):
    """Agent that uses autoregression with public data only.
       It fits its model again after each day.

    Attributes:
        model: an autoregression model trained each day on all available history
               used for predicting future aggregate energy consumption.
    """

    def __init__(self, account=ACCOUNT_0, logging=True, **kwargs):
        super(ArRetrainAgent, self).__init__(account, logging, **kwargs)
        self.model = AR(self.aggregate_history).fit()
        self.log('ArRetrainAgent')

    def predict_for_tomorrow(self):
        # need to predict all starting from train_amt, but only return last NUM_PREDICTIONS
        # there is a 1 day offset between the period predicted for and the training data
        train_amt = len(self.aggregate_history)
        self.model = AR(self.aggregate_history).fit()
        predictions = self.model.predict(start=train_amt,
                                         end=train_amt+2*NUM_PREDICTIONS-1,
                                         dynamic=False)[-NUM_PREDICTIONS:]
        return list(map(int, predictions))
