from django.db import models
from elements.models import Project

class Equipment(models.Model):
    project = models.ForeignKey(Project)
    equipment_name = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()