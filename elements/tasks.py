import json
from djcelery import celery
from django.db import connection
from geopy.distance import vincenty
from pandas import read_table
from routes.route import StandartRoute


@celery.task
def write_file_chunks(filename, project_id, module, latitude_column_name, longitude_column_name, chunk):
    cursor = connection.cursor()
    for row in chunk.to_dict(orient='records'):
        cursor.execute(
            'INSERT INTO uploaded_files (filename, project_id, module, latitude, longitude, row) VALUES (%s, %s, %s, %s, %s, %s)',(
                filename,
                project_id,
                module,
                row.get(latitude_column_name),
                row.get(longitude_column_name),
                json.dumps(json.dumps(row, encoding='latin1'))))
    connection.commit()


@celery.task
def upload_file(filename, project_id, module):
    latitude_column_name = None
    longitude_column_name = None

    cursor = connection.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS uploaded_files (
                    id SERIAL,
                    filename TEXT,
                    project_id INT,
                    module INT,
                    latitude NUMERIC,
                    longitude NUMERIC,
                    row JSON)''')
    connection.commit()

    if '.csv' or '.txt' in filename:
        file_reader = read_table(filename, chunksize=100)
        for chunk in file_reader:
            if not latitude_column_name:
                for column in chunk.columns:
                    if 'latitude' in column.lower():
                        latitude_column_name = column
                    elif 'longitude' in column.lower():
                        longitude_column_name = column
            write_file_chunks.delay(filename, project_id, module, latitude_column_name, longitude_column_name, chunk)


@celery.task
def create_route(id_route, route_files, distance):
    points = StandartRoute(route_files).get_points(distance)
    idx = 0
    while idx < len(points):
        write_points.delay(sr.id, distance, points[idx: idx+1000])
        idx += 1000


@celery.task
def write_points(id_route, distance, rows):
    result = [rows.pop(0), ]
    for row in rows:
        status = True
        for r in result:
            if vincenty(r, row).meters < distance:
                status = False
        if status:
            result.append(row)
    cursor = connection.cursor()
    for point in result:
        cursor.execute('INSERT INTO StandartRoutes (route_id, latitude, longitude) VALUES (%s, %s, %s)', (id_route, point[0], point[1]))

    connection.commit()
