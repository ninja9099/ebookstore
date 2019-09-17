from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters as search_filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.mixins import (
ListModelMixin as ListMixin,
UpdateModelMixin as UpdateMixin,
RetrieveModelMixin as RetrieveMixin,
CreateModelMixin as CreateMixin,
DestroyModelMixin as DeleteMixin

)
from rest_framework.response import Response

from apps.books.models import Book, Category
from apps.books.serializers import BookSerializer, CategorySerializer
from apps.users.permissions import IsAdminOrOwner


class CategoryViewSet(ListMixin, RetrieveMixin, CreateMixin, UpdateMixin, viewsets.GenericViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUser,)
    filter_backends = (search_filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name', 'slug')


class BookViewSet(ListMixin, RetrieveMixin,DeleteMixin, CreateMixin, UpdateMixin, viewsets.GenericViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUser | IsAuthenticatedOrReadOnly,)
    filter_backends = (search_filters.SearchFilter, DjangoFilterBackend,)
    filterset_fields = ['category', 'author', 'published_date', 'slug']
    search_fields = ('name', 'author__username', 'category__name', 'publisher')


    def get_permissions(self):
        permission_classes = [IsAuthenticatedOrReadOnly,]
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly, ]
        if self.action == 'update':
            permission_classes =  [IsAdminOrOwner, ]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = BookSerializer(instance=obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)