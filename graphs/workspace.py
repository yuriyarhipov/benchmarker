import json

from models import Workspaces, LegendRange
from routes.route import StandartRoute
from django.db import connection

class Workspace(object):
    column = 'ServRxLevSub'

    def __init__(self, workspace_name):
        ws = Workspaces.objects.filter(workspace_name=workspace_name).first()
        self.workspace_name = workspace_name
        self.route = ws.route.route_name
        self.points = []
        self.legend = ws.calculation.legend
        self.ranges = LegendRange.objects.filter(legend=self.legend)
        self.column = ws.calculation.column
        self.graphs = dict()
        for point in StandartRoute([]).get_route(ws.route.id):
            row_point = self.get_point_info(point)
            point['row'] = row_point
            self.points.append(point)
            self.check_point(self.column, row_point, self.ranges)

        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Graphs (id SERIAL, workspace INT, graph JSON)')
        connection.commit()
        cursor.execute('INSERT INTO graphs (workspace, graph) VALUES (%s, %s)', (ws.id, json.dumps(self.graphs)))
        connection.commit()

    @staticmethod
    def get_graph(graph_id):
        cursor = connection.cursor()
        cursor.execute('SELECT graph FROM Graphs WHERE id=%s', (graph_id, ))
        if cursor.rowcount:
            return cursor.fetchall()[0][0]

    def get_point_info(self, point):
        cursor = connection.cursor()
        cursor.execute('SELECT row FROM uploaded_files WHERE (latitude=%s) AND (longitude=%s)' % (
            point.get('lat'),
            point.get('lon')
        ))
        data = cursor.fetchall()
        return data[0][0]

    def check_point(self, column, row, ranges):
        if column in row:
            value = row.get('ServRxLevSub')
            try:
                value = float(value)
            except:
                value = 0
            for range in ranges:
                range_name = '%s %s %s' % (range.range_from, range.range_symbol, range.range_to)
                if range_name not in self.graphs:
                    self.graphs[range_name] = 0
                if self.check_legend_value(value, float(range.range_from), float(range.range_to), range.range_symbol):
                    self.graphs[range_name] += 1

    def check_legend_value(self, value, from_value, to_value, symbol):
        if symbol == '<':
            return (from_value < value) and (value < to_value)
        elif symbol == '>':
            return (from_value > value) and (value > to_value)
        elif symbol == '<=':
            return (from_value <= value) and (value <= to_value)
        elif symbol == '>=':
            return (from_value >= value) and (value >= to_value)
