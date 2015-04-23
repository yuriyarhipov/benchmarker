from django.db import models
from elements.models import Project


class RouteFile(models.Model):
    project = models.ForeignKey(Project)
    filename = models.TextField()
    filetype = models.TextField()
    module = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()


class StandartRoute(models.Model):
    project = models.ForeignKey(Project)
    route_name = models.TextField()
    distance = models.FloatField(default=5)
    route_files = models.TextField()
