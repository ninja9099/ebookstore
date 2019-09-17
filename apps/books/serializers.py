from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.books.models import Book, Category
from apps.common.base_serializers import BaseSerializer

User = get_user_model()


class CategorySerializer(BaseSerializer):

    class Meta:
        model = Category
        fields = ('name', 'child_set')

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['child_set'] = CategorySerializer(many=True)
        return fields

class BookSerializer(BaseSerializer):
    rating = serializers.CharField(source='get_rating', read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "created_ts",
            "updated_ts",
            "rating",
            "name",
            "cover",
            "author",
            "published_date",
            "total_pages",
            "publisher",
            "file",
            "created_by",
            "category"
        )

    # handle many to many relation explicitly
    def create(self, validated_data):
        instance = super(BookSerializer, self).create(validated_data)
        return instance