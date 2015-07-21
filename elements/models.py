from django.db import models


class Project(models.Model):
    project_name = models.TextField()


class Tasks(models.Model):
    task_name = models.TextField()
    current = models.IntegerField()
    tasks = models.TextField()
    max_value = models.IntegerField()
    message = models.TextField()
