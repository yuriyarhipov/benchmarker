import json

from operator import itemgetter

from geopy.distance import vincenty
from numpy import isnan
from pandas import read_table
from django.db import connection

from routes.models import RouteFile
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

    def save_points_to_database(self, filename, project_id, module):
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

            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS uploaded_files (id SERIAL, filename TEXT, project_id INT, module INT, latitude NUMERIC, longitude NUMERIC, row JSON)')
            cursor.execute('DELETE FROM uploaded_files WHERE (filename=%s) AND (project_id=%s) AND (module=%s)',
                           (filename,
                            project_id,
                            module)
                           )
            connection.commit()
            distance = 0
            last_point = None
            for row in data:
                if row[longitude_index] and row[latitude_index] :
                    longitude = row[longitude_index].strip()
                    latitude = row[latitude_index].strip()
                    if last_point:
                        distance += vincenty([latitude, longitude], last_point).meters
                    last_point = [latitude, longitude]
                    cursor.execute(
                        'INSERT INTO uploaded_files (filename, project_id, module, latitude, longitude, row) VALUES (%s, %s, %s, %s, %s, %s)',
                        (filename,
                        project_id,
                        module,
                        latitude,
                        longitude,
                        json.dumps(self.get_row(columns, row)))
                    )
            connection.commit()
            RouteFile.objects.filter(filename=filename).update(distance=distance)

    def get_row(self, columns, row):
        result = dict()
        for col in columns:
            result[col] = row[columns.index(col)]
        return result

    def get_points_from_file(self, filename, distance):
        points = []
        if '.csv' or '.txt' in filename:
            file_reader = read_table(filename, chunksize=1000)
            data = []
            #with open(filename) as f:
            #    columns = f.readline().split(',')
            #    data = [row.split(',') for row in f]
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
                if row[longitude_index] and row[latitude_index] :
                    longitude = row[longitude_index].strip()
                    latitude = row[latitude_index].strip()
                    if longitude and latitude:
                        try:
                            points.append([float(latitude), float(longitude)])
                        except:
                            print latitude, longitude


        #points = self.fast_distance(points, distance)
        #points.sort()
        #points = self.fast_distance(points, distance)
        #points.sort(key=itemgetter(1))
        #points = self.fast_distance(points, distance)
        #points = self.sort_points(points)
        #points = self.fast_distance(points, distance)
        return points

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
        return points

    def get_route(self, route_id, color):
        points = []
        cursor = connection.cursor()
        cursor.execute('SELECT longitude, latitude FROM StandartRoutes WHERE (route_id=%s)', (route_id, ))
        for row in cursor:
            points.append(dict(lon=float(row[0]), lat=float(row[1]), color=color))
        return points


