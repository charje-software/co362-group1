# Agent

## Running demo
Change:
 - `Oracle.ACCOUNT` to account[0] in Ganache
 - `ACCOUNTS` in `demo.py` to accounts[1..9] in Ganache.
 - `PredictionMarketAdapter.PREDICTION_MARKET` to Prediction Market contract address. (note: run `truffle migrate` before hand)

## Contributing
When modifying the code, run pylint:
```
pycodestyle --show-source --show-pep8 --max-line-length=100 *.py
```

To run tests:
```
python test_agent_unittest.py
python test_oracle_unittest.py
```