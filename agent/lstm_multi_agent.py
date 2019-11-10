from agent import Agent
from meter import Meter


class LstmMultiAgent(Agent):
    """Agent that uses multivariate LSTM with private and public data.

    Attributes:
        model: a pretrained LSTM model
        predictions_count: counter for keeping track of the number of betting
               rounds participated in
        history: past aggregate energy consumption
        meter: Meter for fetching latest household energy consumption
    """

    def __init__(self, model_file_name, data_file_name, account=Agent.ACCOUNT_1):
        super(ArAgent, self).__init__(account)
        self.predictions_count = 0
        # TODO: save a model and load it here
        # self.model = ...
        # TODO: save data set and load it here
        # self.history = ...
        self.meter = Meter(agent_account=self.account)

    def predict(self, n):
        # TODO: use model and history to make predictions
        predictions = [0] * n
        self.predictions_count += n
        return list(map(int, predictions))

    def update_aggregate_data(self):
        # TODO: add the returned data to the history
        self.prediction_market_adapter.get_latest_aggregate_consumption()

    def update_private_data(self):
        # TODO: add the returned data to the history
        self.meter.get_latest_aggregate_consumption()
