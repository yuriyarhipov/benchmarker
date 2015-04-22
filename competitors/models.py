from django.db import models
from elements.models import Project


class Competitor(models.Model):
    project = models.ForeignKey(Project)
    filename = models.TextField()
