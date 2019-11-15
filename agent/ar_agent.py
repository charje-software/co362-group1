from statsmodels.tsa.ar_model import ARResults

from agent import Agent
from prediction_market_adapter import ACCOUNT_0


class ArAgent(Agent):
    """Agent that uses autoregression with public data only.

    Attributes:
        model: a pretrained autoregression model used for predicting
               future aggregate energy consumption.
        predictions_count: counter for keeping track of the number of betting
               rounds participated in.
    """

    START = 38237  # first time point to predict for relative to the first entry used for training

    def __init__(self, account=ACCOUNT_0, model_file_name="./models/armodel.pkl"):
        super(ArAgent, self).__init__(account)
        self.predictions_count = 0
        self.model = ARResults.load(model_file_name)

    def predict(self, n):
        # need to predict all starting from START, but only return last n
        predictions = self.model.predict(start=ArAgent.START,
                                         end=ArAgent.START+self.predictions_count+(n),
                                         dynamic=False)
        self.predictions_count += n
        return list(map(int, predictions[-n:]))
