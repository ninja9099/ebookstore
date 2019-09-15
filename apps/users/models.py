import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import BasePermission

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


class IsReader(BasePermission):
    message = 'Only reader can perform this action'

    def has_permission(self, request, view):
        return request.user.user_type == UserTypes.Reader


class IsAuthor(BasePermission):
    message = 'Only Author can perform the action.'

    def has_permission(self, request, view):
        return request.user.user_type == UserTypes.Author

    def has_object_permission(self, request, view, obj):
        """ checks if book is uploaded by author is the same who is editing"""
        return True


class EmailVerificationTokens(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'eb_email_tokens'
        verbose_name_plural = 'Email verification Tokens'

    def __str__(self):
        return str(self.user)