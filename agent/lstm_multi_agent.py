import pandas as pd
import numpy as np
import math

from tensorflow.keras.models import load_model

from agent import Agent
from meter import Meter
from prediction_market_adapter import NUM_PREDICTIONS


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

    NUM_HISTORIC_DATA = 144

    def __init__(self, model_file_name, household_name,
                 account=Agent.ACCOUNT_1):
        super(LstmMultiAgent, self).__init__(account)
        self.predictions_count = 0
        self.model = load_model(model_file_name)
        data_file_name = './data/household_' + household_name + '_history.pkl'
        self.my_history = list(pd.read_pickle(data_file_name).consumption)
        self.history = list(pd.read_pickle('./data/agg_history.pkl').aggregate_consumption)
        self.meter = Meter(household_name)

    def predict(self, n):
        agg_history = np.array(self.history[-(n+LstmMultiAgent.NUM_HISTORIC_DATA):-NUM_PREDICTIONS])
        agg_mean = 1161.5864476123875  # calculated mean from training data
        agg_std_dev = 4.24746527e+02   # calculated std_dev from training data
        agg_history = (agg_history-agg_mean)/agg_std_dev  # normalise input data

        history = np.array(self.my_history[-(n+LstmMultiAgent.NUM_HISTORIC_DATA):-NUM_PREDICTIONS])
        mean = 2.47782910e-01
        std_dev = 2.41221916e-01
        history = (history-mean)/std_dev

        # batch data into format that model requires: 3D array of (?, 144, 2)
        data = []
        agg_history = np.array(agg_history)
        my_history = np.array(history)
        for i in range(0, n, NUM_PREDICTIONS):
            indices = range(i-LstmMultiAgent.NUM_HISTORIC_DATA, i)
            tuple = []
            for j in range(len(agg_history[indices])):
                tuple.append([agg_history[indices][j], history[indices][j]])
            data.append(tuple)

        num_batches = math.ceil(n / NUM_PREDICTIONS)
        predictions = []
        predictions_ = self.model.predict(data)
        for i in range(num_batches):
            for j in range(NUM_PREDICTIONS):
                predictions.append(predictions_[i][j] * agg_std_dev + agg_mean)

        self.predictions_count += n
        return list(map(int, predictions))

    def update_aggregate_data(self):
        self.history.append(self.prediction_market.get_latest_aggregate_consumption())

    def update_private_data(self):
        self.my_history.append(self.meter.get_latest_consumption())
