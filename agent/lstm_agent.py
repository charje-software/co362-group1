import pandas as pd
import numpy as np
import math

from tensorflow.keras.models import load_model

from agent import Agent
from prediction_market_adapter import NUM_PREDICTIONS, ACCOUNT_0


class LstmAgent(Agent):
    """Agent that uses LSTM with public data only.

    Attributes:
        model: a pretrained LSTM model used for predicting
               future aggregate energy consumption.
        predictions_count: counter for keeping track of the number of betting
               rounds participated in.
    """

    NUM_HISTORIC_DATA = 144

    def __init__(self, account=ACCOUNT_0, model_file_name="./models/LSTMunivariate.h5",
                 logging=True):
        super(LstmAgent, self).__init__(account, logging)
        self.predictions_count = 0
        self.model = load_model(model_file_name)
        self.log('LstmAgent')

    def predict_for_tomorrow(self):
        model_input = np.array(self.aggregate_history[
                    -(NUM_PREDICTIONS+LstmAgent.NUM_HISTORIC_DATA):-NUM_PREDICTIONS])
        mean = 959.1326234         # calculated mean from training data
        std_dev = 480.45316223     # calculated std_dev from training data
        model_input = (model_input-mean)/std_dev  # normalise input data

        # batch data into format that model requires: 3D array of (?, 144, 1)
        model_input = np.array(model_input)
        indices = range(0-LstmAgent.NUM_HISTORIC_DATA, 0)
        data = [[[x] for x in model_input[indices]]]

        predictions = []
        predictions_ = self.model.predict(data)
        for j in range(NUM_PREDICTIONS):
            predictions.append(predictions_[0][j] * std_dev + mean)

        self.predictions_count += NUM_PREDICTIONS
        return list(map(int, predictions))
