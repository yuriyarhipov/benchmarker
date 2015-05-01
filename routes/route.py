import psycopg2
from os.path import basename

from geopy.distance import vincenty, great_circle

class Route(object):
    filename = None
    distance = 0
    latitude = 'All-Latitude Decimal Degree (Text)'
    longitude = 'All-Longitude Decimal Degree (Text)'

    def __init__(self, f):
        self.filename = f.filename
        self.longitude =f.longitude
        self.latitude =f.latitude

    def get_latitude_idx(self, columns):
        latitude = self.latitude
        idx_latitude = None
        if latitude in columns:
            idx_latitude = columns.index(latitude)
        elif 'latitude' in columns:
            idx_latitude = columns.index('latitude')
        return idx_latitude

    def get_longitude_idx(self, columns):
        longitude = self.longitude
        idx_longitude = None
        if longitude in columns:
            idx_longitude = columns.index(longitude)
        elif 'longitude' in columns:
            idx_longitude = columns.index('longitude')
        return idx_longitude

    def get_points(self, distance):
        points = []
        route_distance = float(0)
        with open(self.filename) as f:
            first_line = f.readline()
            columns = [col for col in first_line.split('\t')]
            idx_latitude = self.get_latitude_idx(columns)
            idx_longitude = self.get_longitude_idx(columns)

            i = 0
            for row in f:
                row = row.split('\t')
                if (row[2] != 'Not Valid') and (row[idx_longitude] != ''):
                    i += 1
                    current_point = dict(longitude=row[idx_longitude], latitude=row[idx_latitude], id=i, icon='/static/bul.png')
                    if len(points) == 0:
                        points.append(current_point)
                        previous_point = current_point
                    else:
                        point_distance = vincenty((points[-1]['latitude'], points[-1]['longitude']), (current_point['latitude'], current_point['longitude'])).meters
                        if point_distance > distance:
                            points.append(current_point)
                            route_distance = route_distance + vincenty((previous_point['latitude'], previous_point['longitude']), (current_point['latitude'], current_point['longitude'])).meters
                        previous_point = current_point
        return int(route_distance /1000), points


