from django.db import models

class Legend(models.Model):
    legend_name = models.TextField()

class LegendRange(models.Model):
    legend = models.ForeignKey(Legend)
    range_from = models.TextField()
    range_to = models.TextField()
    range_symbol = models.TextField()
    range_color = models.TextField()

class Calculation(models.Model):
    calculation_name = models.TextField()
    equipment = models.TextField()
    technology = models.TextField()
    legend = models.ForeignKey(Legend)
    test = models.TextField()
    column = models.TextField()
    operation = models.TextField()

