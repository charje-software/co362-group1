# Agent

## Running demo
Check that:
 - `Oracle.ACCOUNT` is account[0] in Ganache
 - `ACCOUNTS` in `demo.py` matches accounts[1..9] in Ganache.
 - `PredictionMarketAdapter.PREDICTION_MARKET` is Prediction Market contract address. (note: run `truffle migrate` before hand)

Make sure you're on college network or use VPN so that Oracle data is accessible
and run
```
python demo.py
```

## Autonomous Agents and Oracle
Run the Oracle (on college network) with suitable start, end and interval times.
```
python oracle.py '2020-01-02 14:48:00' '2020-01-28 00:00:00' '30min'
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
