from geopy.distance import vincenty
from django.db import connection


class Route(object):
    filename = None
    distance = 0
    latitude = 'All-Latitude Decimal Degree (Text)'
    longitude = 'All-Longitude Decimal Degree (Text)'

    def __init__(self, f):
        self.filename = f.filename
        self.longitude = f.longitude
        self.latitude = f.latitude
        self.status = f.status



    def get_points(self, distance):
        if self.status == 'db':
            distance, points = self.get_points_from_db(distance)
        else:
            distance, points = self.get_points_from_file(distance)
        return distance, points

    def get_points_from_db(self, distance):
        cursor = connection.cursor()
        cursor.execute('''SELECT row->'%s', row->'%s' FROM routes WHERE (filename='%s') ORDER BY IDX''' % (self.longitude, self.latitude, self.filename))
        points = []
        route_distance = float(0)
        i = 0
        for row in cursor:
            i += 1
            current_point = dict(longitude=row[0], latitude=row[1], id=i, icon='/static/bul.png')
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

    def get_points_from_file(self, distance):
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
        return int(route_distance / 1000), points


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
            distance += current_distance
        return distance

    def get_points_from_file(self, filename, distance):
        points = []
        with open(filename) as f:
            columns = f.readline().split('\t')
            longitude_index = self.get_longitude_idx(columns)
            latitude_index = self.get_latitude_idx(columns)
            for row in f:
                row = row.split('\t')
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
        i = 0
        for row in cursor:
            points.append(dict(longitude=row[0], latitude=row[1], id=i, icon='/static/bul.png'))
            i += 1
        return points


