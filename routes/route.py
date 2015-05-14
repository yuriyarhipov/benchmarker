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
        elif '.xls':
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
                    points.append([latitude, longitude])
        current_point = points[0]
        result_points = []
        for point in points[1:]:
            if vincenty(current_point, point).meters > distance:
                result_points.append(point)
                current_point = point

        points = result_points
        result_points = [points[0], ]
        for point in points[1:]:
            in_route = False
            for p in result_points:
                if vincenty(p, point).meters < distance:
                    in_route = True
            if not in_route:
                result_points.append(point)
        return result_points

    def is_point_in_route(self, point, points, distance):
        for p in points:
            if vincenty(p, point).meters < distance:
                return True
        return False

    def filter_points(self, base_points, points, distance):
        result = []
        for point in points:
            if not self.is_point_in_route(point, base_points, distance):
                result.append(point)
        return result

    def get_points(self, distance):
        points = []
        route_distance = 0
        for f in self.files:
            points.append(self.get_points_from_file(f, distance))
        if len(points) > 1:
            result = points[0]
            route_distance = self.get_distance(result)
            points = points[1:]
            for files_points in points:
                filtered_points = self.filter_points(result, files_points, distance)
                route_distance += self.get_distance(filtered_points)
                result.extend(filtered_points)
        else:
            result = points[0]
            route_distance = self.get_distance(result)
        return result, route_distance

    def get_route(self, route_id):
        points = []
        cursor = connection.cursor()
        cursor.execute('SELECT longitude, latitude FROM StandartRoutes WHERE (route_id=%s)', (route_id, ))
        for row in cursor:
            points.append(dict(lon=float(row[0]), lat=float(row[1])))
        return points


