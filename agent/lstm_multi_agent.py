import pandas as pd
import numpy as np
import math

from tensorflow.keras.models import load_model

from agent import Agent
from meter import Meter
from prediction_market_adapter import NUM_PREDICTIONS, ACCOUNT_0


class LstmMultiAgent(Agent):
    """Agent that uses multivariate LSTM with private and public data.

    Attributes:
        model: a pretrained LSTM model
        predictions_count: counter for keeping track of the number of betting
               rounds participated in
        my_history: past individual energy consumption (as a list)
        meter: Meter for fetching latest household energy consumption
    """

    NUM_HISTORIC_DATA = 144

    def __init__(self, model_file_name, household_name, normalise_values,
                 account=ACCOUNT_0, logging=True):
        super(LstmMultiAgent, self).__init__(account, logging)
        self.predictions_count = 0
        self.model = load_model(model_file_name)
        data_file_name = './data/household_' + household_name + '_history.pkl'
        self.my_history = list(pd.read_pickle(data_file_name).consumption)
        self.meter = Meter(household_name)
        self.agg_mean = normalise_values[0]
        self.agg_std_dev = normalise_values[1]
        self.mean = normalise_values[2]
        self.std_dev = normalise_values[3]
        self.num_history_added = 0
        self.log('LstmMultiAgent for household {0}'.format(household_name))

    def predict_for_tomorrow(self):
        agg_history = np.array(self.aggregate_history[
                    -(NUM_PREDICTIONS+LstmMultiAgent.NUM_HISTORIC_DATA):-NUM_PREDICTIONS])
        agg_history = (agg_history-self.agg_mean)/self.agg_std_dev  # normalise input data

        history = np.array(self.my_history[
                    -(NUM_PREDICTIONS+LstmMultiAgent.NUM_HISTORIC_DATA):-NUM_PREDICTIONS])
        history = (history-self.mean)/self.std_dev

        # batch data into format that model requires: 3D array of (?, 144, 2)
        agg_history = np.array(agg_history)
        my_history = np.array(history)
        # offset to make sure that you take an exact 3 days starting from start of day
        offset = self.num_history_added % NUM_PREDICTIONS
        indices = range(0-LstmMultiAgent.NUM_HISTORIC_DATA-offset, 0-offset)
        tuple = []
        for j in range(len(agg_history[indices])):
            tuple.append([agg_history[indices][j], history[indices][j]])
        data = [tuple]

        predictions = []
        predictions_ = self.model.predict(data)
        for j in range(NUM_PREDICTIONS):
            predictions.append(predictions_[0][j] * self.agg_std_dev + self.agg_mean)

        self.predictions_count += NUM_PREDICTIONS
        return list(map(int, predictions))

    def update_per_period(self):
        self.my_history.append(self.meter.get_latest_consumption())
        self.num_history_added += 1
