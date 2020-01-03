import unittest
from unittest import TestCase, mock

from agents.oracle import Oracle
from agents.prediction_market_adapter import ACCOUNT_0


class TestOracle(TestCase):

    JSON_TEST_DATA = {
        '1': {'consumption': '500',
              'datetime': '2014-01-28 00:30:00'},
        '2': {'consumption': '288',
              'datetime': '2014-01-28 01:00:00'},
        '3': {'consumption': '863',
              'datetime': '2014-01-28 01:30:00'}
        }

    def test_query_live_data(self):
        with mock.patch('agents.oracle.requests.get', autospec=True) as mock_oracle_get:
            mock_oracle_get.return_value.json.return_value = TestOracle.JSON_TEST_DATA

            oracle = Oracle(logging=False)

            result1, _ = oracle.query_live_data()
            self.assertEqual(result1, '500')

            result2, _ = oracle.query_live_data()
            self.assertEqual(result2, '288')

            self.assertEqual(mock_oracle_get.call_count, 2)

    def test_query_data_end_should_error(self):
        oracle = Oracle(Oracle.DATA_SIZE + 1, logging=False)
        self.assertRaises(ValueError, oracle.query_live_data)

    def test_update_consumption(self):
        with mock.patch('agents.oracle.PredictionMarketAdapter', autospec=True) \
                    as mock_prediction_market, \
                    mock.patch('agents.oracle.requests.get', autospec=True) \
                    as mock_oracle_get:

            mock_prediction_market = mock_prediction_market.return_value
            mock_oracle_get.return_value.json.return_value = TestOracle.JSON_TEST_DATA
            oracle = Oracle(logging=False)

            oracle.update_consumption()
            oracle.update_consumption()
            oracle.update_consumption()

            self.assertEqual(mock_prediction_market.update_consumption.mock_calls, [
                mock.call(ACCOUNT_0, int(TestOracle.JSON_TEST_DATA['1']['consumption'])),
                mock.call(ACCOUNT_0, int(TestOracle.JSON_TEST_DATA['2']['consumption'])),
                mock.call(ACCOUNT_0, int(TestOracle.JSON_TEST_DATA['3']['consumption']))
            ])


if __name__ == '__main__':
    unittest.main()
