# co362-group1

Software Engineering Project for Group 1:
Crowd-sourcing agent-based machine learning algorithms using prediction marketplaces implemented on a blockchain

## Interactive Demo

Seed phrase for Ganache:
```
goose eternal solar fence clean blur option shy debate runway other crater
```
More info on how to run agents in `agent/README.md`.

## Autonomous Demo

Running ganache-cli in docker with same seed phrase
```
sudo docker run -d -p 8545:8545 trufflesuite/ganache-cli:latest -h 0.0.0.0 -m 'goose eternal solar fence clean blur option shy debate runway other crater'
```

Test that accounts match:
```
curl -X POST --data '{"jsonrpc":"2.0","method":"eth_accounts","params":[],"id":1}' localhost:8545
```
More info on how to run agents in `agent/README.md`.
