import os

from PySide6.QtGui import QGuiApplication, QCloseEvent, QFocusEvent, QKeyEvent, QPixmap, QImage, QIcon, QAction, QFont
from PySide6.QtCore import QDate, Qt, QEvent, QLocale, Signal, QThread, QThreadPool, QRunnable, QSharedMemory
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QWidgetAction, QLabel, QCheckBox, QTableWidget, QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QSizePolicy, QMenu, QSystemTrayIcon, QFileDialog, QPlainTextEdit, QHeaderView, QTableWidgetItem, QStyle, QInputDialog

from core.util import utils, config_utils


def wheel_event(widget: QWidget, event: QEvent = None):
    return


def key_pressed(table: QTableWidget, event: QKeyEvent):
    if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
        if event.key() == Qt.Key.Key_C:
            text = ""
            row = table.currentRow()
            col = table.currentColumn()
            item = table.item(row, col)
            widget = table.cellWidget(row, col)
            if widget is not None:
                if isinstance(widget, QComboBox):
                    text = widget.currentText()
                elif isinstance(widget, QPlainTextEdit):
                    text = widget.toPlainText()
                elif isinstance(widget, QLineEdit):
                    text = widget.text()
            elif item is not None:
                text = item.text()
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(text)
        elif event.key() == Qt.Key.Key_V:
            clipboard = QGuiApplication.clipboard()
            text = clipboard.text()
            row = table.currentRow()
            col = table.currentColumn()
            widget = table.cellWidget(row, col)
            item = table.item(row, col)
            if widget is not None:
                if isinstance(widget, QComboBox):
                    widget.setCurrentText(text)
                elif isinstance(widget, QPlainTextEdit):
                    widget.setPlainText(text)
                elif isinstance(widget, QLineEdit):
                    widget.setText(text)
            elif item is not None:
                value = item.data(Qt.ItemDataRole.DisplayRole)
                try:
                    item.setData(Qt.ItemDataRole.DisplayRole, type(value)(text))
                except Exception:
                    return
    return super(QTableWidget, table).keyPressEvent(event)


QTableWidget.keyPressEvent = key_pressed
QComboBox.wheelEvent = wheel_event
QDoubleSpinBox.wheelEvent = wheel_event
QSpinBox.wheelEvent = wheel_event


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
    multi_thread = int(config_utils.load_config("global", "multi_thread"))

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


def show_msg(msg, level="INFO", buttons=QMessageBox.Ok):
    level = level.upper()
    msg_type = QMessageBox.Information
    icon = QIcon(QApplication.style().standardPixmap(QStyle.StandardPixmap.SP_MessageBoxInformation))
    if level == "WARNING":
        msg_type = QMessageBox.Warning
        icon = QIcon(QApplication.style().standardPixmap(QStyle.StandardPixmap.SP_MessageBoxWarning))
    elif level == "ERROR" or level == "CRITICAL":
        msg_type = QMessageBox.Critical
        icon = QIcon(QApplication.style().standardPixmap(QStyle.StandardPixmap.SP_MessageBoxCritical))
    qmsg = QMessageBox(msg_type, level, msg, buttons)
    qmsg.setWindowFlags(Qt.WindowStaysOnTopHint)
    qmsg.setWindowIcon(icon)
    qmsg.exec()


def load_qss(app):
    config = config_utils.load_config("style")
    qss_file = config.get("qss")
    font_size = config.get("font_size")
    font = config.get("font")
    style_sheet = ""
    if qss_file is not None:
        qss_file = utils.get_path(qss_file)
        if os.path.isfile(qss_file):
            try:
                with open(qss_file, "r", encoding="utf-8") as f:
                    style_sheet = f.read()
            except Exception as e:
                print(e.args)
    if font is not None:
        style_sheet += "\r\n*{font-family:%s;}" % font
    if font_size is not None:
        style_sheet += "\r\n*{font-size:%spx;}" % font_size
    app.setStyleSheet(style_sheet)
