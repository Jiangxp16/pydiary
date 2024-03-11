import datetime
import os
import sys
import configparser
from lunardate import LunarDate

CONFIG_FILE = "config.ini"
num_latin = '0123456789'
num_chs = '〇一二三四五六七八九'
trans_latin_to_chs = str.maketrans(num_latin, num_chs)


def solar_to_lunar(solar_date: datetime.date):
    lunar_date = LunarDate.fromSolarDate(solar_date.year, solar_date.month, solar_date.day)
    return lunar_date


def lunar_tostring(lunar_date: LunarDate):
    year = lunar_date.year
    month = lunar_date.month
    day = lunar_date.day
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

    return "%s年%s月%s" % (year_chs, month_chs, day_chs)


def read_config(config_file, item_name, key=None):
    res_dict = {}
    try:
        config = configparser.ConfigParser()
        config.optionxform = lambda optionstr: optionstr
        config.read(config_file, encoding='utf-8')
        res_dict = dict(config.items(item_name))
    except Exception as e:
        print(e.args)
        print('Failed reading config_file: %s.' % config_file)
    if key is not None:
        return res_dict.get(key)
    return res_dict


def load_config(seg, key=None):
    config_default = {
        "global": {
            "db_name": "diary.db",
            "first_day_of_week": 7,
        },
        "style": {
            "logo": "style/logo.png",
            "font": "Times New Roman,Kaiti",
            "font_size": 18,
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
