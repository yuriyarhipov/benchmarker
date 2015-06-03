from django.db import models, connection
from routes.models import StandartRoute

class Legend(models.Model):
    legend_name = models.TextField()

class LegendRange(models.Model):
    legend = models.ForeignKey(Legend)
    range_from = models.TextField()
    range_to = models.TextField()
    range_symbol = models.TextField()
    range_color = models.TextField()

class Calculation(models.Model):
    calculation_name = models.TextField()
    equipment = models.TextField()
    technology = models.TextField()
    legend = models.ForeignKey(Legend)
    test = models.TextField()
    column = models.TextField()
    operation = models.TextField()


class Workspaces(models.Model):
    workspace_name = models.TextField()
    route = models.ForeignKey(StandartRoute)
    competitor = models.TextField()
    network = models.TextField()
    test = models.TextField()
    calculation = models.ForeignKey(Calculation)

    def graph_id(self):
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM Graphs WHERE workspace=%s', (self.id, ))
        return cursor.fetchall()[0][0]
