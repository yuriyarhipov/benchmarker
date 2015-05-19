from django.db import models
from elements.models import Project


class RouteFile(models.Model):
    project = models.ForeignKey(Project)
    filename = models.TextField()
    filetype = models.TextField()
    module = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    columns = models.TextField()
    status = models.TextField()


class StandartRoute(models.Model):
    project = models.ForeignKey(Project)
    route_time = models.TextField()
    route_name = models.TextField()
    points_amount = models.IntegerField(default=0)
    distance = models.FloatField(default=5)
    route_files = models.TextField()
    route_distance = models.FloatField(default=0)
