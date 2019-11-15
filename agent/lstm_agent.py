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
        history: past aggregate energy consumption (as a list)
    """

    NUM_HISTORIC_DATA = 144

    def __init__(self, account=ACCOUNT_0, model_file_name="./models/LSTMunivariate.h5"):
        super(LstmAgent, self).__init__(account)
        self.predictions_count = 0
        self.model = load_model(model_file_name)
        self.history = list(pd.read_pickle('./data/agg_history.pkl').aggregate_consumption)

    def predict(self, n):
        model_input = np.array(self.history[-(n+LstmAgent.NUM_HISTORIC_DATA):-NUM_PREDICTIONS])
        mean = 959.1326234         # calculated mean from training data
        std_dev = 480.45316223     # calculated std_dev from training data
        model_input = (model_input-mean)/std_dev  # normalise input data

        # batch data into format that model requires: 3D array of (?, 144, 1)
        data = []
        model_input = np.array(model_input)
        for i in range(0, n, NUM_PREDICTIONS):
            indices = range(i-LstmAgent.NUM_HISTORIC_DATA, i)
            data.append([[x] for x in model_input[indices]])

        num_batches = math.ceil(n / NUM_PREDICTIONS)
        predictions = []
        predictions_ = self.model.predict(data)
        for i in range(num_batches):
            for j in range(NUM_PREDICTIONS):
                predictions.append(predictions_[i][j] * std_dev + mean)

        self.predictions_count += n
        return list(map(int, predictions))

    def update_aggregate_data(self):
        self.history += self.prediction_market.get_latest_aggregate_consumptions()
