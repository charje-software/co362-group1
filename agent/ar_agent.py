from statsmodels.tsa.ar_model import ARResults

from agent import Agent
from prediction_market_adapter import ACCOUNT_0, NUM_PREDICTIONS


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

    def predict_for_tomorrow(self):
        # need to predict all starting from START, but only return last NUM_PREDICTIONS
        predictions = self.model.predict(start=ArAgent.START,
                                         end=ArAgent.START+self.predictions_count+NUM_PREDICTIONS,
                                         dynamic=False)[-NUM_PREDICTIONS:]
        self.predictions_count += NUM_PREDICTIONS
        return list(map(int, predictions))
