from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.common.base_serializers import BaseSerializer
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        only_fields = kwargs.pop('only_fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)


class UserReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","first_name","last_name","about_me", "user_type", "avatar")