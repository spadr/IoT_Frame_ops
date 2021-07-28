from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import os

def get_photo_upload_path(self, filename):
    root_path = "user/photos"
    user_path = root_path + "/" + self.user.username
    user_dir_path = settings.MEDIA_ROOT + "/" + user_path
    if not os.path.exists(user_dir_path):
        os.mkdir(user_dir_path)
    return user_path + "/" + filename


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alive_monitoring = models.BooleanField(default=False)
    send_message_to_email = models.BooleanField(default=False)
    line_token = models.CharField(max_length=100, blank=True, null=True)
    send_message_to_line = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class DeviceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    monitoring = models.BooleanField(default=False)
    interval = models.IntegerField(null=True)
    activity = models.DateTimeField()



class NumberModel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    time = models.DateTimeField()
    data = models.FloatField(null=True)



class ImageModel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    time = models.DateTimeField()
    filename = models.CharField('File Name', max_length=100)
    image = models.ImageField('Photo', upload_to=get_photo_upload_path)