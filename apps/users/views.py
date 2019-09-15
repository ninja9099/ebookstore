from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.users.serializers import UserSerializer, UserReadOnlySerializer, PasswordSerializer
from rest_framework import viewsets, filters as search_filters, status
from rest_framework.mixins import (
    ListModelMixin as ListMixin,
    CreateModelMixin as CreateMixin,
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


class UserViewset(ListMixin,CreateMixin, UpdateMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser | IsAuthenticatedOrReadOnly,)
    filter_backends = (search_filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('first_name', 'last_name', 'username', 'email', 'about_me')
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser | IsAuthenticated]
        return [permission() for permission in permission_classes]


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
            raise ValidationError(_('Not allowed to update other users'))
        serializer = self.get_serializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.serializer_class = UserSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid(raise_exception=True):
            user = self.perform_create(serializer)
            user.set_password(password_serializer.data['password1'])
            user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

