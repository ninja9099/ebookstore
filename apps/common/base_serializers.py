from rest_framework import serializers


def get_user_label(user, always_show_username=False):
    name = user.get_full_name()
    username = user.username
    if not always_show_username:
        return name or username

    return name and name != username and '%s (%s)' % (name, username) or username


class BaseSerializer(serializers.ModelSerializer):
    created_ts = serializers.ReadOnlyField()
    updated_ts = serializers.ReadOnlyField()

    def to_representation(self, instance):
        ret = super(BaseSerializer, self).to_representation(instance)
        try:
            if 'created_by' in ret.keys():
                ret['created_by'] = get_user_label(user=instance.created_by)
            if 'updated_by' in ret.keys():
                ret['updated_by'] = get_user_label(user=instance.updated_by)
        except Exception as ex:
            pass
        return ret
