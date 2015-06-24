import json
from djcelery import celery
from django.db import connection
from geopy.distance import vincenty
from lib.files import RouteFile


def filter_row(row):
    result = dict()
    for key, value in row.iteritems():
        if str(value).lower() not in ['nan', '', 'null', 'none']:
            result[key] = value
    return result


@celery.task
def create_route(id_route, route_files, distance):
    for f in route_files:
        rf = RouteFile(f)
        for rows in rf.get_points():
            write_points.delay(id_route, distance, rows)


@celery.task
def write_points(id_route, distance, rows):
    result = [rows.pop(0), ]
    for row in rows:
        status = True
        for r in result:
            if vincenty(r[:-1], row[:-1]).meters < distance:
                status = False
        if status:
            result.append(row)

    cursor = connection.cursor()
    for point in result:
        cursor.execute(
            'INSERT INTO StandartRoutes (route_id, latitude, longitude, row) VALUES (%s, %s, %s, %s)',
            (id_route, point[0], point[1], json.dumps(filter_row(point[2]), encoding='latin1')))
    connection.commit()
