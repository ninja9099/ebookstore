from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from apps.users.serializers import UserSerializer, UserReadOnlySerializer
from rest_framework import viewsets, filters as search_filters
from rest_framework.mixins import (
    ListModelMixin as ListMixin,
    UpdateModelMixin as UpdateMixin
)
User = get_user_model()


def jwt_custom_payload(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(
            user,
            context={'request': request},
            remove_fields=[
                'user_permissions',
                'password',
                'groups'
            ]).data
    }


def index(request):
    return render(request, 'index.html')


class UserViewset(ListMixin,  UpdateMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser | IsAuthenticatedOrReadOnly,)
    filter_backends = (search_filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('first_name', 'last_name', 'username', 'email', 'about_me')
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return self.serializer_class
        return UserReadOnlySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request_data = request.data.copy()
        if 'email' in request_data.keys():
            request_data.pop('email')
        if instance.id != request.user.pk:
            raise ValidationError('Not allowed to edit other users')
        serializer = self.get_serializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

