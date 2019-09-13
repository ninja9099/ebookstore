from apps.common.constant import GlobalConstant


class UserTypes(GlobalConstant):
    Reader = 1
    Author = 2
    Manager = 3

    FieldStr = {
        Reader: "Reader",
        Author: "Author",
        Manager: "Manager",
    }