import os
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from iot.models.tube import TubeModel


def user_directory_path(self, filename):
    root_path = "user/images"
    user_path = root_path + "/" + self.tube.email + "/" + self.tube.channel + "/" + self.tube.name
    user_dir_path = settings.MEDIA_ROOT + "/" + user_path
    if not os.path.exists(user_dir_path):
        os.makedirs(user_dir_path)
    return user_path + "/" + filename


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


class ImageModel(models.Model):
    tube = models.ForeignKey(TubeModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, editable=True)
    time = models.DateTimeField(null=False)
    value = models.ImageField(upload_to=user_directory_path)


@receiver(post_delete, sender=ImageModel)
def delete_file(sender, instance, **kwargs):
    instance.image.delete(False)
