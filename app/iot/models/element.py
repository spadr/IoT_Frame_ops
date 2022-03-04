from django.db import models
from iot.models.tube import TubeModel
import uuid


class NumberModel(models.Model):
    tube = models.ForeignKey(TubeModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    time = models.DateTimeField()
    value = models.FloatField(null=True)


class BooleanModel(models.Model):
    tube = models.ForeignKey(TubeModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    time = models.DateTimeField()
    value = models.BooleanField(null=True)


class CharModel(models.Model):
    tube = models.ForeignKey(TubeModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    time = models.DateTimeField()
    value = models.CharField(max_length=100, null=True)
