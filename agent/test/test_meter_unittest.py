import unittest
from unittest import TestCase

from agents.meter import Meter


class TestMeter(TestCase):

    def test_get_latest_aggregate_consumption(self):
        expected1 = 0.434
        expected2 = 0.561
        meter = Meter('MAC000002')

        actual1 = meter.get_latest_consumption()
        actual2 = meter.get_latest_consumption()

        self.assertEqual(expected1, actual1)
        self.assertEqual(expected2, actual2)


if __name__ == '__main__':
    unittest.main()
