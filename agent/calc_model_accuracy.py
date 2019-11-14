import requests
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from unittest import mock
import pandas as pd

from agent import Agent
from ar_agent import ArAgent
from lstm_agent import LstmAgent
from lstm_multi_agent import LstmMultiAgent
from prediction_market_adapter import NUM_PREDICTIONS


class MetricsCalculator:
    def __init__(self):
        self.actual = list(pd.read_pickle('./data/agg_future.pkl').aggregate_consumption)
        # trim to multiple of 48
        self.actual = self.actual[:-(len(self.actual) % NUM_PREDICTIONS)]

    def calc_metrics(self, agent, model_name):
        predictions = []
        with mock.patch('agent.PredictionMarketAdapter.get_latest_aggregate_consumption') \
                as mock_get_latest_aggregate_consumption:
            for i in range(len(self.actual)//48):
                # get predictions for 48 values at a time from agent
                predictions += agent.predict(NUM_PREDICTIONS)
                for j in range(48):
                    agent.update_private_data()
                    mock_get_latest_aggregate_consumption.return_value = self.actual[i * 48 + j]
                    agent.update_aggregate_data()

        # calculate MSE
        assert(len(predictions) == len(self.actual))
        mse = mean_squared_error(self.actual, predictions)

        # generate graphs
        fig = plt.figure()
        plt.plot(self.actual, label='actual')
        plt.plot(predictions, color='red', label='predicted')
        plt.title(model_name + ' MSE= ' + ('%.2f' % mse))
        plt.legend()

        fig.savefig('metrics/' + model_name.split('.')[0] + '-plot.png')


metrics_calculator = MetricsCalculator()

metrics_calculator.calc_metrics(Agent(), 'default')
metrics_calculator.calc_metrics(ArAgent(), 'ar_model')
metrics_calculator.calc_metrics(LstmAgent(), 'lstm_model')

household_2_normalise_values = [1161.5864476123875, 4.24746527e+02, 2.47782910e-01, 2.41221916e-01]
metrics_calculator.calc_metrics(LstmMultiAgent(
                                model_file_name='./models/LSTMmultivariate.h5',
                                household_name='MAC000002',
                                normalise_values=household_2_normalise_values),
                                'lstm_multi_model')

household_6_normalise_values = [9.17196847e+02, 5.31688332e+02, 5.95951121e-02, 5.35316582e-02]
metrics_calculator.calc_metrics(LstmMultiAgent(
                                model_file_name='./models/LSTMmultivariate_household6.h5',
                                household_name='MAC000006',
                                normalise_values=household_6_normalise_values),
                                'lstm_multi_model6')
