import pandas as pd
import numpy as np
import math
import pickle

from agents.agent import Agent
from agents.prediction_market_adapter import NUM_PREDICTIONS, ACCOUNT_0, PERIOD_LENGTH


class RfAgent(Agent):
    """Agent that uses LSTM with public data only.

    Attributes:
        model: a pretrained LSTM model used for predicting
               future aggregate energy consumption.
        predictions_count: counter for keeping track of the number of betting
               rounds participated in.
    """

    NUM_HISTORIC_DATA = 336

    def __init__(self, account=ACCOUNT_0, model_file_name="./models/rf.mdl",
                 logging=True, **kwargs):
        super(RfAgent, self).__init__(account, logging, **kwargs)
        self.predictions_count = 0
        self.model = pickle.load(open(model_file_name, 'rb'))
        self.datetime = pd.to_datetime('2014-01-28 00:00:00')
        # self.features, self.num_features, self.cat_features = self.engineer_features(agg_demand)
        self.log('RfAgent')

    def predict_for_tomorrow(self):
        model_input = self.generate_input()

        mean = 1162.57834632     # calculated mean from training data
        std_dev = 422.36255133   # calculated std_dev from training data
        predictions = []
        for j in range(NUM_PREDICTIONS):
            prediction = self.model[j].predict(model_input)
            predictions.append(prediction * std_dev + mean)

        return list(map(int, predictions))

    def update_daily(self):
        super(RfAgent, self).update_daily()
        self.datetime += pd.Timedelta('1days')

    def generate_input(self):
        consumption = np.array(self.aggregate_history[-RfAgent.NUM_HISTORIC_DATA:])
        date_time = pd.date_range(start=self.datetime - RfAgent.NUM_HISTORIC_DATA * PERIOD_LENGTH,
                                  end=self.datetime, freq='30min')
        model_input = pd.DataFrame(zip(date_time, consumption),
                                   columns=['datetime', 'aggregate_consumption'])
        model_input.datetime = pd.to_datetime(model_input.datetime)
        model_input['day_of_year'] = model_input['datetime'].apply(lambda x: x.dayofyear)
        model_input['day_of_month'] = model_input['datetime'].apply(lambda x: x.day)
        model_input['day_of_week'] = model_input['datetime'].apply(lambda x: x.dayofweek)
        model_input.index = model_input.datetime
        model_input = model_input.drop(columns=['datetime'])

        # scale input according to training data standardization
        means = {'day_of_year': 188.0585337, 'day_of_month': 15.90230575,
                 'aggregate_consumption': 1162.57834632}
        std_devs = {'day_of_year': 118.85431568, 'day_of_month': 8.74171958,
                    'aggregate_consumption': 422.36255133}
        for key in means.keys():
            model_input[key] = model_input[key].apply(lambda x: (x-means[key])/std_devs[key])

        return np.array([np.array(model_input).flatten()])
