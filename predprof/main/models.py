from django.db import models


class Tile(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    data = models.JSONField()


class Station(models.Model):
    STATION_TYPES = [("C", "Купер"), ("E", "Энгель")]
    x = models.IntegerField()
    y = models.IntegerField()
    station_type = models.CharField(max_length=1, choices=STATION_TYPES)
