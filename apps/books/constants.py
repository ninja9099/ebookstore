from apps.common.constant import GlobalConstant


class BookReadStatus(GlobalConstant):

    Started = 1
    Halfway = 2
    Finished = 3

    FieldStr = {
       Started: "Started",
       Halfway: "Halfway",
       Finished: "Finished",
    }