from colr import color
import pandas as pd
from sklearn.metrics import mean_absolute_error

from agents.prediction_market_adapter import PredictionMarketAdapter, NUM_PREDICTIONS, ACCOUNT_0, \
                                      MID_TIER_THRESHOLD, TOP_TIER_THRESHOLD


class Agent:
    """Simple agent representing one household.

    The Agent base class outlines core interaction between the agent and the prediction
    market. It should NOT be used for betting as it is, as it simply uses a constant
    default prediction. Subclasses should override place_bet's helper predict_for_tomorrow
    and other methods as necessary.

    Agent assumes that place_bet, rank_bet, collect_reward, update_per_period, update_daily
    are called every day with the following frequencies and order by any script that
    runs the Agent:

    1.  update_aggregate_data() at the start of every day
    2.  update_private_data() every 30 min period
    3.  place_bet() every day between 00:00 and 12:00
    4.  rank_bet() every day between 00:00 and 12:00
    5.  collect_reward() every day between 12:00 and 00:00

    So these 5 methods are opportunities for the agent to do something (update its stored
    data/models, interact with data sources or the prediciton market, etc.)
    but depending on the strategies implemented by the subclass, it might e.g choose note
    to place a bet.

    Attributes:
        account:            The agent's account on the blockchain.
        logging:            If true, the agent prints info about its actions to std out.
        prediction_market:  An instance of PredictionMarketAdapter used for interacting with the
                            PredictionMarket smart contract.
        prediction_history: List containing past predictions (most recent last).
        aggregate_history:  List of aggregate consumption data (most recent last).
    """

    DEFAULT_BETTING_AMOUNT = 1
    DEFAULT_PREDICTION = 700

    def __init__(self, account=ACCOUNT_0, logging=True, **kwargs):
        self.account = account
        self.logging = logging
        self.prediction_market = PredictionMarketAdapter()
        self.prediction_history = [None, None]  # No predictions yesterday or the day before
        self.aggregate_history = list(pd.read_pickle('./data/agg_history.pkl')
                                      .aggregate_consumption)
        self.color = self.account[2:8] if kwargs.get('color') is None else kwargs.get('color')
        self.name = self.account[:8] if kwargs.get('name') is None else kwargs.get('name')

    def log(self, msg):
        if self.logging:
            print(color(self.name + ": " + msg, fore=self.color))

    def place_bet(self):
        """
        Places a bet on behalf of the Agent if the agent wants to bet.
        """
        predicted_consumptions = self.predict_for_tomorrow()

        if predicted_consumptions is None:
            self.log('Will not bet during current betting round.')
        else:
            self.prediction_market.place_bet(self.account, Agent.DEFAULT_BETTING_AMOUNT,
                                             predicted_consumptions)
            self.log('Placing a bet. Predictions: {0}.'.format(predicted_consumptions))

        self.prediction_history.append(predicted_consumptions)

    def rank_bet(self):
        """
        If the agent placed a bet the day before yesterday and its predictions will
        rank on a winning tier, rank the agents bet in the prediction market.
        """
        if self.prediction_history[-3] is not None:
            mae = mean_absolute_error(self.aggregate_history[-NUM_PREDICTIONS:],
                                      self.prediction_history[-3])

            if mae < MID_TIER_THRESHOLD:
                tier = 'top' if mae < TOP_TIER_THRESHOLD else 'mid'
                self.log('Ranking previous predictions. Expecting {1} tier (MAE = {0:.2f}).'
                         .format(mae, tier))
                self.prediction_market.rank(self.account)
            else:
                self.log('No need to ask for ranking.   Expecting to lose  (MAE = {0:.2f}).'
                         .format(mae))

    def collect_reward(self):
        """
        If the agent ranked a bet today and it ranked on a winning tier,
        collect the agent's reward from the prediction market.
        """
        if self.prediction_history[-3] is not None:
            try:
                tier = self.prediction_market.get_winning_tier(self.account)
            except ValueError:
                tier = 'lost'

            if tier is not 'lost':
                self.prediction_market.transfer_reward(self.account)
                self.log('Collecting reward. Won?: {0}.'.format(tier))

    def predict_for_tomorrow(self):
        """
        Subclasses of Agent should override this to use their prediction algorithm.

        Returns: A list of NUM_PREDICTIONS integers corresponding to predicted aggregate
                 energy consumption for tomorrow.
                 None if the Agent chooses not to bet.
        """
        return [Agent.DEFAULT_PREDICTION] * NUM_PREDICTIONS

    def update_per_period(self):
        """
        Called once every time period when running the agent.
        Subclasses of Agent can override this to e.g. update their stored history
        of private data.
        """
        pass

    def update_daily(self):
        """
        Called once every day when running the agent.
        Updates aggregate_history.
        """
        self.aggregate_history += self.prediction_market.get_latest_aggregate_consumptions()
