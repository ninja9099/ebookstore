from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.books.models import Book
from apps.common.base_serializers import BaseSerializer

User = get_user_model()


class BookSerializer(BaseSerializer):

    class Meta:
        model = Book
        fields = ('__all__')