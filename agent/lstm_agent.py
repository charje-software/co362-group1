from agent import Agent

import pandas as pd


class LstmAgent(Agent):
    """Agent that uses LSTM with public data only.

    Attributes:
        model: a pretrained LSTM model used for predicting
               future aggregate energy consumption.
        predictions_count: counter for keeping track of the number of betting
               rounds participated in.
        history: past aggregate energy consumption (as a list)
    """

    def __init__(self, account=Agent.ACCOUNT_1, model_file_name="lstm_model.pkl"):
        super(LstmAgent, self).__init__(account)
        self.predictions_count = 0
        # TODO: save a model and load it here
        # self.model = ...
        self.history = list(pd.read_pickle('./data/agg_history.pkl').aggregate_consumption)

    def predict(self, n):
        # TODO: use model and history to make predictions
        predictions = [0] * n
        self.predictions_count += n
        return list(map(int, predictions))

    def update_aggregate_data(self):
        self.history.append(self.prediction_market_adapter.get_latest_aggregate_consumption())
