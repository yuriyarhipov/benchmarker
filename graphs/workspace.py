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
        self.map = []
        for point in StandartRoute([]).get_route(ws.route.id, ws.route.color):
            row_point = self.get_point_info(point)
            point['row'] = row_point
            self.points.append(point)
            color = self.check_point(self.column, row_point, self.ranges)
            if not color:
                color = point.get('color')
            self.map.append(dict(lon=point.get('lon'), lat=point.get('lat'), color=color))

        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Graphs (id SERIAL, workspace INT, graph JSON, map JSON)')
        connection.commit()
        cursor.execute('INSERT INTO graphs (workspace, graph, map) VALUES (%s, %s, %s)', (ws.id, json.dumps(self.graphs), json.dumps(self.map)))
        connection.commit()

    @staticmethod
    def get_graph(graph_id):
        cursor = connection.cursor()
        cursor.execute('SELECT graph FROM Graphs WHERE id=%s', (graph_id, ))
        if cursor.rowcount:
            return cursor.fetchall()[0][0]

    @staticmethod
    def get_map(map_id):
        cursor = connection.cursor()
        cursor.execute('SELECT map FROM Graphs WHERE id=%s', (map_id, ))
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
            value = row.get(column)
            try:
                value = float(value)
            except:
                value = 0
            for legend_range in ranges:
                range_name = '%s %s %s' % (legend_range.range_from, legend_range.range_symbol, legend_range.range_to)
                if range_name not in self.graphs:
                    self.graphs[range_name] = 0
                if self.check_legend_value(value, float(legend_range.range_from), float(legend_range.range_to), legend_range.range_symbol):
                    self.graphs[range_name] += 1
                    return legend_range.range_color



    def check_legend_value(self, value, from_value, to_value, symbol):
        if symbol == '<':
            return (from_value < value) and (value < to_value)
        elif symbol == '>':
            return (from_value > value) and (value > to_value)
        elif symbol == '<=':
            return (from_value <= value) and (value <= to_value)
        elif symbol == '>=':
            return (from_value >= value) and (value >= to_value)
