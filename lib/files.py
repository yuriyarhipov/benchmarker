from django.conf import settings
from django.db import connection
from pandas import read_table
import json
import mmap
from geopy.distance import vincenty


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


def map_count(filename):
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines


def get_dict_row(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            yield row

class RouteFile(object):

    def __init__(self, filename):
        self.filename = filename
        self.filename = filename
        self.file_reader = self.get_row()
        self.columns = self.file_reader.next()
        for column in self.columns:
            if 'latitude' in column.lower():
                self.latitude_column_name = column
            elif 'longitude' in column.lower():
                self.longitude_column_name = column

    def get_row(self):
        with open(self.filename, "rb") as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                yield row[0].split('\t')




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

    @staticmethod
    def clean_row(row):
        result = dict()
        for key, value in row.iteritems():
            if str(value).lower() not in ['nan', '', 'null', 'none']:
                result[key] = value
        return result

    @staticmethod
    def slow_distance(sort_points, distance):
        i = 0
        while i < len(sort_points):
            points = sort_points[i:i + 100]
            i += 100
            result = [points[0], ]
            points = points[1:]
            for p in points:
                status = True
                for rp in result:
                    if vincenty(p[:-1], rp[:-1]).meters < distance:
                        status = False
                        break
                if status:
                    result.append(p)
        return result
