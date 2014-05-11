import logging
from collections import defaultdict
from tempodb import Client, DataPoint

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
        if reading is None:
            return
        logger.debug('tempodb setting: {0!s}, {1}'.format(reading.timestamp,
                                                          reading.value))
        option = "{0} batch size".format(reading.reading_type)
        batch_size = self.config.get(option, self.batch_size)
        data = self.readings[(reading.series_key, reading.reading_type)]
        data.append(DataPoint(reading.timestamp, reading.value))
        if len(data) >= batch_size:
            option = "{0} api key".format(reading.reading_type)
            api_key = self.config.get(option, self.api_key)
            option = "{0} api secret".format(reading.reading_type)
            api_secret = self.config.get(option, self.api_secret)
            Client(api_key, api_secret).write_key(reading.series_key, data)
            self.readings[(reading.series_key, reading.reading_type)] = []

    def flush(self):
        for series, data in self.readings.items():
            option = "{0} api key".format(series[1])
            api_key = self.config.get(option, self.api_key)
            option = "{0} api secret".format(series[1])
            api_secret = self.config.get(option, self.api_secret)
            Client(api_key, api_secret).write_key(series[0], data)
            self.readings[series] = []
