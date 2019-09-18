import logging

from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters as search_filters, status
from rest_framework.decorators import api_view, permission_classes
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

from apps.books.models import Book, Category, BookReview
from apps.books.serializers import BookSerializer, CategorySerializer, BookReviewSerializer
from apps.users.permissions import IsAdminOrOwner

logger = logging.getLogger('api')
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




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def book_review(request, book_id=None):
    try:
        if request.method =='GET':
            paginator = LimitOffsetPagination()
            book = Book.objects.get(pk=book_id)
            logger.info('Request  to get reviews of book {}'.format(book.name))
            queryset = BookReview.objects.filter(book__id=book_id).order_by('-id') or None
            if queryset:
                res_queryset = paginator.paginate_queryset(queryset, request)
                serializer = BookReviewSerializer(instance=res_queryset, many=True)
                return paginator.get_paginated_response(serializer.data)
            return Response([],status=status.HTTP_200_OK)
        logger.info('User {} request to update the review of book'.format(request.user))
        request_data = request.data.copy()
        serializer = BookReviewSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            {'message': _("Response recorded successfully")},
            status=status.HTTP_201_CREATED
        )
    except Book.DoesNotExist:
        logger.critical('Book with request id: {} not Found'.format(book_id))
        return Response(
            {'message': _("Book Not Found")},
            status=status.HTTP_404_NOT_FOUND
        )