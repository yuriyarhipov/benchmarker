import json
from djcelery import celery
from django.db import connection
from geopy.distance import vincenty
from lib.files import RouteFile
from celery.task.control import revoke


@celery.task(ignore_result=True)
def create_route(id_route, route_files, distance):
    for f in route_files:
        rf = RouteFile(f)
        for rows in rf.get_points(1000):
            write_points.delay(id_route, distance, rows)
    revoke(create_route.request.id, terminate=True)


@celery.task(ignore_result=True)
def write_points(id_route, distance, rows):
    result = [rows.pop(0), ]
    for row in rows:
        status = True
        for r in result:
            if vincenty(r[:-1], row[:-1]).meters < distance:
                status = False
                result[result.index(r)][2].append(r[2])
                break

        if status:
            result.append(row)

    cursor = connection.cursor()
    for point in result:
        cursor.execute('''
            INSERT INTO
                StandartRoutes (
                    route_id,
                    latitude,
                    longitude,
                    row)
            VALUES (%s, %s, %s, %s)''', (
            id_route,
            point[0],
            point[1],
            json.dumps(point[2], encoding='latin1')))
    connection.commit()
    revoke(write_points.request.id, terminate=True)


@celery.task(ignore_result=True)
def save_file(filename):
    rf = RouteFile(filename)
    rf.save_file()
    revoke(save_file.request.id, terminate=True)
