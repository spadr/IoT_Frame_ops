import os
import uuid

from django.db import models
from iot.models.tube import TubeModel


class IntModel(models.Model):
    tube = models.ForeignKey(TubeModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    time = models.DateTimeField(null=False)
    value = models.IntegerField(null=False)


class FloatModel(models.Model):
    tube = models.ForeignKey(TubeModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    time = models.DateTimeField(null=False)
    value = models.FloatField(null=False)


class BooleanModel(models.Model):
    tube = models.ForeignKey(TubeModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    time = models.DateTimeField(null=False)
    value = models.BooleanField(null=False)


class CharModel(models.Model):
    tube = models.ForeignKey(TubeModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    time = models.DateTimeField(null=False)
    value = models.CharField(max_length=100, null=False)