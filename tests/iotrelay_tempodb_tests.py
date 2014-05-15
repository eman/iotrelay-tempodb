from datetime import datetime
from unittest import TestCase
import csv
import os
from iotrelay import Reading
from tests.tempodb_mock import Client, DataPoint
import iotrelay_tempodb

iotrelay_tempodb.Client = Client
iotrelay_tempodb.DataPoint = DataPoint

TIME_FMT = "%Y-%m-%d %H:%M:%S %z"
TEST_DATA = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                         "test_data.csv")


class IoTTempoDBTest(TestCase):
    def readings(self):
        try:
            return self._readings
        except AttributeError:
            with open(TEST_DATA, 'rt') as f:
                self._readings = [line for line in csv.reader(f)]
        return self._readings

    def compare_readings(self, num_readings):
        config = {'batch size': num_readings, 'api key': '', 'api secret': ''}
        Client.reset()
        tdb_handler = iotrelay_tempodb.Handler(config)
        for ts, key, value in self.readings():
            timestamp = datetime.strptime(ts, TIME_FMT)
            tdb_handler.set_reading(Reading('weather', value, timestamp, key))
        tdb_handler.flush()
        self.assertEqual(sorted(Client.data_points), sorted(self.readings()))

    def test_compare_readings_batch_size_one(self):
        config = {'batch size': 1, 'api key': '', 'api secret': ''}
        Client.reset()
        tdb_handler = iotrelay_tempodb.Handler(config)
        for ts, key, value in self.readings():
            timestamp = datetime.strptime(ts, TIME_FMT)
            tdb_handler.set_reading(Reading('weather', value, timestamp, key))
        self.assertEqual(Client.data_points, self.readings())

    def test_compare_readings_vary_batch_size(self):
        [self.compare_readings(i) for i in range(2, 12)]
