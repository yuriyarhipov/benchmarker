from operator import itemgetter

from geopy.distance import vincenty
from django.db import connection


class StandartRoute(object):

    def __init__(self, files):
        self.files = files

    def route(self, distance):
        cursor = connection.cursor()
        sql_files = ','.join(["'%s'" % f for f in self.files])

        cursor.execute('''
            SELECT DISTINCT
                latitude,
                longitude
            FROM
                uploaded_files
            WHERE
                filename in (%s)
            ORDER BY latitude, longitude;
            ''' % (sql_files))

        points = cursor.fetchall()

        points = self.fast_distance(points, distance)
        points = self.sort_points(points)
        points = self.fast_distance(points, distance)
        print len(points)
        points = self.points_sort(points, distance, 10)
        print len(points)
        return points

    def points_sort(self, data, distance, index_range):
        data.sort()
        status = True
        idx = 1
        while status:
            status = False
            for i in range(len(data)):
                if i + idx < len(data):
                    while (i + idx < len(data)) and (vincenty(data[i], data[i + idx]).meters <= distance):
                        data.pop(i + idx)
                else:
                    break
            if idx < index_range:
                status = True
                idx += 1
        return data

    def slow_distance(self, sort_points, distance):
        i = 0
        while i < len(sort_points):
            points = sort_points[i:i + 100]
            i += 100
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

    def fast_distance(self, points, distance):
        result = [points[0], ]
        points = points[1:]
        for p in points:
            if vincenty(result[-1], p).meters > distance:
                result.append(p)
        return result

    def sort_points(self, points):
        temp_result = []
        for point in points:
            temp_result.append([point, point[0] + point[1]])
        temp_result.sort(key=itemgetter(1))
        points = [p[0] for p in temp_result]
        return points

    def get_points(self, distance):
        points = []
        for f in self.files:
            points.extend(self.get_points_from_file(f, distance))
        points.sort()
        points = self.fast_distance(points, distance)
        points.sort(key=itemgetter(1))
        points = self.fast_distance(points, distance)
        points = self.sort_points(points)
        points = self.fast_distance(points, distance)
        points = self.slow_distance(points, distance)
        return points

    def get_route(self, route_id, color):
        points = []
        cursor = connection.cursor()
        cursor.execute('SELECT longitude, latitude FROM StandartRoutes WHERE (route_id=%s)', (route_id, ))
        for row in cursor:
            points.append(dict(lon=float(row[0]), lat=float(row[1]), color=color))
        return points
