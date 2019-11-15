import pandas as pd
from statsmodels.tsa.ar_model import AR

from agent import Agent
from prediction_market_adapter import ACCOUNT_0


class ArRetrainAgent(Agent):
    """Agent that uses autoregression with public data only.
       It fits its model again after each day.

    Attributes:
        model: a pretrained autoregression model used for predicting
               future aggregate energy consumption.
        history: past aggregate energy consumption (as a list)
    """

    def __init__(self, account=ACCOUNT_0):
        super(ArRetrainAgent, self).__init__(account)
        self.history = list(pd.read_pickle('./data/agg_history.pkl').aggregate_consumption)
        self.model = AR(self.history).fit()

    def predict(self, n):
        # need to predict all starting from START, but only return last n
        train_amt = len(self.history)
        predictions = self.model.predict(start=train_amt,
                                         end=train_amt+(n-1),
                                         dynamic=False)
        return list(map(int, predictions))

    def update_aggregate_data(self):
        self.history += self.prediction_market.get_latest_aggregate_consumptions()
        self.model = AR(self.history).fit()
