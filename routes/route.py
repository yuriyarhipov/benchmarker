from operator import itemgetter

from geopy.distance import vincenty
from django.db import connection
from lib.excel import Excel


class StandartRoute(object):
    latitude = 'All-Latitude Decimal Degree (Text)'
    longitude = 'All-Longitude Decimal Degree (Text)'

    def __init__(self, files):
        self.files = files

    def get_latitude_idx(self, columns):
        columns = [col.lower() for col in columns]
        latitude = self.latitude.lower()
        idx_latitude = None
        if latitude.lower() in columns:
            idx_latitude = columns.index(latitude)
        elif 'latitude' in columns:
            idx_latitude = columns.index('latitude')
        return idx_latitude

    def get_longitude_idx(self, columns):
        columns = [col.lower() for col in columns]
        longitude = self.longitude.lower()
        idx_longitude = None
        if longitude.lower() in columns:
            idx_longitude = columns.index(longitude)
        elif 'longitude' in columns:
            idx_longitude = columns.index('longitude')
        return idx_longitude

    def get_distance(self, points):
        if len(points) < 2:
            return 0
        current_point = points[0]
        distance = 0
        for p in points[1:]:
            current_distance = vincenty(current_point, p).km
            current_point=p
            distance += current_distance
        return distance

    def get_points_from_file(self, filename, distance):
        points = []
        if '.csv' in filename:
            with open(filename) as f:
                columns = f.readline().split(',')
                data = [row.split(',') for row in f]
        elif '.xls' in filename:
            data = Excel(filename).get_data()
            columns = data[0]
            data = data[1:]
        else:
            with open(filename) as f:
                columns = f.readline().split('\t')
                data = [row.split('\t') for row in f]

        if data and columns:
            longitude_index = self.get_longitude_idx(columns)
            latitude_index = self.get_latitude_idx(columns)
            for row in data:
                longitude = row[longitude_index].strip()
                latitude = row[latitude_index].strip()
                if longitude and latitude:
                    points.append([float(latitude), float(longitude)])

        points = self.fast_distance(points, distance)
        points.sort()
        points = self.fast_distance(points, distance)
        points.sort(key=itemgetter(0))
        points = self.fast_distance(points, distance)
        points.sort(key=itemgetter(1))
        points = self.fast_distance(points, distance)
        return points

    def fast_distance(self, points, distance):
        result = [points[0], ]
        points = points[1:]
        for p in points:
            if vincenty(result[-1], p).meters > distance:
                result.append(p)
        result = self.middle_distance(result, distance)
        return result

    def slow_distance(self, points, distance):
        result = [points[0], ]
        points = points[1:]
        for p in points:
            status = True
            for rp in result:
                if vincenty(p, rp).meters < distance:
                    status = False
                    break
            if status:
                result.append(p)
        return result

    def middle_distance(self, points, distance):
        i = 0
        result = []
        while (i < len(points)):
            result.extend(self.slow_distance(points[i:i + 100], distance))
            i += 100
        return result

    def get_points(self, distance):
        points = []
        route_distance = 0
        for f in self.files:
            points.extend(self.get_points_from_file(f, distance))
        points.sort()
        points = self.fast_distance(points, distance)
        points.sort(key=itemgetter(0))
        points = self.fast_distance(points, distance)
        points.sort(key=itemgetter(1))
        points = self.fast_distance(points, distance)
        if points:
            route_distance = int((len(points) - 1) * distance/1000)

        return points, route_distance

    def get_route(self, route_id):
        points = []
        cursor = connection.cursor()
        cursor.execute('SELECT longitude, latitude FROM StandartRoutes WHERE (route_id=%s)', (route_id, ))
        for row in cursor:
            points.append(dict(lon=float(row[0]), lat=float(row[1])))
        return points


