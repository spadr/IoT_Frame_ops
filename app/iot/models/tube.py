from django.db import models
from iot.models.custom_user import User
import uuid


class TubeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    is_variable = models.BooleanField(default=False)
    data_type = models.CharField(max_length=100)
    monitoring = models.BooleanField(default=False)
    interval = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    activity = models.DateTimeField()
