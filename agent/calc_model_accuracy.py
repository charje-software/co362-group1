import requests
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

from agent import Agent
from ar_agent import ArAgent


class MetricsCalculator:

    DATA_URL = 'http://146.169.40.141/oracle.json'
    DATA_SIZE = 1489

    def __init__(self):
        # get aggregate consumption values from oracle
        oracle_data = requests.get(self.DATA_URL).json()
        self.actual = []
        for key, value in oracle_data.items():
            self.actual.append(int(value['consumption']))

    def calc_metrics(self, agent, model_name):
        # get predictions for last 1489 values from agent
        predictions = agent.predict(self.DATA_SIZE)

        # calculate MSE
        assert(len(predictions) == len(self.actual))
        mse = mean_squared_error(self.actual, predictions)

        # generate graphs
        fig = plt.figure()
        plt.plot(self.actual, label='actual')
        plt.plot(predictions, color='red', label='predicted')
        plt.title(model_name + ' MSE= ' + ("%.2f" % mse))
        plt.legend()

        fig.savefig('metrics/' + model_name.split('.')[0] + '-plot.png')


metrics_calculator = MetricsCalculator()

metrics_calculator.calc_metrics(Agent(), "default")
metrics_calculator.calc_metrics(ArAgent(), "armodel")
