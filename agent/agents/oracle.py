import requests
from colr import color
import time
from datetime import datetime
import pandas as pd
import sys

from agents.prediction_market_adapter import PredictionMarketAdapter, NUM_PREDICTIONS, ACCOUNT_0, \
                                      PERIOD_LENGTH


class Oracle:
    '''Oracle agent, responsible for feeding live values into prediction market to determine if
    agent bets are successful or not.

    Attributes:
        prediction_market: An instance of PredictionMarketAdapter used for interacting wtih the
                           PredictionMarket smart contract.

    '''

    DATA_URL = 'http://146.169.40.141/oracle.json'
    DATA_SIZE = 1488

    def __init__(self, time_index=1, logging=True):
        self.time_index = time_index
        self.prediction_market = PredictionMarketAdapter()
        self.logging = logging
        self.account = ACCOUNT_0
        if self.logging:
            print(color('Oracle : Aggregate consumption data oracle.', fore='595959'))

    def update_consumption(self):
        updated_consumption, date_time = self.query_live_data()
        self.prediction_market.update_consumption(self.account, int(updated_consumption))
        if self.logging:
            print(color('Oracle : Aggregate consumption until {0}: {1} kW.'
                  .format(pd.to_datetime(date_time).time(), updated_consumption), fore='595959'))

    def query_live_data(self):
        if self.time_index > Oracle.DATA_SIZE:
            raise ValueError('Oracle has no more data to stream for current time period!')

        oracle_data = requests.get(Oracle.DATA_URL).json()[str(self.time_index)]
        updated_consumption = oracle_data['consumption']
        datetime = oracle_data['datetime']
        self.time_index = self.time_index + 1
        return updated_consumption, datetime

    def run(self, start_time, end_time, time_delta=PERIOD_LENGTH):
        """
        Calls update_consumption every time_delta to pass the latest aggregate
        consumption data to the prediction market from start_time until end_time
        or until dataset is exhausted.

        Args:
            start_time: first data update occurs at start_time + time_delta
                        (actual time -- not timestamp of data entry)
            end_time:   date and time for last data update (actual time -- not
                        timestamp of data entry)
            time_delta: how long to wait between data updates.
        """
        now = datetime.now()
        if now < start_time:
            time.sleep((start_time - now).seconds)
        elif start_time < now:
            raise ValueError('Start time cannot be in the past!')

        next_time = start_time + time_delta
        while now <= end_time:
            now = datetime.now()
            time.sleep((next_time - now).seconds)
            next_time += time_delta
            try:
                self.update_consumption()
            except ValueError:
                break  # no more data to fetch


if __name__ == "__main__":
    oracle = Oracle()
    if len(sys.argv) == 3:
        oracle.run(start_time=pd.to_datetime(sys.argv[1]),
                   end_time=pd.to_datetime(sys.argv[2]))
    elif len(sys.argv) == 4:
        oracle.run(start_time=pd.to_datetime(sys.argv[1]),
                   end_time=pd.to_datetime(sys.argv[2]),
                   time_delta=pd.Timedelta(sys.argv[3]))
