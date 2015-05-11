import re
import json
from djcelery import celery
from django.db import connection

from routes.models import RouteFile
from routes.models import StandartRoute
from routes.route import StandartRoute as SR


@celery.task
def worker(project, module, uploaded_file):
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Routes (project_id INT, filename TEXT, module TEXT, idx INTEGER, row JSON)')
    cursor.execute("DELETE FROM Routes WHERE (project_id=%s) AND (filename='%s') AND (module='%s')" % (project.id, uploaded_file, module))
    connection.commit()

    columns_pattern = re.compile('\[\S+\]')

    with open(uploaded_file) as f:
        columns_row = columns_pattern.sub('', f.readline())
        columns = columns_row.split('\t')
        if 'All-Latitude Decimal Degree' in columns:
            latitude = 'All-Latitude Decimal Degree'
        else:
            latitude = 'Latitude'

        if 'All-Longitude Decimal Degree' in columns:
            longitude = 'All-Longitude Decimal Degree'
        else:
            longitude = 'Longitude'
        for row in f:
            data = dict()
            row = row.split('\t')
            idx = row[columns.index('Index')]
            for col in columns:
                if row[columns.index(col)] != '':
                    data[col] = unicode(row[columns.index(col)], "ISO-8859-1")
            if data.get(longitude) and data.get(latitude):
                cursor.execute('''INSERT INTO Routes (project_id, filename, module, row, idx) VALUES (%s, %s, %s, %s, %s)''', [
                project.id, uploaded_file, module, json.dumps(data), idx, ])
        connection.commit()

    rf = RouteFile.objects.filter(
        project=project,
        filename=uploaded_file,
        module=module).first()
    rf.latitude = latitude
    rf.longitude = longitude
    rf.status= 'db'
    rf.save()

@celery.task
def create_standart_route(route_id):
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS StandartRoutes (route_id INT, longitude TEXT, latitude TEXT)')
    sr = StandartRoute.objects.get(id=route_id)
    route_files = sr.route_files.split(',')
    distance = sr.distance
    points, route_distance = SR(route_files).get_points(distance)
    sr.route_distance = int(route_distance)
    sr.save()
    cursor.execute('DELETE FROM StandartRoutes WHERE (route_id=%s)', (sr.id, ))
    for point in points:
        cursor.execute('INSERT INTO StandartRoutes (route_id, latitude, longitude) VALUES (%s, %s, %s)', (sr.id, point[0], point[1]))
    connection.commit()
