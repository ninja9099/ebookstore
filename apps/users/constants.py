

class UserTypes:
    Reader = 1
    Author = 2
    Manager = 3

    FieldStr = {
        Reader: "Reader",
        Author: "Author",
        Manager: "Manager",
    }
    @classmethod
    def get_choices(cls):
        return cls.FieldStr.items()