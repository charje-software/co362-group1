from web3 import Web3

# Needs to match address of contract migrated to ganache (set manually)
PREDICTION_MARKET = '0x068dd7B803aDaF4661960eE4337971c1Ae10d3bD'

# Account to be used by oracle, for testing, migrations etc.
ACCOUNT_0 = '0xd8CA13a2b3FB03873Ce14d2D04921a7D8552c28F'

# Hashes of methods in prediction market contract
PLACE_BET = '0x10962d45'  # placeBet(uint256[48])
RANK = '0x934209ce'  # rank()
CLAIM_WINNINGS = '0xb401faf1'  # claimWinnings()
UPDATE_CONSUMPTION = '0xa05d262b'  # updateConsumption(uint256)
UPDATE_CONSUMPTION = '0xa05d262b'  # updateConsumption(uint256)

# how many predictions to make per bet
NUM_PREDICTIONS = 48  # must be even

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
        self.partial_contract = self.w3.eth.contract(
            address=address,
            abi=[{
                "constant": True,
                "inputs": [
                    {
                        "name": "dayOffset",
                        "type": "uint256"
                    }
                ],
                "name": "getOracleConsumptions",
                "outputs": [
                    {
                        "name": "",
                        "type": "uint256[48]"
                    }
                ],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            }])

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

    def place_bet(self, agent_account, amount_in_eth, predictions):
        """
        Calls the PredictionMarket smart contract to place a bet on behalf of the agent.

        Args:
            agent_account: The agent's account on the blockchain.
            amount_in_eth: How much to bet.
            predictions: NUM_PREDICTIONS predictions of energy consumption
        """
        encoded_data = PLACE_BET
        for i in range(0, len(predictions)):
            encoded_data += (format(predictions[i], 'x')).zfill(64)

        self.w3.eth.sendTransaction(
            {'to': self.address, 'from': agent_account, 'value': amount_in_eth * ETH_TO_WEI,
             'data': encoded_data})

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
        balance_before = self.w3.eth.getBalance(agent_account)
        self.w3.eth.sendTransaction({'to': self.address, 'from': agent_account,
                                     'data': self.get_call_data(CLAIM_WINNINGS, [])})
        balance_after = self.w3.eth.getBalance(agent_account)
        return (balance_after - balance_before) > 0

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

    def get_latest_aggregate_consumptions(self):
        """
        Calls the PredictionMarket smart contract to fetch the latest NUM_PREDICTIONS oracle values.
        """
        return self.partial_contract.functions.getOracleConsumptions(2).call()
