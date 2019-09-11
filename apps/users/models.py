from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.users.constants import UserTypes


def get_image_path(instance, filename):
    """
    method to create separate folder for each user
    :param instance:
    :param filename:
    :return: file_path
    """
    return 'user_{0}/{1}'.format(instance.id, filename)


class User(AbstractUser):
    about_me = models.TextField(max_length=500, blank=True)
    user_type = models.IntegerField(choices=UserTypes.get_choices())
    avatar = models.ImageField(upload_to=get_image_path, null=True, blank=True)