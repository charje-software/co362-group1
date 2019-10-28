from prediction_market_adapter import PredictionMarketAdapter
import requests

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

    def __init__(self, time_index=1):
        self.time_index = time_index
        self.prediction_market = PredictionMarketAdapter()

    def update_consumption(self):
        updated_consumption = self.query_live_data()
        self.prediction_market.update_consumption(Oracle.ACCOUNT, int(updated_consumption))

    def query_live_data(self):
        if self.time_index > Oracle.DATA_SIZE:
            raise Exception("Oracle has run out of data to stream!")
        updated_consumption = requests.get(Oracle.DATA_URL).json()[str(self.time_index)]['consumption']
        self.time_index = self.time_index + 1
        return updated_consumption
