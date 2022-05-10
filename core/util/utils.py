import datetime
import os
import sys
import holidays
import sxtwl

num_latin = '0123456789'
num_chs = '〇一二三四五六七八九'
trans_latin_to_chs = str.maketrans(num_latin, num_chs)
JQ_LIST = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
           "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
           "立冬", "小雪", "大雪"]


def lunar_string(solar_date):
    date = sxtwl.fromSolar(solar_date.year, solar_date.month, solar_date.day)
    year = date.getLunarYear()
    month = date.getLunarMonth()
    day = date.getLunarDay()
    jq_index = date.getJieQi()
    jq = None if jq_index > len(JQ_LIST) - 1 or jq_index < 0 else JQ_LIST[jq_index]

    year_chs = str(year).translate(trans_latin_to_chs)
    month_chs = str(month).translate(trans_latin_to_chs)
    day_chs = str(day).translate(trans_latin_to_chs)

    if len(month_chs) == 2:
        month_chs = "十" + month_chs[1]

    if len(day_chs) == 2:
        if day_chs[0] == "一":
            day_chs = "十" + day_chs[1]
        elif day_chs[0] == "二":
            day_chs = "二十" + day_chs[1]
        elif day_chs[0] == "三":
            day_chs = "三十" + day_chs[1]
        if day_chs[-1] == "〇":
            day_chs = day_chs[:-1]

    if len(day_chs) == 1:
        day_chs = "初" + day_chs

    res = "%s年%s月%s" % (year_chs, month_chs, day_chs)
    if jq:
        res += " " + jq
    return res


def get_path(relative_path):
    path = os.path.normpath(os.path.join(".", relative_path))
    if os.path.exists(path):
        return path
    try:
        path = os.path.join(sys._MEIPASS, relative_path)
    finally:
        return path


def get_holiday(date: datetime.date, loc):
    holiday_dict = holidays.CountryHoliday(loc, years=date.year)
    return holiday_dict.get(date, None)


def date2int(date: datetime.date, include_day=True):
    if include_day:
        return date.year * 10000 + date.month * 100 + date.day
    return date.year * 100 + date.month


def int2date(x: int):
    return datetime.date(int(x / 10000), int((x % 10000) / 100), int(x % 100))


def get_last_day(year, month):
    day_last = datetime.date(year, month, 28)
    while (day_last + datetime.timedelta(days=1)).month == day_last.month:
        day_last = day_last + datetime.timedelta(days=1)
    return day_last
