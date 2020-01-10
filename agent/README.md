# Agent

## Prerequisites
```
python -m pip install -r requirements.txt
```

Because the Random Forest model file is too large for Github (> 100MB), see
[`/agent/models/README.md`](models/README.md) to download the Random Forest model. 

## Step-through demo
Make a workspace in Ganache with the following seed phrase to get reproducible account addresses:
```
goose eternal solar fence clean blur option shy debate runway other crater
```
In the `prediction-market` directory, migrate contracts:
```
truffle migrate --reset --network development
```

Ensure `PredictionMarketAdapter.PREDICTION_MARKET` is the deployed Prediction Market contract address.

Make sure you're on college network or use VPN so that Oracle data is accessible
and run:
```
python demo.py                         # starts at time 2014-01-28 00:00:00
python demo.py '2014-02-08 00:00:00'   # fast forwards to 2014-02-08 00:00:00
```

The demo runs through 2014-01-28 00:00:00 to 2014-02-27 23:30:00

| key | continue until |
| ------ | ------ |
| e | forever (end of demo) |
| d | next day |
| h | next half day |
| otherwise | next (30min) period|

Press the key and enter to progress through the demo.

## Demo with Autonomous Agents
This demo runs the Oracle and 7 different agents for a period representing '2014-01-28 00:00:00' to '2014-02-27 23:30:00' like the Step-through demo, but in this case the agents are each controlled by their own controller and pick random times with in allowed betting stages for their interactions
with the prediction market. The exception is the `CheatingAgent` which places its bets at the very end of the betting stage.

To run the demo, make sure that *ganache-cli* is running on *cloud-vm-41-214*. Otherwise, start it like this:
```
sudo docker run -d -p 8545:8545 trufflesuite/ganache-cli:latest -h 0.0.0.0 -m 'goose eternal solar fence clean blur option shy debate runway other crater'
```

Check that the it accepts RPC requests by e.g. listing the available accounts:
```
curl -X POST --data '{"jsonrpc":"2.0","method":"eth_accounts","params":[],"id":1}' http://146.169.41.214:8545
```

In the `prediction-market` directory, migrate contracts:
```
truffle migrate --reset --network internal_demo
```

### All
On a VM (recommended) or your machine, start a new *screen* and run the following script with suitable start, end and interval times.
The start time is actual time mapped to 00:00:00 of the first day in the demo, the demo will run until the actual end time provided
or for 31 virtual days, whichever is earlier. The interval time is the actual time representing 30min virtual time in the demo.
```
sh demo.sh '2020-01-03 10:48:00' '2020-02-28 00:00:00' '30min'
```

### Custom Alternative
Run the Oracle (on college network) with suitable start, end and interval times.
```
python -m agents.oracle '2020-02-02 14:48:00' '2020-02-28 00:00:00' '30min'
```
Run one or more of scripts in the `participants` directory each running an agent.
These scripts take the same arguments as `oracle.py`.

## Contributing
When modifying the code, run pylint:
```
pycodestyle --show-source --show-pep8 --max-line-length=100 *.py **/*.py
```

To run all tests:
```
python -m unittest discover test
```
Run a test e.g.:
```
python -m unittest test.test_agent_unittest
```

To compare model performance:
```
python calc_model_accuracy.py
```
