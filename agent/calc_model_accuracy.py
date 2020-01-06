from unittest import mock

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error

from agents.agent import Agent
from agents.ar_agent import ArAgent
from agents.ar_retrain_agent import ArRetrainAgent
from agents.ar_retrain_decision_agent import ArRetrainDecisionAgent
from agents.lstm_agent import LstmAgent
from agents.lstm_multi_agent import LstmMultiAgent
from agents.rf_agent import RfAgent
from agents.prediction_market_adapter import NUM_PREDICTIONS


class MetricsCalculator:
    def __init__(self):
        # discard first day as the first prediction period is the day after
        self.actual = list(pd.read_pickle('./data/agg_future.pkl')
                           .aggregate_consumption)[NUM_PREDICTIONS:]

    def calc_metrics(self, agent, model_name):
        predictions = []
        skipped = False
        with mock.patch('agents.agent.PredictionMarketAdapter.get_latest_aggregate_consumptions') \
                as mock_get_latest_aggregate_consumptions:
            for i in range(len(self.actual) // 48):
                # get predictions for 48 values at a time from agent
                preds = agent.predict_for_tomorrow()
                if preds is not None:
                    predictions += preds
                else:
                    predictions += [-1] * NUM_PREDICTIONS
                    skipped = True

                for j in range(48):
                    agent.update_per_period()

                mock_get_latest_aggregate_consumptions.return_value = \
                    self.actual[i * 48: (i + 1) * 48]
                agent.update_daily()

        assert (len(predictions) == len(self.actual))

        # generate graphs
        fig = plt.figure()
        plt.plot(self.actual, label='actual')
        plt.plot(predictions, color='red', label='predicted')

        # calculate MSE
        if not skipped:
            mse = mean_squared_error(self.actual, predictions)
            plt.title(model_name + ' MSE= ' + ('%.2f' % mse))
        else:
            plt.title(model_name + ' (MSE not calculated)')

        plt.legend()
        fig.savefig('metrics/' + model_name.split('.')[0] + '-plot.png')


if __name__ == "__main__":
    metrics_calculator = MetricsCalculator()

    metrics_calculator.calc_metrics(Agent(account='dummy', logging=False), 'default')
    metrics_calculator.calc_metrics(ArAgent(account='dummy', logging=False), 'ar_model')
    metrics_calculator.calc_metrics(ArRetrainAgent(account='dummy', logging=False),
                                    'ar_retrain_model')
    metrics_calculator.calc_metrics(ArRetrainDecisionAgent(account='dummy', logging=False),
                                    'ar_retrain_decision_model')
    metrics_calculator.calc_metrics(LstmAgent(account='dummy', logging=False), 'lstm_model')

    household_2_normalise_values = [1.16123236e+03, 4.24041018e+02, 2.47572234e-01, 2.41049693e-01]
    metrics_calculator.calc_metrics(LstmMultiAgent(
        account='dummy',
        model_file_name='./models/LSTMmultivariate.h5',
        household_name='MAC000002',
        normalise_values=household_2_normalise_values, logging=False),
        'lstm_multi_model')

    household_6_normalise_values = [9.58825287e+02, 4.79798972e+02, 5.91586789e-02, 5.25940389e-02]
    metrics_calculator.calc_metrics(LstmMultiAgent(
        account='dummy',
        model_file_name='./models/LSTMmultivariate_household_6.h5',
        household_name='MAC000006',
        normalise_values=household_6_normalise_values, logging=False),
        'lstm_multi_model6')

    household_7_normalise_values = [1.15617658e+03, 4.22140991e+02, 1.95881843e-01, 2.31648739e-01]
    metrics_calculator.calc_metrics(LstmMultiAgent(
        account='dummy',
        model_file_name='./models/LSTMmultivariate_household_7.h5',
        household_name='MAC000007',
        normalise_values=household_7_normalise_values, logging=False),
        'lstm_multi_model7')
    metrics_calculator.calc_metrics(RfAgent(account='dummy', logging=False), 'random_forest')
