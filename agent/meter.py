import pandas as pd


class Meter:
    """Meter for one household for providing latest energy consumption.

    Attributes:
        data:  The agents individual energy consumption for half-hourly periods.
        self.
        timestamp: Date and time for latest completed period.
    """
    def __init__(self, household_name):
        self.timestamp = pd.to_datetime('2014-01-28 00:30:00')
        data_file_name = './data/household_' + household_name + '_future.pkl'
        self.data = pd.read_pickle(data_file_name)

    def get_latest_consumption(self):
        """
        Returns the household's consumption during the last completed period.

        Note that you should only call this once per 30min period, as this is
        just a pretend meter that uses the calls to track time.
        """
        assert self.timestamp <= pd.to_datetime('2014-02-28 00:00:00')

        consumption = self.data.loc[self.timestamp, 'consumption']
        self.timestamp += pd.Timedelta('30min')

        return consumption
