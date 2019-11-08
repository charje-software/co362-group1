import time
from colr import color

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
    DEFAULT_BETTING_AMOUNT = 1
    NUM_PREDICTIONS = 48
    DEFAULT_PREDICTION = 700

    # For ML agents
    # first time point to predict for relative to the first entry used for training
    START = 38237

    def __init__(self, account=ACCOUNT_1):
        self.account = account
        self.prediction_market = PredictionMarketAdapter()

    def run(self, period_length, rounds=1, logging=True):
        """
        Participate in a given number of consecutive betting rounds.

        Args:
            period_length: Length of betting period. Note that the function will
                           take (rounds + 3) * period_length seconds to run.
                           (It also waits after claiming the final reward.)
            rounds: Number of betting rounds. Default: 1
            logging: If true, the agent prints each action. Default: True
        """
        time.sleep(period_length / 5.0)  # off-set so agent doesn't clash with oracle
        has_bet = False
        waiting = False
        has_ranked = False

        def log(msg):
            if logging:
                print(color(self.account[:8], fore=self.account[2:8]) + ": " + msg)

        while rounds > 0 or has_bet or waiting or has_ranked:
            if has_ranked:
                log("Collecting reward. Won: {0}.".format(self.collect_reward()))
                has_ranked = False

            if waiting:
                log("Ranking prediction.")
                self.rank_bet()
                waiting = False
                has_ranked = True

            if has_bet:
                log("Waiting.")
                has_bet = False
                waiting = True

            if rounds > 0:
                log("Placing a bet. Prediction: {0}.".format(self.place_bet()))
                rounds -= 1
                has_bet = True

            time.sleep(period_length)

    def place_bet(self):
        predicted_consumption = self.predict(48)
        self.prediction_market.place_bet(self.account, Agent.DEFAULT_BETTING_AMOUNT,
                                         predicted_consumption)
        return predicted_consumption

    def rank_bet(self):
        self.prediction_market.rank(self.account)

    def collect_reward(self):
        return self.prediction_market.transfer_reward(self.account)

    def predict(self, n):
        return [Agent.DEFAULT_PREDICTION] * n
