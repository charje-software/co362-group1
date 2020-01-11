# Prediction Market

## Setup
Install dependencies by running:

```
npm install
```

Install [Ganache](https://www.trufflesuite.com/ganache) and create a workspace with `truffle-config.js`

Add a file called `secrets.json` with the following contents (only required if you want to deploy to Ropsten):
```
{
    "InfuraApiKey": "YOUR_API_KEY",
    "Mnemonic": "YOUR_SEED_PHRASE"
}
```

## Compile, Migrate, Test
Make sure to have Ganache running. The default network that truffle migrates to is [`development`](truffle-config.js) which details the default port and IP address (localhost) Ganache runs on.

To compile, migrate and test:

```
truffle compile

truffle migrate

truffle test
```

Note that the default network that truffle migrates to is `development`.

## Interacting with the contract

Use the Web3 API (e.g. Web3.js, Web3.py) to interact with the contract.

For example, using [Metamask](https://metamask.io/) and opening the console in your browser, run:

```
window.eth.sendTransaction({'to': 'contract_address', 'from': 'account_address', 'data': 'function_hash'}, console.log)
```

Get the function hash by going to https://emn178.github.io/online-tools/keccak_256.html and hash the function definition (e.g. functionName(uint)). Get the first 8 digits and pad the rest of the 32 bits with 0s.

### Prediction Market Adapter

Alternatively, we have written a Python prediction market adapter for our autonomous Python agents to
interact with the smart contract. See [`agent/agents/prediction_market_adapter.py`](../agent/agents/prediction_market_adapter.py)