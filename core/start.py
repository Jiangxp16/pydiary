import sys
sys.path.append('./')

from core.diary.diary_window import DiaryWindow
from core.util.qt_utils import QApplication, load_qss
from core.util import config_utils, dbconfig_utils

app = QApplication(sys.argv)
load_qss(app)

if not dbconfig_utils.login():
    sys.exit(0)

diary = DiaryWindow()
if not config_utils.load_config("global", "hide_on_startup"):
    diary.show()
sys.exit(app.exec())
