import uuid

from django.db import models
from iot.models.custom_user import User


class TubeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    is_variable = models.BooleanField(default=False)
    data_type = models.CharField(max_length=100)
    monitoring = models.BooleanField(default=False)
    interval = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    activity = models.DateTimeField()
    compare_upper_threshold = models.BooleanField(default=False)
    compare_lower_threshold = models.BooleanField(default=False)
    upper_threshold = models.FloatField(default=100)
    lower_threshold = models.FloatField(default=0)
