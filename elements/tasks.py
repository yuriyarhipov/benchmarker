import json
from djcelery import celery
from django.db import connection
from lib.files import RouteFile
from celery.task.control import revoke
from routes.route import StandartRoute
from geopy.distance import vincenty
from graphs.workspace import Workspace
from pandas import read_table


@celery.task(ignore_result=True)
def create_route(id_route, route_files, distance):
    sr = StandartRoute(route_files)
    points = sr.route(distance)
    i = 0
    while i < len(points):
        write_points.delay(id_route, distance, points[i:i + 1000])
        i += 1000
        break
    revoke(create_route.request.id, terminate=True)


@celery.task(bind=True)
def write_points(self, id_route, distance, rows):
    result = [rows[0], ]
    points = rows[1:]
    for p in points:
        status = True
        for rp in result:
            if vincenty(p, rp).meters < distance:
                status = False
                break
        if status:
            result.append(p)
    rows = result
    cursor = connection.cursor()
    sql_points = []
    for point in rows:
        sql_points.append(cursor.mogrify('(%s, %s, %s)', (
            id_route,
            point[0],
            point[1])))

    cursor.execute('''
        INSERT INTO
            StandartRoutes (
                route_id,
                latitude,
                longitude)
        VALUES %s''' % ','.join(sql_points))
    cursor.close()
    print self.request
    revoke(write_points.request.id, terminate=True)


@celery.task(ignore_result=True)
def save_file(filename):
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
    cursor.close()
    latitude_column_name = None
    longitude_column_name = None
    file_reader = read_table(filename, chunksize=1)
    columns = file_reader.get_chunk(1).columns
    for column in columns:
        if 'latitude' in column.lower():
            latitude_column_name = column
        elif 'longitude' in column.lower():
            longitude_column_name = column

    file_reader = read_table(filename, chunksize=100)
    ids = []
    for chunk in file_reader:
        task_worker = write_file_row.delay(filename, chunk, latitude_column_name, longitude_column_name)
        ids.append(task_worker.id)
        if len(ids) > 10:
            break

    print len(ids)
    revoke(save_file.request.id, terminate=True)


@celery.task(bind=True)
def write_file_row(self, filename, chunk, latitude_column_name, longitude_column_name):
    return
    points = []
    for row in chunk.to_dict(orient='records'):
        latitude = row.get(latitude_column_name)
        longitude = row.get(longitude_column_name)
        if ((str(latitude) not in ['nan', 'NULL', '']) and
           (str(longitude) not in ['nan', 'NULL', ''])):
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                point = [latitude, longitude, [RouteFile.clean_row(row), ]]
                points.append(point)
            except:
                pass

    cursor = connection.cursor()
    sql_points = []
    for point in points:
        sql_points.append(cursor.mogrify('(%s, %s, %s, %s)', (
            filename,
            point[0],
            point[1],
            json.dumps(point[2], encoding='latin1'))))

    cursor.execute('''
        INSERT INTO uploaded_files
            (filename, latitude, longitude, row)
        VALUES %s''' % ','.join(sql_points))
    cursor.close()
    revoke(write_file_row.request.id, terminate=True)


@celery.task(ignore_result=True)
def create_workspace(workspace_name):
    Workspace(workspace_name)
