import pandas as pd
import time


def unixTimeMillis(dt):
    """Convert datetime to unix timestamp"""
    return int(time.mktime(dt.timetuple()))


def unixToDatetime(unix):
    """Convert unix timestamp to datetime."""
    return pd.to_datetime(unix, unit="s")


def getMarks(start, end, daterange, Nth=100):
    """Returns the marks for labeling.
    Every Nth value will be used.
    """

    result = {}
    for i, date in enumerate(daterange):
        if i % Nth == 1:
            # Append value to dict
            result[unixTimeMillis(date)] = str(date.strftime("%Y-%m-%d"))

    return result
