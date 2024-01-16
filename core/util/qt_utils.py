import hashlib
import os
import platform
if platform.system() == 'Windows':
    import win32event
    import win32api
    import winerror

from PySide6.QtGui import QGuiApplication, QCloseEvent, QTextCursor, QFocusEvent, QKeyEvent, QPixmap, QImage, QIcon, QAction, QFont
from PySide6.QtCore import QAbstractItemModel, QCoreApplication, QModelIndex, QObject, QDate, QPersistentModelIndex, QRect, Qt, QEvent, QLocale, Signal, QThread, QThreadPool, QRunnable, QSharedMemory
from PySide6.QtWidgets import (QWidget, QApplication, QMainWindow, QWidgetAction, QLabel, QCheckBox, QTableWidget, QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox,
                               QMessageBox, QSizePolicy, QMenu, QSystemTrayIcon, QFileDialog, QPlainTextEdit, QHeaderView, QTableWidgetItem, QStyle,
                               QInputDialog, QItemDelegate, QStyledItemDelegate, QItemEditorFactory, QAbstractItemView, QDateTimeEdit,
                               )
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from core.util import utils, config_utils


class SingleInstanceApp(QApplication):
    activationRequested = Signal()

    def __init__(self, argv):
        super().__init__(argv)
        path_hash = hashlib.md5(self.applicationFilePath().encode("utf-8")).hexdigest()
        self.server_name = f"DIARY_{path_hash}"
        self.server = QLocalServer(self)
        self.is_running = False
        QLocalServer.removeServer(self.server_name)
        listening = self.server.listen(self.server_name)
        if not listening:
            self.activate_existing_instance()
            self.is_running = True
            return

        self.mutex = None
        if platform.system() == 'Windows':
            mutex = win32event.CreateMutex(None, 1, self.server_name)
            wait_result = win32event.WaitForSingleObject(mutex, 0)
            if wait_result == win32event.WAIT_OBJECT_0 or wait_result == win32event.WAIT_ABANDONED:
                self.mutex = mutex
            else:
                self.server.close()
                self.activate_existing_instance()
                self.is_running = True
                return

        self.server.newConnection.connect(self.handle_new_connection)

    def handle_new_connection(self):
        connection = self.server.nextPendingConnection()
        if connection:
            connection.waitForReadyRead(1000)
            message = bytes(connection.readAll()).decode('utf-8').strip()
            if message == 'activate':
                self.activationRequested.emit()
            connection.close()

    def activate_existing_instance(self):
        socket = QLocalSocket(self)
        socket.connectToServer(self.server_name)
        if socket.waitForConnected(1000):
            socket.write(b'activate')
            socket.waitForBytesWritten(1000)
            socket.close()

    def exec(self):
        if self.is_running:
            return 0
        return super().exec()

    def __del__(self):
        if self.server.isListening():
            self.server.close()
        if self.mutex is not None and platform.system() == 'Windows':
            win32event.ReleaseMutex(self.mutex)
            self.mutex = None


class TextEdit(QPlainTextEdit):
    focusIn = Signal()
    focusOut = Signal()

    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)
        self.text_last = None

    def focusOutEvent(self, e: QFocusEvent) -> None:
        text = self.toPlainText()
        if self.text_last != text:
            self.text_last = text
            self.focusOut.emit()
        return super().focusOutEvent(e)

    def focusInEvent(self, e: QFocusEvent) -> None:
        self.focusIn.emit()
        return super().focusInEvent(e)

    def setPlainText(self, text: str) -> None:
        self.text_last = text
        return super().setPlainText(text)


class LineEdit(QLineEdit):
    focusIn = Signal()
    focusOut = Signal()

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self.text_last = None

    def focusOutEvent(self, e: QFocusEvent) -> None:
        text = self.text()
        if self.text_last != text:
            self.text_last = text
            self.focusOut.emit()
        return super().focusOutEvent(e)

    def focusInEvent(self, e: QFocusEvent) -> None:
        self.focusIn.emit()
        return super().focusInEvent(e)

    def setText(self, text: str) -> None:
        self.text_last = text
        return super().setText(text)


class WheelEventFilter(QObject):

    def __init__(self) -> None:
        QObject.__init__(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Wheel:
            return True
        return super().eventFilter(watched, event)


wheel_event_filter = WheelEventFilter()


class ComboBox(QComboBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.wheel_enabled = False

    def wheelEvent(self, event: QEvent) -> None:
        if self.wheel_enabled:
            return super().wheelEvent(event)

    def enable_wheel(self, enabled=True):
        self.wheel_enabled = enabled

    def set_style(self, read_only=True, align_center=True):
        self.view().setTextElideMode(Qt.TextElideMode.ElideNone)
        self.setEditable(True)
        self.lineEdit().setReadOnly(read_only)

        if align_center:
            self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
            model = self.view().model()
            if model:
                for i in range(model.rowCount()):
                    if model.item(i):
                        model.item(i).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_current_text(self, text: str):
        self.setCurrentIndex(-1)
        for i in range(self.count()):
            if text == self.itemText(i):
                self.setCurrentIndex(i)
                break


class SpinBox(QSpinBox):
    focusIn = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.wheel_enabled = False
        self.installEventFilter(wheel_event_filter)
        self.setMinimum(-99999999)
        self.setMaximum(99999999)
        self.setKeyboardTracking(False)
        self.setAccelerated(True)
        self.setStepType(self.StepType.AdaptiveDecimalStepType)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setButtonSymbols(self.ButtonSymbols.NoButtons)

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.focusIn.emit()
        return super().focusInEvent(event)

    def enable_wheel(self, enabled=True):
        self.wheel_enabled = enabled

    def wheelEvent(self, event: QEvent) -> None:
        if self.wheel_enabled:
            return super().wheelEvent(event)


class DoubleSpinBox(QDoubleSpinBox):
    focusIn = Signal()

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.wheel_enabled = False
        self.installEventFilter(wheel_event_filter)
        self.setMinimum(-float("inf"))
        self.setMaximum(float("inf"))
        self.setKeyboardTracking(False)
        self.setAccelerated(True)
        self.setStepType(self.StepType.AdaptiveDecimalStepType)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setButtonSymbols(self.ButtonSymbols.NoButtons)

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.focusIn.emit()
        return super().focusInEvent(event)

    def enable_wheel(self, enabled=True):
        self.wheel_enabled = enabled

    def textFromValue(self, val: float) -> str:
        text = super().textFromValue(val)
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return text

    def wheelEvent(self, event: QEvent) -> None:
        if self.wheel_enabled:
            return super().wheelEvent(event)


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, decimals=2, step=0.01, **kwargs) -> None:
        super().__init__()
        self.decimals = decimals
        self.step = step
        self.set_kwargs(decimals=decimals, step=step, **kwargs)

    def set_kwargs(self, **kwargs):
        if "decimals" in kwargs:
            self.decimals = kwargs["decimals"]
        if "step" in kwargs:
            self.step = kwargs["step"]
        self.col_dict = kwargs.get("col_dict", {})
        self.labels_dict = kwargs.get("labels_dict", {})

    def createEditor(self, parent: QWidget, option, index) -> QWidget:
        editor_col = index.column()
        editor_data = index.data()
        editor_type = self.col_dict.get(editor_col)
        if editor_type is None:
            if isinstance(editor_data, float):
                editor_type = DoubleSpinBox
            elif isinstance(editor_data, int):
                editor_type = SpinBox
            else:
                editor_type = LineEdit
        if editor_type == TextEdit:
            editor = TextEdit(parent)
            editor.setContentsMargins(0, 0, 0, 0)
            editor.selectAll()
        elif editor_type == DoubleSpinBox:
            editor = DoubleSpinBox(parent)
            editor.setDecimals(self.decimals)
            editor.setSingleStep(self.step)
            editor.setFrame(False)
        elif editor_type == SpinBox:
            editor = SpinBox(parent)
            editor.setFrame(False)
        elif editor_type == LineEdit:
            editor = LineEdit(parent)
        elif editor_type == ComboBox:
            editor = ComboBox(parent)
            editor.enable_wheel()
            editor.addItems(self.labels_dict[editor_col])
            editor.currentIndexChanged.connect(editor.clearFocus)
        else:
            editor = super().createEditor(parent, option, index)
        editor.setStyleSheet("border-radius: 0px;")

        def deselect():
            editor.focusIn.disconnect(deselect)
            if isinstance(editor, TextEdit):
                cursor = editor.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)
                editor.setTextCursor(cursor)
            else:
                line = editor
                if isinstance(editor, SpinBox | DoubleSpinBox):
                    line = editor.findChild(QLineEdit)
                line.deselect()
                line.setCursorPosition(len(editor.text()))
        if isinstance(editor, SpinBox | DoubleSpinBox | LineEdit | TextEdit):
            editor.focusIn.connect(deselect)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        if isinstance(editor, TextEdit):
            return editor.setPlainText(index.data(Qt.ItemDataRole.DisplayRole))
        elif isinstance(editor, ComboBox):
            return editor.set_current_text(index.data(Qt.ItemDataRole.DisplayRole))
        return super().setEditorData(editor, index)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex) -> None:
        if isinstance(editor, TextEdit):
            return model.setData(index, editor.toPlainText())
        elif isinstance(editor, ComboBox):
            return model.setData(index, editor.currentText())
        return super().setModelData(editor, model, index)


class StateLabel(QLabel):
    OFF = DEFAULT = 0
    ON = 1
    ERROR = RUNNING = 2
    WARNING = 3

    STYLE_DICT = {
        ON: "background-color:green",
        OFF: "background-color:lightgray",
        ERROR: "background-color:red",
        WARNING: "background-color:yellow",
    }

    def __init__(self, state=DEFAULT, width=20, height=20, border_radius=10):
        QLabel.__init__(self)
        self.style = "border-radius:%dpx;" % border_radius
        self.setMinimumHeight(height)
        self.setMinimumWidth(width)
        self.setMaximumHeight(height)
        self.setMaximumWidth(width)
        self.setGeometry(QRect(0, 0, width, height))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_state(state)

    def set_state(self, state):
        self.setStyleSheet(self.style + self.STYLE_DICT.get(state, self.STYLE_DICT[self.DEFAULT]))


class TableWidget(QTableWidget):

    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.horizontalHeader().setSortIndicatorClearable(True)

    def keyPressEvent(self, event: QKeyEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_C:
                text = ""
                row = self.currentRow()
                col = self.currentColumn()
                item = self.item(row, col)
                widget = self.cellWidget(row, col)
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
                row = self.currentRow()
                col = self.currentColumn()
                widget = self.cellWidget(row, col)
                item = self.item(row, col)
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
        return super().keyPressEvent(event)

    def set_delegate(self, precision=2, step=0.01, **kwargs):
        delegate = self.itemDelegate()
        if isinstance(delegate, ItemDelegate):
            delegate.set_kwargs(decimals=precision, step=step, **kwargs)
        else:
            self.setItemDelegate(ItemDelegate(precision, step, **kwargs))

    def set_item(self, row, col, value, editable=True, center=False):
        item = self.item(row, col)
        if item is None:
            item = QTableWidgetItem()
            if center:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(row, col, item)
        item.setData(Qt.ItemDataRole.DisplayRole, value)
        flag = item.flags()
        if editable:
            flag |= Qt.ItemFlag.ItemIsEditable
        else:
            flag &= ~Qt.ItemFlag.ItemIsEditable
        item.setFlags(flag)

    def get_value(self, row, col):
        item = self.item(row, col)
        if item is None:
            return None
        return item.data(Qt.ItemDataRole.DisplayRole)

    def get_widget(self, row, col, widget_class):
        widget = self.cellWidget(row, col)
        if widget is None:
            widget = widget_class(self)
            widget.setContentsMargins(0, 0, 0, 0)
            widget.row = row
            widget.col = col
            widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            widget.setStyleSheet("border-radius: 0px;")
            self.setCellWidget(row, col, widget)
        return widget

    def get_combo(self, row, col, labels=None) -> ComboBox:
        cb = self.get_widget(row, col, ComboBox)
        if labels is not None:
            try:
                cb.currentIndexChanged.disconnect()
            except Exception:
                pass
            cb.clear()
            cb.addItems(labels)
        return cb

    def get_check(self, row, col) -> QCheckBox:
        return self.get_widget(row, col, QCheckBox)

    def get_state(self, row, col) -> StateLabel:
        return self.get_widget(row, col, StateLabel)

    def get_text(self, row, col) -> TextEdit:
        return self.get_widget(row, col, TextEdit)

    def get_line(self, row, col) -> LineEdit:
        return self.get_widget(row, col, LineEdit)

    def set_style(self, resize_column=(), align_center=True, selected_row=-1):
        self.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in resize_column:
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        if align_center:
            for i in range(self.rowCount()):
                for j in range(self.columnCount()):
                    item = self.item(i, j)
                    if item is not None:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        items = self.selectedItems()
        if len(items) > 0:
            if items[0].row() != selected_row:
                self.selectRow(selected_row)
        else:
            self.selectRow(selected_row)

    def get_selected_rows(self):
        rows = set()
        for item in self.selectedItems():
            rows.add(item.row())
        return list(rows)


class QtTask(QRunnable, QObject):
    complete_signal = Signal(object)

    def __init__(self, func, args=(), kwargs=None, complete=None):
        QRunnable.__init__(self)
        QObject.__init__(self)
        self._func = func
        self._args = args
        self._kwargs = kwargs if kwargs is not None else {}
        if complete is not None:
            self.complete_signal.connect(complete)

    def run(self):
        res = self._func(*self._args, **self._kwargs)
        self.complete_signal.emit(res)


class BaseWindow(QMainWindow):
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

    def start_task(self, func, args=(), kwargs=None, complete=None):
        kwargs = kwargs if kwargs is not None else {}
        if self.multi_thread:
            QThreadPool.globalInstance().start(QtTask(func, args, kwargs, complete))
        else:
            res = func(*args, **kwargs)
            if complete is not None:
                complete(res)

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
