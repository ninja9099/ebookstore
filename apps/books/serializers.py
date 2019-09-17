from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.books.models import Book, Category
from apps.common.base_serializers import BaseSerializer


User = get_user_model()


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name','parent')
    # removed due to schema generation going infinite
    # def get_fields(self):
    #     fields = super(CategorySerializer, self).get_fields()
    #     fields['child_set'] = CategorySerializer(many=True)
    #     return fields

class BookSerializer(BaseSerializer):
    rating = serializers.CharField(source='get_rating', read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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