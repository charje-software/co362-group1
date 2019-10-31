import requests
import time

from prediction_market_adapter import PredictionMarketAdapter


class Oracle:
    """Oracle agent, responsible for feeding live values into prediction market to determine if
    agent bets are successful or not.

    Attributes:
        prediction_market: An instance of PredictionMarketAdapter used for interacting wtih the
                           PredictionMarket smart contract.

    """

    ACCOUNT = '0x98ccdc5F73bb4F7f97B480920B40A52Fa9dAD663'
    DATA_URL = 'http://146.169.40.141/oracle.json'
    DATA_SIZE = 1489

    def __init__(self, time_index=1, logging=True):
        self.time_index = time_index
        self.prediction_market = PredictionMarketAdapter()
        self.logging = logging

    def run(self, period_length, rounds=1, logging=True):
        """
        Participate in a given number of consecutive betting rounds.

        Args:
            period_length: Length of betting period. Note that the function will
                           take (rounds + 3) * period_length seconds to run.
                           (It also waits after claiming the final reward.)
            rounds: Number of betting rounds. Default: 1
            logging: If true, oracle prints updated consumption each time period. Default: True
        """

        rounds += 3  # Update consumption for 3 extra betting rounds so agents can collect rewards
        assert Oracle.DATA_SIZE - self.time_index - rounds + 1 >= 0  # Check enough data to stream

        self.logging = logging

        while rounds > 0:
            time.sleep(period_length)
            self.update_consumption()
            rounds -= 1

    def update_consumption(self):
        updated_consumption = self.query_live_data()
        self.prediction_market.update_consumption(Oracle.ACCOUNT, int(updated_consumption))
        if self.logging:
            print("Oracle consumption data from previous period: " + updated_consumption + "kW.")

    def query_live_data(self):
        if self.time_index > Oracle.DATA_SIZE:
            raise ValueError("Oracle has no more data to stream for current time period!")
        oracle_data = requests.get(Oracle.DATA_URL).json()[str(self.time_index)]
        updated_consumption = oracle_data['consumption']
        self.time_index = self.time_index + 1
        return updated_consumption
