import sys
import atexit
sys.path.append('./')

from core.diary.diary_window import DiaryWindow
from core.util.qt_utils import QApplication, load_qss, QSharedMemory
from core.util import config_utils, dbconfig_utils

app = QApplication(sys.argv)

shared = QSharedMemory(app.applicationFilePath())
if not shared.create(1):
    shared.attach()
    shared.detach()
    if not shared.create(1):
        print("Another instance is already running.")
        sys.exit(0)

load_qss(app)

if not dbconfig_utils.login():
    sys.exit(0)

diary = DiaryWindow()
if not config_utils.load_config("global", "hide_on_startup"):
    diary.show()

app.exec()
shared.detach()
sys.exit(app.exec())
