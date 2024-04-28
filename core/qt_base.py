from PySide6.QtGui import QCloseEvent, QFocusEvent, QKeyEvent, QPixmap, QIcon, QAction, QFont
from PySide6.QtCore import QDate, Qt, QEvent, QLocale, Signal, QThread, QThreadPool, QRunnable
from PySide6.QtWidgets import QMainWindow, QWidgetAction, QLabel, QTableWidget, QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QSizePolicy, QMenu, QSystemTrayIcon, QFileDialog, QPlainTextEdit, QHeaderView, QTableWidgetItem, QStyle

from core import utils


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


class LineEdit(QLineEdit):
    focusOut = Signal()

    def focusOutEvent(self, e: QFocusEvent) -> None:
        text = self.text()
        if self.text_last != text:
            self.text_last = text
            self.focusOut.emit()
        return super().focusOutEvent(e)

    def setText(self, text: str) -> None:
        self.text_last = text
        return super().setText(text)


class BaseWindow(QMainWindow):
    thread_update = QThreadPool()
    multi_thread = int(utils.load_config("global", "multi_thread"))

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

    def set_table_value(self, table: QTableWidget, row, col, value, editable=True, center=False):
        item = table.item(row, col)
        if item is None:
            item = QTableWidgetItem()
            table.setItem(row, col, item)
        item.setData(Qt.ItemDataRole.DisplayRole, value)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable if editable else item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        if center:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def get_table_value(self, table: QTableWidget, row, col):
        item = table.item(row, col)
        if item is None:
            return None
        return item.data(Qt.ItemDataRole.DisplayRole)

    def start_task(self, func, *args, **kwargs):
        if self.multi_thread:
            class Task(QRunnable):
                def run(self):
                    func(*args, **kwargs)
            self.thread_update.start(Task())
        else:
            func(*args, **kwargs)

    def get_table_widget(self, table: QTableWidget, row, col, obj_class):
        widget = table.cellWidget(row, col)
        if widget is None:
            widget = obj_class(table)
            widget.setContentsMargins(0, 0, 0, 0)
            widget.row = row
            widget.col = col
            widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            table.setCellWidget(row, col, widget)
        return widget

    def get_table_combo(self, table: QTableWidget, row, col, labels=None) -> QComboBox:
        cb: QComboBox = self.get_table_widget(table, row, col, QComboBox)
        if labels is not None:
            try:
                cb.currentIndexChanged.disconnect()
            except Exception:
                pass
            cb.clear()
            cb.addItems(labels)
        return cb

    def get_table_text_edit(self, table: QTableWidget, row, col) -> TextEdit:
        return self.get_table_widget(table, row, col, TextEdit)

    def get_table_line(self, table: QTableWidget, row, col) -> LineEdit:
        le: LineEdit = self.get_table_widget(table, row, col, LineEdit)
        return le

    def get_table_sb(self, table: QTableWidget, row, col) -> QSpinBox:
        sb: QSpinBox = self.get_table_widget(table, row, col, QSpinBox)
        sb.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        sb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb.setKeyboardTracking(False)
        return sb

    def get_table_dsb(self, table: QTableWidget, row, col) -> QDoubleSpinBox:
        sb: QDoubleSpinBox = self.get_table_widget(table, row, col, QDoubleSpinBox)
        sb.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        sb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb.setKeyboardTracking(False)
        sb.setDecimals(1)
        return sb

    def reconnect(self, signal, slot):
        try:
            signal.disconnect()
        except Exception:
            pass
        finally:
            signal.connect(slot)
