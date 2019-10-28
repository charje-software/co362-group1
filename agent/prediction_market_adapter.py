from web3 import Web3

# TODO: Decide how to set constants for local / VM hosted ganache.
#       Currently addresses need to be set manually.

# Needs to match address of contract migrated to ganache
PREDICTION_MARKET = '0x41D504711eEf11Cc040ebA89B32902bf31CCb39e'

# Hashes of methods in prediction market contract
PLACE_BET = '0x10fe7c48'           # placeBet(uint256)
RANK = '0x934209ce'                # rank()
CLAIM_WINNINGS = '0xb401faf1'      # claimWinnings()
UPDATE_CONSUMPTION = '0xa05d262b'  # updateConsumption(uint256)

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

    def get_call_data(self, function_hash, params):
        """
        Computes the data field for a corresponding contract function call.

        Args:
            function_hash: First 8 characters of the hex hash of the function
            params: List of parameters (strings) for the function.
        """
        if (len(params) == 0):
            return function_hash + ''.zfill(64)

        data = function_hash
        for i in range(0, len(params)):
            data += params[i].zfill(64)
        return data

    def place_bet(self, agent_account, amount_in_eth, prediction):
        """
        Calls the PredictionMarket smart contract to place a bet on behalf of the agent.

        Args:
            agent_account: The agent's account on the blockchain.
            amount_in_eth: How much to bet.
            prediction: How much agent thinks total demand will be
        """
        self.w3.eth.sendTransaction(
            {'to': self.address, 'from': agent_account, 'value': amount_in_eth * ETH_TO_WEI,
             'data': self.get_call_data(PLACE_BET, [format(prediction, 'x')])})

    def rank(self, agent_account):
        """
        Calls the PredictionMarket smart contract to rank the agent's prediction.

        Args:
            agent_account: The agent's account on the blockchain.
        """
        self.w3.eth.sendTransaction({'to': self.address, 'from': agent_account,
                                     'data': self.get_call_data(RANK, [])})

    def transfer_reward(self, agent_account):
        """
        Calls the PredictionMarket smart contract to transfer the agent's winnings to its account.

        Args:
            agent_account: The agent's account on the blockchain.
        """
        self.w3.eth.sendTransaction({'to': self.address, 'from': agent_account,
                                     'data': self.get_call_data(CLAIM_WINNINGS, [])})

    def update_consumption(self, oracle_account, updated_consumption):
        """
        Calls the PredictionMarket smart contract to pass in live data for most recent time period,
        used to rank agent predictions.

        Args:
            oracle_account: The Oracle agent's account on the blockchain.
            updated_consumption: The consumption figure for the previous time period.
        """
        self.w3.eth.sendTransaction(
            {'to': self.address, 'from': oracle_account,
             'data': self.get_call_data(UPDATE_CONSUMPTION, [format(updated_consumption, 'x')])})
