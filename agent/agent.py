from prediction_market_adapter import PredictionMarketAdapter


class Agent:
    """Simple agent representing one household.

    Attributes:
        account:           The agent's account on the blockchain.
        prediction_market: An instance of PredictionMarketAdapter used for interacting with the
                           PredictionMarket smart contract.
    """

    # For manual testing. Needs to match address of an account on ganache.
    ACCOUNT_1 = '0x9F122516DcB6C39A6E77A27D3631d69478aa9f24'
    DEFAULT_BETTING_AMOUNT = 10

    def __init__(self, account=ACCOUNT_1):
        self.account = account
        self.prediction_market = PredictionMarketAdapter()

    def place_bet(self):
        self.prediction_market.place_bet(self.account, Agent.DEFAULT_BETTING_AMOUNT)

    def collect_reward(self):
        self.prediction_market.transfer_reward(self.account)
