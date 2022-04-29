import sys
sys.path.append('./')
from PySide6.QtWidgets import QApplication
from core.diary_window import DiaryWindow
from core import utils

app = QApplication(sys.argv)
utils.load_qss(app)
diary = DiaryWindow()
# diary.show()
if not utils.load_config("global", "hide_on_startup"):
    diary.show()
sys.exit(app.exec())
