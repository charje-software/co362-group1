from web3 import Web3
from constants import PREDICTION_MARKET, PLACE_BET, DISTRIBUTE_WINNINGS, ETH_TO_WEI

class Agent:
    def __init__(self, account, rpc_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = account

    def place_bet(self, amountInEth):
        self.w3.eth.sendTransaction({'to': PREDICTION_MARKET, 'from': self.account, 'value': amountInEth * ETH_TO_WEI, 'data': PLACE_BET})

    def get_winnings(self):
        self.w3.eth.sendTransaction({'to': PREDICTION_MARKET, 'from': self.account, 'data': DISTRIBUTE_WINNINGS})
