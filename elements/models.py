from django.db import models


class Project(models.Model):
    project_name = models.TextField()


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
