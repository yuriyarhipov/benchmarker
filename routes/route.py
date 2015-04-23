import psycopg2
from os.path import basename

from geopy.distance import vincenty

class Route(object):
    filename = None
    distance = 0
    latitude = 'All-Latitude Decimal Degree (Text)'
    longitude = 'All-Longitude Decimal Degree (Text)'

    def __init__(self, filename, distance):
        self.filename = filename
        self.distance = distance

    def get_points(self):
        
        return int(route_distance/1000), data


