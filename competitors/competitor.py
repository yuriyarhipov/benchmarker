import json
from django.db import connection

from lib.excel import Excel

class Competitor(object):

    def __init__(self):
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Competitors (id SERIAL, project_id INT, competitor JSON)')
        connection.commit()

    def parse_file(self, project_id, filename):
        cursor = connection.cursor()
        data = Excel(filename).get_data()
        columns = data[0]
        data = data[1:]
        for row in data:
            competitor = dict()
            for col in columns:
                competitor[col] = row[columns.index(col)]
            if competitor.get('Competitor', '') != '':
                cursor.execute('''INSERT INTO Competitors (project_id, competitor) VALUES (%s, %s)''', (project_id, json.dumps(competitor)))
        connection.commit()

    def get_competitors(self, project_id):
        cursor = connection.cursor()
        columns = set()
        cursor.execute("SELECT competitor FROM Competitors WHERE project_id=%s" % (project_id, ))
        data = []
        for row in cursor:
            columns = columns.union(row[0].keys())
            data.append(row[0])
        columns = list(columns)
        columns.sort()
        result = []
        for competitor in data:
            row = []
            for col in columns:
                row.append(competitor[col])
            result.append(row)
        return columns, result

    def get_competitor(self, project_id, competitor_name):
        cursor = connection.cursor()
        competitor = dict()
        cursor.execute("SELECT competitor FROM Competitors WHERE project_id=%s" % (project_id, ))
        for row in cursor:
            if row[0].get('Competitor') == competitor_name:
                competitor = row[0]

        columns = competitor.keys()
        columns.sort()
        result = []
        for col in columns:
            result.append(dict(label=col, value = competitor.get(col)))
        return result

    def save_competitor(self, project_id, competitor_name, params):
        cursor = connection.cursor()
        cursor.execute("SELECT id, competitor FROM Competitors WHERE project_id=%s" % (project_id, ))
        for row in cursor:
            if row[1].get('Competitor') == competitor_name:
                competitor_id = row[0]
        cursor.execute("DELETE FROM Competitors WHERE (id=%s)", (competitor_id, ))
        cursor.execute('''INSERT INTO Competitors (project_id, competitor) VALUES (%s, %s)''', (project_id, json.dumps(params)))
        connection.commit()






