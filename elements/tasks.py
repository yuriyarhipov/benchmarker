from djcelery import celery
from routes.route import StandartRoute
from django.db import connection
from geopy.distance import vincenty


@celery.task
def upload_file(filename, project_id, module):
    StandartRoute([]).save_points_to_database(filename, project_id, module)

@celery.task
def write_points(id_route, distance, rows):
    result = [rows.pop(0), ]
    for row in rows:
        status = True
        for r in result:
            if vincenty(r, row).meters < distance:
                status =False
        if status:
            result.append(row)
    cursor = connection.cursor()
    for point in result:
        cursor.execute('INSERT INTO StandartRoutes (route_id, latitude, longitude) VALUES (%s, %s, %s)', (id_route, point[0], point[1]))

    connection.commit()




