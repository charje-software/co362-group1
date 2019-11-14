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


if __name__ == "__main__":
    metrics_calculator = MetricsCalculator()

    metrics_calculator.calc_metrics(Agent(account='dummy'), 'default')
    metrics_calculator.calc_metrics(ArAgent(account='dummy'), 'ar_model')
    metrics_calculator.calc_metrics(LstmAgent(account='dummy'), 'lstm_model')

    household_2_normalise_values = [1.16123236e+03, 4.24041018e+02, 2.47572234e-01, 2.41049693e-01]
    metrics_calculator.calc_metrics(LstmMultiAgent(
                                    account='dummy',
                                    model_file_name='./models/LSTMmultivariate.h5',
                                    household_name='MAC000002',
                                    normalise_values=household_2_normalise_values),
                                    'lstm_multi_model')

    household_6_normalise_values = [9.58825287e+02, 4.79798972e+02, 5.91586789e-02, 5.25940389e-02]
    metrics_calculator.calc_metrics(LstmMultiAgent(
                                    account='dummy',
                                    model_file_name='./models/LSTMmultivariate_household_6.h5',
                                    household_name='MAC000006',
                                    normalise_values=household_6_normalise_values),
                                    'lstm_multi_model6')

    household_7_normalise_values = [1.15617658e+03, 4.22140991e+02, 1.95881843e-01, 2.31648739e-01]
    metrics_calculator.calc_metrics(LstmMultiAgent(
                                    account='dummy',
                                    model_file_name='./models/LSTMmultivariate_household_7.h5',
                                    household_name='MAC000007',
                                    normalise_values=household_7_normalise_values),
                                    'lstm_multi_model7')
