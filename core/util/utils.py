import datetime
import os
import sys
import configparser
import holidays
import sxtwl

CONFIG_FILE = "config.ini"
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


def read_config(config_file, item_name, key=None):
    res_dict = {}
    try:
        config = configparser.ConfigParser()
        config.optionxform = lambda optionstr: optionstr
        config.read(config_file, encoding='utf-8')
        res_dict = dict(config.items(item_name))
    except Exception:
        pass
    if key is not None:
        return res_dict.get(key)
    return res_dict


def load_config(seg, key=None):
    config_default = {
        "global": {
            "db_name": "diary.db",
            "first_day_of_week": 7,
            "multi_thread": 1,
            "login_expired": 0,
        },
        "style": {
            "font": "Arial,Kaiti",
            "font_size": 18,
            "logo": "style/logo.png",
            "icon_interest": "style/interest.png",
            "icon_bill": "style/bill.png",
            "icon_note": "style/note.png",
            "icon_exit": "style/exit.png",
            "icon_imp": "style/imp.png",
            "icon_exp": "style/exp.png",
            "icon_save": "style/save.png",
            "icon_add": "style/add.png",
            "icon_del": "style/del.png",
            "icon_month": "style/month.png",
            "icon_day": "style/day.png",
            "qss": None,
        }
    }
    if os.path.isfile(CONFIG_FILE):
        val = read_config(CONFIG_FILE, seg, key)
        if val is not None and val != {}:
            return val
    if key is None:
        return config_default.get(seg)
    return config_default.get(seg, {}).get(key)


def get_path(relative_path):
    path = os.path.normpath(os.path.join(".", relative_path))
    if os.path.exists(path):
        return path
    try:
        path = os.path.join(sys._MEIPASS, relative_path)
    finally:
        return path


def load_qss(app):
    config = load_config("style")
    qss_file = config.get("qss")
    font_size = config.get("font_size")
    font = config.get("font")
    style_sheet = ""
    if qss_file is not None:
        qss_file = get_path(qss_file)
        if os.path.isfile(qss_file):
            try:
                with open(qss_file, "r", encoding="utf-8") as f:
                    style_sheet = f.read()
            except Exception as e:
                print(e.args)
    if font is not None:
        style_sheet += "\r\n*{font-family:%s;}" % font
    if font_size is not None:
        style_sheet += "\r\n*{font-size:%spx;}" % font_size
    app.setStyleSheet(style_sheet)


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
