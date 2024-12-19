import sys
import os
import atexit

name_exec = sys.argv[0]
if name_exec.endswith(".exe"):
    os.chdir(os.path.dirname(name_exec))

sys.path.append('./')


def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Record exceptions to log
    """
    import time
    import traceback
    with open("error.log", "a") as f:
        err_msg = time.strftime("%Y-%m-%d %H:%M:%S ") + \
            ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        f.write(err_msg)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
    sys.exit(-1)


sys.excepthook = handle_exception

from core.diary.diary_window import DiaryWindow
from core.util.qt_utils import QApplication, load_qss, QSharedMemory, show_msg
from core.util import config_utils, dbconfig_utils, win_utils

if int(config_utils.load_config("global", "start_on_startup")):
    win_utils.add_to_startup()
else:
    win_utils.remove_from_startup()

app = QApplication(sys.argv)

shared = QSharedMemory(app.applicationFilePath())
if not shared.create(1):
    shared.attach()
    shared.detach()
    if not shared.create(1):
        show_msg("Another instance is already running.", "WARNING")
        os._exit(0)


@atexit.register
def clean_shared_memory():
    shared.detach()


load_qss(app)

if not dbconfig_utils.login():
    sys.exit(0)

diary = DiaryWindow()
if not int(config_utils.load_config("global", "hide_on_startup")):
    diary.show()

app.exec()
