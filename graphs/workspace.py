import json
from models import Workspaces, LegendRange
from routes.route import StandartRoute
from django.db import connection


class Point(object):

    def check_value(self, value, ranges):
        for legend_range in ranges:
            try:
                range_from = float(legend_range.range_from)
                range_to = float(legend_range.range_to)
                if self.check_legend_value(
                        value,
                        range_from,
                        range_to,
                        legend_range.range_symbol):
                    return legend_range.range_color
            except:
                return

    def check_legend_value(self, value, from_value, to_value, symbol):
        if symbol == '<':
            return (from_value < value) and (value < to_value)
        elif symbol == '>':
            return (from_value > value) and (value > to_value)
        elif symbol == '<=':
            return (from_value <= value) and (value <= to_value)
        elif symbol == '>=':
            return (from_value >= value) and (value >= to_value)


class Workspace(object):

    def __init__(self, workspace_name):
        self.ws = Workspaces.objects.filter(
            workspace_name=workspace_name).first()
        self.workspace_name = workspace_name
        self.route = self.ws.route
        self.points = []
        self.legend = self.ws.calculation.legend
        self.ranges = LegendRange.objects.filter(legend=self.legend)
        self.column = self.ws.calculation.column
        self.graphs = dict()
        self.map = []
        for point in StandartRoute([]).get_route(
                self.ws.route.id,
                self.ws.route.color):
            row_point = self.get_point_info(point)
            if row_point:
                point['row'] = row_point
                self.points.append(point)
                value = row_point.get(self.column)
                try:
                    value = float(value)
                except:
                    value = 0
                color = Point().check_value(
                    value,
                    self.ranges)
                if not color:
                    color = point.get('color')
                self.map.append(dict(
                    lon=point.get('lon'),
                    lat=point.get('lat'),
                    color=color))

        for point in self.map:
            color = point.get('color')
            if color not in self.graphs:
                self.graphs[color] = 0
            self.graphs[color] += 1

        print self.graphs
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Graphs (id SERIAL, workspace INT, graph JSON, map JSON)')
        connection.commit()
        cursor.execute('INSERT INTO graphs (workspace, graph, map) VALUES (%s, %s, %s)', (self.ws.id, json.dumps(self.graphs), json.dumps(self.map)))
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
        print 'SELECT map FROM Graphs WHERE id=%s' % (map_id, )
        if cursor.rowcount:
            return cursor.fetchall()[0][0]

    def get_point_info(self, point):
        cursor = connection.cursor()
        cursor.execute('SELECT row FROM uploaded_files WHERE (latitude=%s) AND (longitude=%s)' % (
            point.get('lat'),
            point.get('lon')
        ))
        if cursor.rowcount == 0:
            return
        data = cursor.fetchone()
        return data[0][0]
