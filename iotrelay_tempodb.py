'''
Copyright (c) 2014, Emmanuel Levijarvi
All rights reserved.
License BSD
'''
import logging
from collections import defaultdict
from tempodb import Client, DataPoint
import requests

logger = logging.getLogger(__name__)
__version__ = "1.0.0"
DEFAULT_BATCH_SIZE = 30


class Handler(object):
    def __init__(self, config):
        self.readings = defaultdict(list)
        self.config = config
        self.batch_size = int(config.get('batch size', DEFAULT_BATCH_SIZE))
        self.api_key = config['api key']
        self.api_secret = config['api secret']

    def set_reading(self, reading):
        logger.debug('tempodb setting: {0!s}'.format(reading))
        data = self.readings[(reading.series_key, reading.reading_type)]
        data.append(DataPoint(reading.timestamp, reading.value))
        batch_option = "{0} batch size".format(reading.reading_type)
        if len(data) >= int(self.config.get(batch_option, self.batch_size)):
            self.send_reading(reading.series_key, reading.reading_type, data)
            self.readings[(reading.series_key, reading.reading_type)] = []

    def flush(self):
        (self.send_reading(series[0], series[1], data)
         for series, data in self.readings.items())

    def send_reading(self, series_key, reading_type, data):
        api_key_option = "{0} api key".format(reading_type)
        api_key = self.config.get(api_key_option, self.api_key)
        api_secret_option = "{0} api secret".format(reading_type)
        api_secret = self.config.get(api_secret_option, self.api_secret)
        try:
            Client(api_key, api_secret).write_key(series_key, data)
        except requests.exceptions.RequestException as e:
            logger.error('Unable to send {0} to TempoDB. {1!s}'.format(
                         series_key, e))
        else:
            del self.reading[(series_key, reading_type)]
