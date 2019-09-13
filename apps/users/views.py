from django.shortcuts import render

# Create your views here.
from apps.users.serializers import UserSerializer


def jwt_custom_payload(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }