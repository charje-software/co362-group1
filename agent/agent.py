from colr import color

from prediction_market_adapter import PredictionMarketAdapter, NUM_PREDICTIONS, ACCOUNT_0


class Agent:
    """Simple agent representing one household.

    Note that the agent assumes that place_bet, rank_bet, collect_reward are called only
    once in each period when allowed.

    Attributes:
        account:           The agent's account on the blockchain.
        prediction_market: An instance of PredictionMarketAdapter used for interacting with the
                           PredictionMarket smart contract.
        has_bet:           List of booleans indicating whether or not the agent bet the last time
                           place_bet was called.
    """

    DEFAULT_BETTING_AMOUNT = 1
    DEFAULT_PREDICTION = 700

    def __init__(self, account=ACCOUNT_0, logging=True):
        self.account = account
        self.prediction_market = PredictionMarketAdapter()
        self.logging = logging
        self.has_bet = [False, False, False, False]

    def log(self, msg):
        if self.logging:
            print(color(self.account[:8], fore=self.account[2:8]) + ": " + msg)

    def place_bet(self):
        predicted_consumptions = self.predict(NUM_PREDICTIONS)
        if predicted_consumptions is None:
            self.log('Will not bet during current betting round.')
            self.has_bet += [False]
            return

        self.prediction_market.place_bet(self.account, Agent.DEFAULT_BETTING_AMOUNT,
                                         predicted_consumptions)
        self.log('Placing a bet. Predictions: {0}.'.format(predicted_consumptions))
        self.has_bet += [True]

    def rank_bet(self):
        if self.has_bet[-3]:
            self.log('Ranking previous predictions.')
            self.prediction_market.rank(self.account)

    def collect_reward(self):
        if self.has_bet[-3]:
            self.prediction_market.transfer_reward(self.account)
            self.log('Collecting reward. Won?: {0}.'
                     .format(self.prediction_market.get_winning_tier(self.account)))

    def predict(self, n):
        """
        Predict the aggregate energy consumption for the next n timestamps.
        Subclasses of Agent should override this to use their predictions algorithm.
        Should return None if no predictions possible or the agent doesn't want to bet.
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
