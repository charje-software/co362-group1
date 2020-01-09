import pandas as pd
from colr import color
import sys

from agents.ar_agent import ArAgent
from agents.ar_retrain_agent import ArRetrainAgent
from agents.ar_retrain_decision_agent import ArRetrainDecisionAgent
from agents.cheating_agent import CheatingAgent
from agents.lstm_agent import LstmAgent
from agents.lstm_multi_agent import LstmMultiAgent
from agents.rf_agent import RfAgent
from agents.oracle import Oracle

START = pd.to_datetime('2014-01-28 00:00:00')
END = pd.to_datetime('2014-02-27 23:30:00')

ACCOUNTS = ['0xEA43d7cE5224683B1D83D19327699756504fB489',
            '0x4B516E6c8c3a5Ea97Ff7377d81Ea2238C46C5882',
            '0x768848539fc4AA09435797773456d114ea83bcE1',
            '0xfcC640fB2629943aaaA35c4D0A79000e0bfc8870',
            '0x80Fb53cb93F0e23b7698E6475498d3395806B2c9',
            '0x30717eD75d2c188eB01bCB8733C291B6348B6F5B',
            '0x844A203E1D962E61505f6ef17abBF432f3F680d5',
            '0x3FFA1EA78d44488c43DE84B6D03C3b6C0DC7248E',
            '0x0A058293Feb18aedbca8c2169947381d2e71F424']

agent1 = ArAgent(ACCOUNTS[0], color='A63D40', name='Chris  ')
agent2 = ArRetrainAgent(ACCOUNTS[1], color='9e4acf', name='Hannah ')
agent3 = ArRetrainDecisionAgent(ACCOUNTS[2], color='3959bf', name='Ashly  ')
agent4 = LstmAgent(ACCOUNTS[3], color='6494AA', name='Ram    ')
household_2_normalise_values = [1.16123236e+03, 4.24041018e+02, 2.47572234e-01, 2.41049693e-01]
agent5 = LstmMultiAgent(
    account=ACCOUNTS[4],
    model_file_name='./models/LSTMmultivariate.h5',
    household_name='MAC000002',
    normalise_values=household_2_normalise_values, color='E9B872', name='Jasmine')
agent6 = RfAgent(ACCOUNTS[5], color='90A959', name='Esther ')
agent7 = CheatingAgent(ACCOUNTS[6], color='151515', name='Cheater')
# important that cheating agent is last / near end
agents = [agent1, agent2, agent3, agent4, agent5, agent6, agent7]
oracle = Oracle()


def is_midnight(date_time):
    return date_time.minute == 0 and date_time.hour == 0


def is_noon(date_time):
    return date_time.minute == 0 and date_time.hour == 12


def is_new_day(date_time):
    return is_midnight(date_time) and date_time > START


def is_new_period(date_time):
    return date_time > START and date_time.minute % 30 == 0


def get_input_and_update(forever, day, half_day):
    key = input(color('Continue until end [e], the next day [d], half_day' +
                ' [h], period [otherwise]? ... ', fore='595959'))
    if key == 'e':
        forever = True
    elif key == 'd':
        day = True
    elif key == 'h':
        half_day = True
    return forever, day, half_day


if __name__ == "__main__":
    if len(sys.argv) == 2:
        fast_forward = pd.to_datetime(sys.argv[1])
    else:
        fast_forward = START

    # flags set by keyboard input
    forever = False
    day = False
    half_day = False

    for date_time in pd.date_range(start=START, end=END, freq='30min'):
        if is_new_period(date_time):
            oracle.update_consumption()
            for agent in agents:
                agent.update_per_period()

        if is_new_day(date_time):
            day = False
            for agent in agents:
                agent.update_daily()

        if (is_midnight(date_time) or is_noon(date_time)):
            half_day = False
            print(color('-' * 59, fore='595959'))
            print(color(' ' * 20 + str(date_time), fore='595959'))
            print(color('-' * 59, fore='595959'))

        if not forever and not day and not half_day and date_time >= fast_forward:
            forever, day, half_day = get_input_and_update(forever, day, half_day)

        if is_midnight(date_time):
            if date_time < END - pd.Timedelta('2days'):
                for agent in agents:
                    agent.place_bet()
            else:
                for agent in agents:
                    agent.prediction_history.append(None)

        if is_midnight(date_time - pd.Timedelta('30min')):
            for agent in agents:
                agent.rank_bet()

        elif is_noon(date_time):
            for agent in agents:
                agent.collect_reward()
