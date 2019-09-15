import logging

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render, render_to_response
from django.utils.translation import ugettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.users.functions import get_verification_email_context, send_verification_email
from apps.users.models import EmailVerificationTokens
from apps.users.permissions import IsAdminOrIsSelf
from apps.users.serializers import UserSerializer, UserReadOnlySerializer, PasswordSerializer
from rest_framework import viewsets, filters as search_filters, status
from rest_framework.mixins import (
    ListModelMixin as ListMixin,
    CreateModelMixin as CreateMixin,
    UpdateModelMixin as UpdateMixin
)

logger = logging.getLogger('api')

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


    @action(detail=True, methods=['put'], permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password1'])
            user.save()
            return Response({'message': _('Password has been set successfully')})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser | IsAuthenticated| IsAdminOrIsSelf]
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
        if 'username' in request_data.keys():
            request_data.pop('username')
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
            logger.debug('Creating user with data:\n {}'.format(request.data))
            user.set_password(password_serializer.data['password1'])
            context = get_verification_email_context(user, request.data['email'])
            try:
                res = send_verification_email(context=context)
            except Exception as e:
                # pass the request so that user can resend the email if sending emails fails
                # due to any reason
                logger.error("Error {} Occurred during email sending process".format(str(e)))
                pass
            user.is_active =False
            user.save()
            logger.debug('User Created successfully with id :\n {}'.format(user.id))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # to get user id for sending emails  for verification email
    def perform_create(self, serializer):
        return serializer.save()


def verify_email(request):
    token = request.GET.get('token')
    user = request.GET.get('user')
    try:
        logger.info("Request to verify the email from user: %s" % user)
        user = User.objects.get(username=user)
        email_token = EmailVerificationTokens.objects.get(key=token, is_active=True)
        email_users = User.objects.filter(
            email=user.email,
            is_active=True).exclude(Q(id=user.id))
        if email_users.count():
            return render_to_response(
                'emails/verify_email_error.html',
                {
                    'error': _('Email address already exist.')
                }
            )
        if email_token.user == user:
            inst = email_token.user
            inst.is_active = True
            inst.save()
            logger.info('User {}  has been activated successfully'.format(inst.username))
            email_token.is_active = False
            email_token.save()
            logger.info('Sending welcome email to %s ' % user)
            # TODO code for welcome email
            return render_to_response(
                'emails/verify_email_success.html',
                {
                    'message': _('Congratulations! Your Email address has been \
                    Verified. Enjoy your  free reading at  E-bookstore')}
            )
        else:
            return render_to_response(
                'emails/verify_email_error.html',
                {
                    'error': _('Invalid activation link')
                }
            )

    except EmailVerificationTokens.DoesNotExist:
        return render_to_response(
            'emails/verify_email_error.html',
            {
                'error': _('Activation link is expired')
            }
        )

    except:
        return render_to_response(
            'emails/verify_email_error.html',
            {
                'error': _('Something has gone Wrong! Please try  again')
            }
        )