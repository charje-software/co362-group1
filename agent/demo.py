import time
import pandas as pd

from ar_agent import ArAgent
from oracle import Oracle
from agent import Agent
from lstm_agent import LstmAgent
from lstm_multi_agent import LstmMultiAgent

START = pd.to_datetime('2014-01-28 00:00:00')
END = pd.to_datetime('2014-02-01 23:30:00')
# END = pd.to_datetime('2014-02-27 23:30:00')
PERIOD_LENGTH = 0.002

ACCOUNTS = ['0xEA43d7cE5224683B1D83D19327699756504fB489',
            '0x4B516E6c8c3a5Ea97Ff7377d81Ea2238C46C5882',
            '0x768848539fc4AA09435797773456d114ea83bcE1',
            '0xfcC640fB2629943aaaA35c4D0A79000e0bfc8870',
            '0x80Fb53cb93F0e23b7698E6475498d3395806B2c9',
            '0x30717eD75d2c188eB01bCB8733C291B6348B6F5B',
            '0x844A203E1D962E61505f6ef17abBF432f3F680d5',
            '0x3FFA1EA78d44488c43DE84B6D03C3b6C0DC7248E',
            '0x0A058293Feb18aedbca8c2169947381d2e71F424']

agent1 = ArAgent(ACCOUNTS[1])
agent2 = LstmAgent(ACCOUNTS[2])
household_2_normalise_values = [1.16123236e+03, 4.24041018e+02, 2.47572234e-01, 2.41049693e-01]
agent3 = LstmMultiAgent(
                account=ACCOUNTS[3],
                model_file_name='./models/LSTMmultivariate.h5',
                household_name='MAC000002',
                normalise_values=household_2_normalise_values)
oracle = Oracle()


def is_betting_time(date_time):
    return date_time.minute == 0 and date_time.hour == 0 \
           and date_time <= END - pd.Timedelta('2 days')


def is_ranking_time(date_time):
    return date_time.minute == 0 and date_time.hour == 0 \
           and date_time >= START + pd.Timedelta('2 days')


def is_collecting_time(date_time):
    return date_time.minute == 0 and date_time.hour == 12 \
           and date_time > START + pd.Timedelta('2 days')


def is_midnight_or_noon(date_time):
    return date_time.minute == 0 and (date_time.hour == 0 or date_time.hour == 12)


def is_new_day(date_time):
    return date_time.minute == 0 and date_time.hour == 0 \
           and date_time >= START + pd.Timedelta('1 days')


def is_new_period(date_time):
    return date_time > START and date_time.minute % 30 == 0


if __name__ == "__main__":
    for date_time in pd.date_range(start=START, end=END, freq='30min'):
        if is_new_period(date_time):
            oracle.update_consumption()
            agent1.update_private_data()
            agent2.update_private_data()
            agent3.update_private_data()

        if is_new_day(date_time):
            agent1.update_aggregate_data()
            agent2.update_aggregate_data()
            agent3.update_aggregate_data()

        if (is_midnight_or_noon(date_time)):
            print('-' * 59)
            print(' ' * 20 + str(date_time))
            print('-' * 59)

        time.sleep(PERIOD_LENGTH / 4.0)

        if is_betting_time(date_time):
            agent1.place_bet()
            agent2.place_bet()
            agent3.place_bet()

        time.sleep(PERIOD_LENGTH / 4.0)

        if is_ranking_time(date_time):
            agent1.rank_bet()
            agent2.rank_bet()
            agent3.rank_bet()

        time.sleep(PERIOD_LENGTH / 4.0)

        if is_collecting_time(date_time):
            agent1.collect_reward()
            agent2.collect_reward()
            agent3.collect_reward()

        time.sleep(PERIOD_LENGTH / 4.0)
