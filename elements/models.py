from django.db import models


class Project(models.Model):
    project_name = models.TextField()


class Competitor(models.Model):
    project = models.ForeignKey(Project)
    competitor = models.TextField()
    gsm = models.BooleanField()
    wcdma = models.BooleanField()
    lte = models.BooleanField()
    future = models.TextField()
    mcc = models.TextField()
    mnc = models.TextField()
    gsm_freq = models.TextField()
    wcdma_carriers = models.TextField()
    lte_carriers = models.TextField()
    future_carriers = models.TextField()


class DataSet(models.Model):
    project = models.ForeignKey(Project)
    equipment = models.TextField()
    module = models.TextField()
    measurement_device = models.TextField()
    value = models.TextField()


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
