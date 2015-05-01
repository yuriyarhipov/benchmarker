import re
import json
from djcelery import celery
from django.db import connection

from lib.files import handle_uploaded_file
from lib.archive import Archive

from routes.models import RouteFile


@celery.task
def worker(project, module, equipment, uploaded_file):
    uploaded_files = Archive(handle_uploaded_file(uploaded_file)[0]).get_files()
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Routes (project_id INT, filename TEXT, module TEXT, row JSON)')
    connection.commit()

    columns_pattern = re.compile('\[\S+\]')

    for uploaded_file in uploaded_files:
        RouteFile.objects.filter(project=project, filename=uploaded_file, module=module).delete()
        with open(uploaded_file) as f:
            columns_row = columns_pattern.sub('', f.readline())
            columns = columns_row.split('\t')
            for row in f:
                data = dict()
                row = row.split('\t')
                for col in columns:
                    if row[columns.index(col)] != '':
                        data[col] = unicode(row[columns.index(col)], "ISO-8859-1")
                cursor.execute('''INSERT INTO Routes (project_id, filename, module, row) VALUES (%s, %s, %s, %s)''', [
                    project.id, uploaded_file, module, json.dumps(data), ])
            connection.commit()

        if 'All-Latitude Decimal Degree' in columns:
            latitude = 'All-Latitude Decimal Degree'
        else:
            latitude = 'Latitude'

        if 'All-Longitude Decimal Degree' in columns:
            longitude = 'All-Longitude Decimal Degree'
        else:
            longitude = 'Longitude'

        RouteFile.objects.create(project=project,
            filename=uploaded_file,
            filetype=equipment,
            module=module,
            latitude=latitude,
            longitude=longitude)


