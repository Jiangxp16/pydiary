import sys
sys.path.append('./')
from PySide6.QtWidgets import QApplication
from core.diary.diary_window import DiaryWindow
from core.util import utils

app = QApplication(sys.argv)
utils.load_qss(app)
diary = DiaryWindow()
if not utils.load_config("global", "hide_on_startup"):
    diary.show()
sys.exit(app.exec())
