from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
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

    REQUIRED_FIELDS = ['user_type', 'email']

    @property
    def get_avatar(self):
        """
        returns the url of the user avatar
        :return:
        """
        try:
            return self.avatar.url
        except ValueError:
            return None

    @property
    def get_user_type(self):
        """
        takes user object
        :return: user type
        """
        return self.user_type

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
