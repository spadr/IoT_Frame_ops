from django.db import models

# Create your models here.

class IotModel(models.Model):
    long_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    time = models.DateTimeField()
    channel = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    data = models.TextField()