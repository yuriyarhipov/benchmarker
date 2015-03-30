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

