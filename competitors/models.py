from django.db import models
from elements.models import Project

class CompetitorFields(models.Model):
    field_name = models.TextField()
    field_type = models.TextField()