import pandas as pd


class Meter:
    """Meter for one household for providing latest energy consumption.

    Attributes:
        data:  The agents individual energy consumption for half-hourly periods.
        self.
        timestamp: Date and time for latest completed period.
    """
    def __init__(self, agent_account=Agent.ACCOUNT_1):
        # TODO: uses a mapping from agent_account to data_file_name to
        # import this agents individual data
        # I don't want the data_file to be an input, as the Agent doesn't need to
        # know that the Meter just pretends to use a real meter but actually has the
        # whole future stored in a data set.
        # self.data = ...
        self.timestamp = pd.to_datetime('2014-02-28 00:00:00')

    def get_latest_consumption(self):
        """
        Returns the household's consumption during the last completed period.
        """
        # TODO: implement
        return 0
