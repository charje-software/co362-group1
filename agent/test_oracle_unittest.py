import unittest

from unittest import TestCase, mock

from oracle import Oracle


class TestOracle(TestCase):

    JSON_TEST_DATA = {
        '1': {'consumption': '500',
              'datetime': '2014-01-28 00:00:00'},
        '2': {'consumption': '288',
              'datetime': '2014-01-28 00:30:00'},
        '3': {'consumption': '863',
              'datetime': '2014-01-28 01:00:00'}
        }

    def test_query_live_data(self):
        with mock.patch('oracle.requests.get', autospec=True) as mock_oracle_get:
            mock_oracle_get.return_value.json.return_value = TestOracle.JSON_TEST_DATA

            oracle = Oracle()

            result1 = oracle.query_live_data()
            self.assertEqual(result1, '500')

            result2 = oracle.query_live_data()
            self.assertEqual(result2, '288')

            self.assertEqual(mock_oracle_get.call_count, 2)

    def test_query_data_end_should_error(self):
        oracle = Oracle(Oracle.DATA_SIZE + 1)
        self.assertRaises(ValueError, oracle.query_live_data)

    def test_update_consumption(self):
        with mock.patch('oracle.PredictionMarketAdapter', autospec=True) as mock_prediction_market,\
              mock.patch('oracle.requests.get', autospec=True) as mock_oracle_get:

            mock_prediction_market = mock_prediction_market.return_value
            mock_oracle_get.return_value.json.return_value = TestOracle.JSON_TEST_DATA
            oracle = Oracle()

            oracle.update_consumption()
            oracle.update_consumption()
            oracle.update_consumption()

            self.assertEqual(mock_prediction_market.update_consumption.mock_calls, [
                mock.call(Oracle.ACCOUNT, int(TestOracle.JSON_TEST_DATA['1']['consumption'])),
                mock.call(Oracle.ACCOUNT, int(TestOracle.JSON_TEST_DATA['2']['consumption'])),
                mock.call(Oracle.ACCOUNT, int(TestOracle.JSON_TEST_DATA['3']['consumption']))
            ])


if __name__ == '__main__':
    unittest.main()