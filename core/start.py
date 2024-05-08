import sys
sys.path.append('./')

from core.diary.diary_window import DiaryWindow
from core.util import utils
from core.util.qt_utils import QApplication
from core.util.i18n_utils import tr
from core.util import config_utils

app = QApplication(sys.argv)
utils.load_qss(app)

if not config_utils.login():
    sys.exit(0)

diary = DiaryWindow()
if not utils.load_config("global", "hide_on_startup"):
    diary.show()
sys.exit(app.exec())
