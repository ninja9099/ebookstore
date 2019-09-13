

class GlobalConstant(object):

    class Meta:
        abstract = True

    FieldStr = {}
    @classmethod
    def get_choices(cls):
        return cls.FieldStr.items()