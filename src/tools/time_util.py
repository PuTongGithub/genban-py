from datetime import datetime

ONE_MIN_SECOND = 60
ONE_HOUR_SECOND = 60 * ONE_MIN_SECOND
ONE_DAY_SECOND = 24 * ONE_HOUR_SECOND

STR_FORMATTER_NO_MARKS = "%Y%m%d%H%M"

def getNow():
    return datetime.now()

def getTimestamp():
    return getNow().timestamp()

def getNowStr(formatter):
    return getNow().strftime(formatter)
