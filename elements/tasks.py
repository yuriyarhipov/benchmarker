import json
import time
import csv
from os.path import basename

from djcelery import celery
from django.db import connection
from lib.files import RouteFile, map_count, get_dict_row
from celery.task.control import revoke
from routes.route import StandartRoute
from routes.models import StandartRoute as SR
from geopy.distance import vincenty
from graphs.workspace import Workspace
from celery.result import AsyncResult
from elements.models import Tasks


@celery.task(ignore_result=True)
def create_route(id_route, route_files, distance):
    route_name = SR.objects.get(id=id_route).route_name
    Tasks.objects.filter(task_name=route_name).delete()
    task = Tasks.objects.create(
        task_name=route_name,
        current=1,
        message='creating...')
    sr = StandartRoute(route_files)
    points = sr.route(distance)
    Tasks.objects.filter(id=task.id).update(current=5)
    i = 0
    ids = []
    while i < len(points):
        task_worker = write_points.delay(id_route, distance, points[i:i + 1000])
        ids.append(task_worker.id)
        i += 1000

    total = len(ids)
    while len(ids) > 5:
        for task_id in ids:
            if AsyncResult(task_id).ready():
                ids.remove(task_id)
        time.sleep(5)
        current = total - len(ids)
        value = float(current) / float(total) * 100
        Tasks.objects.filter(id=task.id).update(
            current=int(value))
    task.delete()
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
    revoke(write_points.request.id, terminate=True)


@celery.task(bind=True)
def save_file(self, filename):
    Tasks.objects.filter(task_name=basename(filename)).delete()
    task = Tasks.objects.create(
        task_name=basename(filename),
        current=0,
        tasks='',
        message='Uploading..')

    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS
                uploaded_files
            (
                id SERIAL,
                filename TEXT,
                ms TEXT,
                latitude NUMERIC,
                longitude NUMERIC,
                row JSON)''')

    cursor.execute('''
            DELETE FROM
                uploaded_files
            WHERE
                filename=%s''', (filename, ))

    cursor.close()
    chunk = []
    ids = []
    row_count = map_count(filename)
    with open(filename, "rb") as csvfile:
        datareader = csv.DictReader(csvfile, delimiter='\t')
        columns = datareader.fieldnames
        latitude_column_name = None
        longitude_column_name = None
        for column in columns:
            if 'latitude' in column.lower():
                latitude_column_name = column
            elif 'longitude' in column.lower():
                longitude_column_name = column
        i = 0
        for row in datareader:
            i += 1
            chunk.append(row)
            if len(chunk) == 1000:
                value = float(i) / float(row_count) * 100
                Tasks.objects.filter(id=task.id).update(
                    current=int(value),
                    message='File processing..')
                task_worker = write_file_row.delay(
                    filename,
                    chunk,
                    latitude_column_name,
                    longitude_column_name)
                ids.append(task_worker.id)
                chunk = []

    Tasks.objects.filter(id=task.id).update(
        current=int(0),
        tasks=','.join(ids),
        message='Writing..')
    revoke(save_file.request.id, terminate=True)


@celery.task(bind=True)
def write_file_row(self,
                   filename,
                   chunk,
                   latitude_column_name,
                   longitude_column_name):
    points = []
    for row in chunk:
        latitude = row.get(latitude_column_name)
        longitude = row.get(longitude_column_name)
        if ((str(latitude) not in ['nan', 'NULL', '']) and
           (str(longitude) not in ['nan', 'NULL', ''])):
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                point = [latitude, longitude, RouteFile.clean_row(row)]
                points.append(point)
            except:
                pass

    cursor = connection.cursor()
    sql_points = []
    for point in points:
        sql_points.append(cursor.mogrify('(%s, %s, %s, %s, %s)', (
            filename,
            point[2].get('MS'),
            point[0],
            point[1],
            json.dumps([point[2], ], encoding='latin1'))))

    cursor.execute('''
        INSERT INTO uploaded_files
            (filename, ms, latitude, longitude, row)
        VALUES %s''' % ','.join(sql_points))
    cursor.close()
    revoke(write_file_row.request.id, terminate=True)


@celery.task(ignore_result=True)
def create_workspace(workspace_name):
    Workspace(workspace_name)
