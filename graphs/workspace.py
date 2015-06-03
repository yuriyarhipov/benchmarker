import json

from models import Workspaces
from routes.route import StandartRoute
from django.db import connection

class Workspace(object):
    graph = dict(
        legend1=0,
        legend2=0,
        legend3=0,
        legend4=0
    )
    column = 'ServRxLevSub'

    def __init__(self, workspace_name):
        ws = Workspaces.objects.filter(workspace_name=workspace_name).first()
        self.workspace_name = workspace_name
        self.route = ws.route.route_name
        self.points = []

        for point in StandartRoute([]).get_route(ws.route.id):
            row_point = self.get_point_info(point)
            point['row'] = row_point
            self.points.append(point)
            self.check_point(row_point)

        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Graphs (id SERIAL, workspace INT, graph JSON)')
        connection.commit()
        cursor.execute('INSERT INTO graphs (workspace, graph) VALUES (%s, %s)', (ws.id, json.dumps(self.graph)))
        connection.commit()

    def get_point_info(self, point):
        cursor = connection.cursor()
        cursor.execute('SELECT row FROM uploaded_files WHERE (latitude=%s) AND (longitude=%s)' % (
            point.get('lat'),
            point.get('lon')
        ))
        data = cursor.fetchall()
        return data[0][0]

    def check_point(self, row):
        if 'ServRxLevSub' in row:
            value = row.get('ServRxLevSub')
            try:
                value = float(value)
            except:
                value = 0
            if self.check_legend_value(value, -50, -55, '<'):
                self.graph['legend1'] += 1
            elif self.check_legend_value(value, -50, -55, '>'):
                self.graph['legend2'] += 1

    def check_legend_value(self, value, from_value, to_value, symbol):
        if symbol == '<':
            return value < from_value
        elif symbol == '>':
            return value > to_value
        elif symbol == '<=':
            return value <= from_value
        elif symbol == '>=':
            return  value >= to_value
