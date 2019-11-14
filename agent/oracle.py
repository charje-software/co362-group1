import requests
import time

from prediction_market_adapter import PredictionMarketAdapter, NUM_PREDICTIONS


class Oracle:
    '''Oracle agent, responsible for feeding live values into prediction market to determine if
    agent bets are successful or not.

    Attributes:
        prediction_market: An instance of PredictionMarketAdapter used for interacting wtih the
                           PredictionMarket smart contract.

    '''

    ACCOUNT = '0xd8CA13a2b3FB03873Ce14d2D04921a7D8552c28F'
    DATA_URL = 'http://146.169.40.141/oracle.json'
    DATA_SIZE = 1488

    def __init__(self, time_index=1, logging=True):
        self.time_index = time_index
        self.prediction_market = PredictionMarketAdapter()
        self.logging = logging

    def update_consumption(self):
        updated_consumption, datetime = self.query_live_data()
        self.prediction_market.update_consumption(Oracle.ACCOUNT, int(updated_consumption))
        if self.logging:
            print('Oracle  : consumption for period ending ({0}): {1} kW.'
                  .format(datetime, updated_consumption))

    def query_live_data(self):
        if self.time_index > Oracle.DATA_SIZE:
            raise ValueError('Oracle has no more data to stream for current time period!')

        oracle_data = requests.get(Oracle.DATA_URL).json()[str(self.time_index)]
        updated_consumption = oracle_data['consumption']
        datetime = oracle_data['datetime']
        self.time_index = self.time_index + 1
        return updated_consumption, datetime
