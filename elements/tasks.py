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
            i = 0
            for row in f:
                i += 1
                data = dict()
                row = row.split('\t')
                for col in columns:
                    if row[columns.index(col)] != '':
                        data[col] = unicode(row[columns.index(col)], "ISO-8859-1")
                cursor.execute('''INSERT INTO Routes (row) VALUES (%s)''', [
                    json.dumps(data), ])
                print i
            connection.commit()




        RouteFile.objects.create(project=project,
            filename=uploaded_file,
            filetype=equipment,
            module=module,
            latitude='All-Latitude Decimal Degree',
            longitude='All-Longitude Decimal Degree')


