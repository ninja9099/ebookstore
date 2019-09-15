from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    def validate_email(self, attrs):
        if User.objects.filter(email=attrs, is_active=True).exists():
            raise ValidationError(_('Email is already exist'))
        return attrs

class UserReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "about_me",
            "user_type",
            "avatar"
        )

    def validate_email(self, attrs):
        if User.objects.filter(email=attrs, is_active=True).exists():
            raise ValidationError(_('Email is already exist'))
        return attrs


class PasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        p1 = attrs.get('password1')
        p2 = attrs.get('password2')
        if p1!=p2:
            raise ValidationError({'password': _('Passwords Do not match')})
        return attrs