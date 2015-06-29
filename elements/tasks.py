import json
from djcelery import celery
from django.db import connection
from lib.files import RouteFile
from celery.task.control import revoke
from routes.route import StandartRoute
from routes.models import StandartRoute as SR
from geopy.distance import vincenty
from graphs.workspace import Workspace


@celery.task(ignore_result=True)
def create_route(id_route, route_files, distance):
    sr = StandartRoute(route_files)
    points = sr.route(distance)
    i = 0
    while i < len(points):
        write_points.delay(id_route, distance, points[i:i + 1000])
        i += 1000
    revoke(create_route.request.id, terminate=True)


@celery.task(ignore_result=True)
def write_points(id_route, distance, rows):
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


@celery.task(ignore_result=True)
def save_file(filename):
    rf = RouteFile(filename)
    for points in rf.get_points(1000):
        write_file_row.delay(filename, points)
    revoke(save_file.request.id, terminate=True)


@celery.task(ignore_result=True)
def write_file_row(filename, points):
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
    ws = Workspace(workspace_name)
    sr = SR.objects.filter(id=ws.route.id).first()

    cursor = connection.cursor()
    cursor.execute('''
        SELECT
            latitude,
            longitude
        FROM
            StandartRoutes
        WHERE
            route_id=%s ''', (ws.route.id, ))

    for row in cursor:
        workspace_point.delay(
            ws.ws.id,
            sr.route_files,
            ws.column,
            row[0],
            row[1])


@celery.task(ignore_result=True)
def workspace_point(workspace_id, route_files, column, latitude, longitude):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT
            row
        FROM
            uploaded_files
        WHERE
            (latitude = %s) AND
            (longitude = %s) AND
            (filename in (%s))
        ''', (latitude, longitude, route_files))
    if cursor.rowcount > 0:
        row = cursor.fetchone()[0][0]
        print column
        print row
        print row.get(column)
