# Agent

## Running demo
Check that:
 - `Oracle.ACCOUNT` is account[0] in Ganache
 - `ACCOUNTS` in `demo.py` matches accounts[1..9] in Ganache.
 - `PredictionMarketAdapter.PREDICTION_MARKET` is Prediction Market contract address. (note: run `truffle migrate` before hand)

## Contributing
When modifying the code, run pylint:
```
pycodestyle --show-source --show-pep8 --max-line-length=100 *.py
```

To run tests:
```
python test_agent_unittest.py
python test_oracle_unittest.py
python test_meter_unittest.py
```

To compare model performance:
```
python calc_model_accuracy.py
```
