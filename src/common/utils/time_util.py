from datetime import datetime
import time

ONE_MIN_SECOND = 60
ONE_HOUR_SECOND = 60 * ONE_MIN_SECOND
ONE_DAY_SECOND = 24 * ONE_HOUR_SECOND

STR_FORMATTER_NO_MARKS = "%Y%m%d%H%M%S"
STR_FORMATTER_WITH_MARKS = "%Y-%m-%d %H:%M:%S"
STR_FORMATTER_DATE_NO_MARKS = "%Y%m%d"

def getNow():
    return datetime.now()

def getTimestamp() -> int:
    return int(time.time())

def getYesterdayTimestamp() -> int:
    return getTimestamp() - ONE_DAY_SECOND

def getNowStr(formatter):
    return getNow().strftime(formatter)

def timestampToStr(timestamp: int, formatter: str) -> str:
    return datetime.fromtimestamp(timestamp).strftime(formatter)
