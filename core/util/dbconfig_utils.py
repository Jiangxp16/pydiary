from hashlib import md5

from core.util import encrypt_utils, sql_utils, config_utils, utils
from core.util.qt_utils import show_msg, QInputDialog, QWidget, QLineEdit, QIcon, Qt
from core.util.i18n_utils import tr

sql_create = """
CREATE TABLE IF NOT EXISTS config (
    name VARCHAR(20) PRIMARY KEY DEFAULT '',
    value VARCHAR(50) NOT NULL DEFAULT ''
);
"""
sql_utils.cur.execute(sql_create)


def get_config(name):
    sql_cmd = "SELECT value FROM config WHERE `name`=?"
    rs = sql_utils.select_one(sql_cmd, (name,), False)
    if rs:
        return rs[0]
    return None


def set_config(name, value):
    if get_config(name) is not None:
        sql_cmd = "UPDATE config SET `value`=? WHERE `name`=?"
        return sql_utils.execute(sql_cmd, (value, name), False)
    sql_cmd = "INSERT INTO config (`name`, `value`) VALUES (?, ?)"
    return sql_utils.execute(sql_cmd, (name, value))


def login(max_input=5):
    widget = QWidget()
    widget.setWindowIcon(
        QIcon(utils.get_path(config_utils.load_config("style", "logo"))))
    pwd = get_config("password")
    if pwd != "":
        title = tr("Input Password")
        if pwd is None:
            title = tr("Add Password or Leave It Empty.")
        text = None
        for i in range(max_input):
            text, ok_pressed = QInputDialog.getText(widget, title,
                                                    tr("PASSWORD"), QLineEdit.Password, flags=Qt.WindowStaysOnTopHint)
            if not ok_pressed:
                return False
            if len(text) > 16:
                show_msg(tr("Password must be less than 16 characters!"), "WARNING")
                continue
            text_md5 = md5(text.encode("utf8")
                           ).hexdigest() if text != "" else text
            if pwd is None or pwd == text_md5:
                break
            show_msg(tr("Password not match!"), "WARNING")
            if i == max_input - 1:
                return False
        if pwd is None:
            set_config("password", text_md5)
        encrypt_utils.key = text
    return True


def change_pwd():
    widget = QWidget()
    widget.setWindowIcon(
        QIcon(utils.get_path(config_utils.load_config("style", "logo"))))
    pwd_old, ok_pressed = QInputDialog.getText(widget,
                                               tr("Input Old Password"),
                                               tr("OLD PASSWORD"),
                                               QLineEdit.Password,
                                               flags=Qt.WindowStaysOnTopHint)
    if not ok_pressed:
        return False
    if pwd_old != encrypt_utils.key:
        show_msg(tr("Old password not match!"), "WARNING")
        return False
    pwd_new, ok_pressed = QInputDialog.getText(widget,
                                               tr("Input New Password"),
                                               tr("NEW PASSWORD"),
                                               QLineEdit.Password,
                                               flags=Qt.WindowStaysOnTopHint)
    if not ok_pressed:
        return False
    if len(pwd_new) > 16:
        show_msg(tr("Password must be less than 16 characters!"), "WARNING")
        return False
    pwd_new_2, ok_pressed = QInputDialog.getText(widget,
                                                 tr("Input New Password Again"),
                                                 tr("NEW PASSWORD"),
                                                 QLineEdit.Password,
                                                 flags=Qt.WindowStaysOnTopHint)
    if not ok_pressed:
        return False
    if pwd_new_2 != pwd_new:
        show_msg(tr("New password not match!"), "WARNING")
        return False

    # get original data
    from core.diary import diary_utils
    from core.interest import interest_utils
    from core.bill import bill_utils
    from core.note import note_utils
    diaries = diary_utils.get_between_dates()
    interests = interest_utils.get_list_by()
    bills = bill_utils.get_list_by()
    notes = note_utils.get_list_by()

    # re-encrypt data
    pwd_new_md5 = md5(pwd_new.encode(
        "utf8")).hexdigest() if pwd_new != "" else pwd_new
    set_config("password", pwd_new_md5)
    encrypt_utils.key = pwd_new
    diary_utils.update_diaries(diaries)
    interest_utils.update_many(interests)
    bill_utils.update_many(bills)
    note_utils.update_many(notes)
    return True
