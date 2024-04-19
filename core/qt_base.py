from PySide6.QtGui import QCloseEvent, QFocusEvent, QKeyEvent, QPixmap, QIcon, QAction
from PySide6.QtCore import QDate, Qt, QEvent, QLocale, Signal
from PySide6.QtWidgets import QMainWindow, QTableWidget, QMessageBox, QSizePolicy, QMenu, QSystemTrayIcon, QFileDialog, QPlainTextEdit, QHeaderView, QTableWidgetItem


class TextEdit(QPlainTextEdit):
    focusOut = Signal()

    def focusOutEvent(self, e: QFocusEvent) -> None:
        text = self.toPlainText()
        if self.text_last != text:
            self.text_last = text
            self.focusOut.emit()
        return super().focusOutEvent(e)

    def setPlainText(self, text: str) -> None:
        self.text_last = text
        return super().setPlainText(text)


class BaseWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

    def connect_all(self):
        self.disconnect_all()
        for ele, func in self.connections:
            ele.connect(func)

    def disconnect_all(self):
        for ele, _ in self.connections:
            try:
                ele.disconnect()
            except Exception:
                pass

    def set_table_value(self, table: QTableWidget, row, col, value, editable=True):
        item = table.item(row, col)
        if item is None:
            item = QTableWidgetItem()
            table.setItem(row, col, item)
        item.setData(Qt.ItemDataRole.DisplayRole, value)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable if editable else item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def get_table_value(self, table: QTableWidget, row, col):
        item = table.item(row, col)
        if item is None:
            return None
        return item.data(Qt.ItemDataRole.DisplayRole)
