from agent import Agent
from meter import Meter

import pandas as pd


class LstmMultiAgent(Agent):
    """Agent that uses multivariate LSTM with private and public data.

    Attributes:
        model: a pretrained LSTM model
        predictions_count: counter for keeping track of the number of betting
               rounds participated in
        history: past aggregate energy consumption (as a list)
        my_history: past individual energy consumption (as a list)
        meter: Meter for fetching latest household energy consumption
    """

    def __init__(self, model_file_name, household_name,
                 account=Agent.ACCOUNT_1):
        super(LstmMultiAgent, self).__init__(account)
        self.predictions_count = 0
        # TODO: save a model and load it here
        # self.model = ...
        data_file_name = './data/household_' + household_name + '_history.pkl'
        self.my_history = list(pd.read_pickle(data_file_name).consumption)
        self.history = list(pd.read_pickle('./data/agg_history.pkl').aggregate_consumption)
        self.meter = Meter(household_name)

    def predict(self, n):
        # TODO: use model and history to make predictions
        predictions = [0] * n
        self.predictions_count += n
        return list(map(int, predictions))

    def update_aggregate_data(self):
        self.history.append(self.prediction_market.get_latest_aggregate_consumption())

    def update_private_data(self):
        self.my_history.append(self.meter.get_latest_consumption())
