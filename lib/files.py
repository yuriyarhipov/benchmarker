from django.conf import settings
from django.db import connection
from pandas import read_table
import json


def handle_uploaded_file(uploaded_files):
    path = settings.STATICFILES_DIRS[0]
    result = []
    for f in uploaded_files:
        filename = '/'.join([path, f.name])
        destination = open(filename, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        result.append(filename)
    return result


class RouteFile(object):

    def __init__(self, filename):
        self.filename = filename
        self.file_reader = read_table(filename, chunksize=1)
        self.columns = self.file_reader.get_chunk(1).columns
        for column in self.columns:
            if 'latitude' in column.lower():
                self.latitude_column_name = column
            elif 'longitude' in column.lower():
                self.longitude_column_name = column
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS
                uploaded_files
            (
                id SERIAL,
                filename TEXT,
                latitude NUMERIC,
                longitude NUMERIC,
                row JSON)''')

    def get_row(self):
        for raw_row in self.file_reader:
            row = dict()
            for key, value in raw_row.to_dict(orient='records')[0].iteritems():
                if str(value) not in ['nan', 'NULL', '']:
                    row[key] = value
            if ((self.longitude_column_name in row) and
               (self.latitude_column_name in row)):
                yield row

    def get_rows(self, limit=1000):
        file_reader = read_table(self.filename, chunksize=limit)
        for raw_rows in file_reader:
            rows = list()
            for raw_row in raw_rows.to_dict(orient='records'):
                row = dict()
                for key, value in raw_row.iteritems():
                    if str(value) not in ['nan', 'NULL', '']:
                        row[key] = value
                rows.append(row)
            yield rows

    def get_points(self, limit=1000):
        file_reader = read_table(self.filename, chunksize=limit)
        for chunk in file_reader:
            points = []
            for row in chunk.to_dict(orient='records'):
                latitude = row.get(self.latitude_column_name)
                longitude = row.get(self.longitude_column_name)
                if ((str(latitude) not in ['nan', 'NULL', '']) and
                   (str(longitude) not in ['nan', 'NULL', ''])):
                    try:
                        latitude = float(latitude)
                        longitude = float(longitude)
                        point = [latitude, longitude, [self.clean_row(row), ]]
                        points.append(point)
                    except:
                        pass
            yield points

    def clean_row(self, row):
        result = dict()
        for key, value in row.iteritems():
            if str(value).lower() not in ['nan', '', 'null', 'none']:
                result[key] = value
        return result

    def save_file(self):
        cursor = connection.cursor()
        i = 0
        for points in self.get_points():
            i += 1
            print i
            for point in points:
                cursor.execute('''
                    INSERT INTO uploaded_files
                        (filename, latitude, longitude, row)
                    VALUES
                        (%s, %s, %s, %s)
                    ''', (self.filename,
                          point[0],
                          point[1],
                          json.dumps(point[2], encoding='latin1'))

                )
        connection.commit()
