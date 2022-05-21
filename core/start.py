import sys
import atexit
sys.path.append('./')

from core.diary.diary_window import DiaryWindow
from core.util.qt_utils import QApplication, load_qss, QSharedMemory, show_msg, QCoreApplication
from core.util import config_utils, dbconfig_utils

app = QApplication(sys.argv)

shared = QSharedMemory(app.applicationFilePath())
if not shared.create(1):
    shared.attach()
    shared.detach()
    if not shared.create(1):
        show_msg("Another instance is already running.", "WARNING")
        QCoreApplication.exit(0)


@atexit.register
def clean_shared_memory():
    shared.detach()


load_qss(app)

if not dbconfig_utils.login():
    QCoreApplication.exit(0)

diary = DiaryWindow()
if not int(config_utils.load_config("global", "hide_on_startup")):
    diary.show()

app.exec()
