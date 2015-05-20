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

    def get_points_from_file(self, filename, distance):
        points = []
        f_distance = 0
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
                    if points:
                        f_distance += vincenty(points[-1], [float(latitude), float(longitude)])
                    points.append([float(latitude), float(longitude)])

        points = self.fast_distance(points, distance)
        points = self.map_distance(points, distance)
        return points, f_distance

    def fast_distance(self, points, distance):
        result = [points[0], ]
        points = points[1:]
        for p in points:
            if vincenty(result[-1], p).meters > distance:
                result.append(p)
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

    def map_distance(self, points, distance):
        points_dict = dict()
        result_points = []
        for p in points:
            key_point = float("{0:.4f}".format(p[0]))
            if key_point not in points_dict:
                points_dict[key_point] = []
            points_dict[key_point].append(p)

        for key, points in points_dict.iteritems():
            result_points.extend(self.slow_distance(points, distance))
        return result_points

    def get_points(self, distance):
        points = []
        route_distance = 0
        for f in self.files:
            file_points, file_distance = self.get_points_from_file(f, distance)
            route_distance += file_distance
            points.extend(file_points)
        points = self.map_distance(points, distance)
        return points, route_distance

    def get_route(self, route_id):
        points = []
        cursor = connection.cursor()
        cursor.execute('SELECT longitude, latitude FROM StandartRoutes WHERE (route_id=%s)', (route_id, ))
        for row in cursor:
            points.append(dict(lon=float(row[0]), lat=float(row[1])))
        return points


