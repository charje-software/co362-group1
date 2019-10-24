from web3 import Web3

# TODO: Decide how to set constants for local / VM hosted ganache.
#       Currently addresses need to be set manually.

# Needs to match address of contract migrated to ganache
PREDICTION_MARKET = '0x41D504711eEf11Cc040ebA89B32902bf31CCb39e'

# Hashes of methods in prediction market contract
PLACE_BET = '0xf90f456000000000000000000000000000000000000000000000000000000000'
DISTRIBUTE_WINNINGS = '0x7d2026cd00000000000000000000000000000000000000000000000000000000'

# Local ganache
RPC_URL = 'http://127.0.0.1:7545'

# Conversion rate between ether and wei
ETH_TO_WEI = 10 ** 18


class PredictionMarketAdapter:
    """Adapter for PredictionMarket smart contract.

    Attributes:
        w3:      Web3 instance for connectiong to the blockchain.
        address: Address on the deployed PredictionMarket smart contract on the blockchain.
    """

    def __init__(self, address=PREDICTION_MARKET, rpc_url=RPC_URL):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.address = address

    def place_bet(self, agent_account, amount_in_eth):
        """
        Calls the PredictionMarket smart contract to place a bet on behalf of the agent.

        Args:
            agent_account: The agent's account on the blockchain.
            amount_in_eth: How much to bet.
        """
        self.w3.eth.sendTransaction(
            {'to': self.address, 'from': agent_account, 'value': amount_in_eth * ETH_TO_WEI,
             'data': PLACE_BET})

    def transfer_reward(self, agent_account):
        """
        Calls the PredictionMarket smart contract to transfer the agent's winnings to its account.

        Args:
            agent_account: The agent's account on the blockchain.
        """
        self.w3.eth.sendTransaction({'to': self.address, 'from': agent_account,
                                     'data': DISTRIBUTE_WINNINGS})
