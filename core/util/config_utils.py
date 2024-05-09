import os
import configparser


def read_config(config_file, item_name=None, key=None):
    res_dict = {}
    try:
        config = configparser.ConfigParser()
        config.optionxform = lambda optionstr: optionstr
        config.read(config_file, encoding='utf-8')
        if item_name is not None:
            res_dict = dict(config.items(item_name))
        else:
            res_dict = dict(config.items())
            for item in res_dict:
                res_dict[item] = dict(res_dict[item])
    except Exception:
        pass
    if key is not None:
        return res_dict.get(key)
    return res_dict


config = {
    "global": {
        "db_name": "diary.db",
        "first_day_of_week": 7,
        "multi_thread": 1,
        "login_expired": 0,
        "hide_on_startup": 0,
        "language": "en",
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
CONFIG_FILE = "config.ini"
if os.path.isfile(CONFIG_FILE):
    config_personalize = read_config(CONFIG_FILE)
    for seg in config_personalize:
        if seg in config:
            config[seg].update(config_personalize[seg])


def load_config(seg, key=None):
    val = config.get(seg, {})
    if key is not None:
        val = val.get(key)
    return val
