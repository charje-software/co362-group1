import time
from colr import color

from prediction_market_adapter import PredictionMarketAdapter, NUM_PREDICTIONS


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
    DEFAULT_PREDICTION = 700

    def __init__(self, account=ACCOUNT_1):
        self.account = account
        self.prediction_market = PredictionMarketAdapter()

    def run(self, period_length, rounds=1, logging=True):
        """
        Participate in a given number of consecutive betting rounds.

        Args:
            period_length: in seconds, duration of the 30min intervals
                over which consumption is measured and predicted for.
                This function will run for
                (rounds + 2) * NUM_PREDICTIONS * period_length seconds
            rounds: Number of betting rounds. One round needs predictions
                for NUM_PREDICTIONS periods Default: 1
            logging: If true, the agent prints each action. Default: True
        """
        time.sleep(period_length / 5.0)  # off-set so agent doesn't clash with oracle

        def log(msg):
            if logging:
                print(color(self.account[:8], fore=self.account[2:8]) + ": " + msg)

        def half_round():
            for period in range(NUM_PREDICTIONS // 2):
                self.update_private_data()
                self.update_aggregate_data()
                time.sleep(period_length)

        for round in range(rounds + 2):
            if round < rounds:
                log("Placing a bet. Predictions: {0}.".format(self.place_bet()))

            if (round > 1):
                log("Ranking previous predictions.")
                self.rank_bet()

            half_round()

            if (round > 1):
                log("Collecting reward. Won: {0}.".format(self.collect_reward()))

            half_round()

    def place_bet(self):
        predicted_consumptions = self.predict(NUM_PREDICTIONS)
        self.prediction_market.place_bet(self.account, Agent.DEFAULT_BETTING_AMOUNT,
                                         predicted_consumptions)
        return predicted_consumptions

    def rank_bet(self):
        self.prediction_market.rank(self.account)

    def collect_reward(self):
        return self.prediction_market.transfer_reward(self.account)

    def predict(self, n):
        """
        Predict the aggregate energy consumption for the next n timestamps.
        Subclasses of Agent should override this to use their predictions algorithm.
        """
        return [Agent.DEFAULT_PREDICTION] * n

    def update_private_data(self):
        """
        Called once every time period when running the agent.
        Subclasses of Agent can override this to update their stored history
        of private data.
        """
        pass

    def update_aggregate_data(self):
        """
        Called once every time period when running the agent.
        Subclasses of Agent can override this to update their stored history
        of aggregate data.
        """
        pass
