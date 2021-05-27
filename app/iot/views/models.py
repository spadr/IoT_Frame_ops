from django.db import models

# Create your models here.

class IotModel(models.Model):
    token = models.CharField(max_length=100)
    device = models.TextField()
    time = models.CharField(max_length=50)
    content = models.TextField()