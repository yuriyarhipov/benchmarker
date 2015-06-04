from django.db import models
from elements.models import Project


class DataSet(models.Model):
    project = models.ForeignKey(Project)
    dataset_name = models.TextField()


class PerformanceTest(models.Model):
    test_name = models.TextField()