import json

from django.db import connection

from models import DataSet
from lib.excel import Excel


class Datasets(object):

    def __init__(self):
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Datasets (id INT, project_id INT, dataset JSON)')

    def save_dataset(self, dataset_name, project_id, filename):
        ds = DataSet.objects.create(project_id=project_id, dataset_name=dataset_name)
        data = Excel(filename).get_data()
        columns = data[0]
        data = data[1:]
        dataset_json = []

        for row in data:
            row_json = dict()
            for col in columns:
                row_json[col] = row[columns.index(col)]
            dataset_json.append(row_json)

        cursor = connection.cursor()
        cursor.execute('''INSERT INTO Datasets (id, project_id, dataset) VALUES (%s, %s, %s);''', (ds.id, project_id, json.dumps(dataset_json)))
        connection.commit()

    def get_dataset(self, dataset_id):
        cursor = connection.cursor()
        cursor.execute('SELECT dataset FROM Datasets WHERE (id=%s)', (dataset_id, ))
        columns = []
        data = []
        dataset = cursor.fetchall()[0][0]
        for row in dataset:
            columns.extend(row.keys())
            data.append(row)
        columns = set(columns)
        columns = list(columns)
        columns.sort()
        result = []
        for ds_row in dataset:
            row = []
            for col in columns:
                row.append(ds_row.get(col))
            result.append(row)
        return columns, result

    @staticmethod
    def get_test(project_id, dataset_id=None):
        cursor = connection.cursor()
        if dataset_id:
            cursor.execute("SELECT dataset FROM datasets WHERE (project_id=%s) AND (id=%s)", (project_id, dataset_id ))
        else:
            cursor.execute("SELECT dataset FROM datasets WHERE project_id=%s", (project_id, ))

        tests = set()
        for row in cursor:
            for ds in row[0]:
                if ds.get('SPECIFIC_TEST'):
                    tests.add(ds.get('SPECIFIC_TEST'))
        tests = list(tests)
        tests.sort()
        return  tests
















