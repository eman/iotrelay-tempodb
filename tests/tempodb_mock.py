TIME_FMT = "%Y-%m-%d %H:%M:%S"


class DataPoint(object):
    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

    def __str__(self):
        return "{0!s}, {1}".format(self.timestamp, self.value)

    def __repr__(self):
        return str(self)


class Client(object):
    data_points = []

    def __init__(self, api_key, secret):
        pass

    @classmethod
    def reset(cls):
        cls.data_points = []

    def write_key(self, series_key, data_points):
        for point in data_points:
            timestamp = point.timestamp.strftime(TIME_FMT)
            self.data_points.append([timestamp, series_key, point.value])
