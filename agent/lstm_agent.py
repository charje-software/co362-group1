from agent import Agent


class LstmAgent(Agent):
    """Agent that uses LSTM with public data only.

    Attributes:
        model: a pretrained LSTM model used for predicting
               future aggregate energy consumption.
        predictions_count: counter for keeping track of the number of betting
               rounds participated in.
        history: past aggregate energy consumption
    """

    def __init__(self, account=Agent.ACCOUNT_1, model_file_name="lstm_model.pkl",
                 data_file_name="historic_aggregate_demand.pkl"):
        super(ArAgent, self).__init__(account)
        self.predictions_count = 0
        # TODO: save a model and load it here
        # self.model = ...
        # TODO: save data set and load it here
        # self.history = ...

    def predict(self, n):
        # TODO: use model and history to make predictions
        predictions = [0] * n
        self.predictions_count += n
        return list(map(int, predictions))

    def update_aggregate_data(self):
        # TODO: add the returned data to the history
        self.prediction_market_adapter.get_latest_aggregate_consumption()
