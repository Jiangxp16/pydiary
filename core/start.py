import sys
import os

name_exec = sys.argv[0]
if name_exec.endswith(".exe"):
    os.chdir(os.path.dirname(name_exec))

sys.path.append('./')

from core.diary.diary_window import DiaryWindow
from core.util.qt_utils import load_qss, show_msg, SingleInstanceApp
from core.util import config_utils, dbconfig_utils, win_utils

if int(config_utils.load_config("global", "start_on_startup")):
    win_utils.add_to_startup()
else:
    win_utils.remove_from_startup()


def handle_exception(exc_type, exc_value, exc_traceback):
    import time
    import traceback
    err_msg = time.strftime("%Y-%m-%d %H:%M:%S ") + \
        ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    with open("error.log", "a") as f:
        f.write(err_msg)
    show_msg(err_msg, "ERROR")
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
    sys.exit(-1)


sys.excepthook = handle_exception

app = SingleInstanceApp(sys.argv)

if app.is_running:
    sys.exit(0)

if not app.is_running:
    load_qss(app)
    if not dbconfig_utils.login():
        sys.exit(0)
    diary = DiaryWindow()
    app.activationRequested.connect(diary.show_default)
    if not int(config_utils.load_config("global", "hide_on_startup")):
        diary.show()

sys.exit(app.exec())
