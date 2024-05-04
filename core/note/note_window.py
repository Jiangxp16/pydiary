from core.note import note_utils
from core.note.note import Ui_Note
from core.util.qtutils import BaseWindow, QEvent, QFileDialog, Qt, QIcon, QKeyEvent
from core.util import utils


class NoteWindow(Ui_Note, BaseWindow):

    def __init__(self, parent=None):
        BaseWindow.__init__(self, parent)
        self.setupUi(self)
        self.connections = (
            (self.pb_add.clicked, self.btn_add),
            (self.pb_del.clicked, self.btn_del),
            (self.pb_imp.clicked, self.btn_imp),
            (self.pb_exp.clicked, self.btn_exp),
            (self.le_filter.editingFinished, self.filter_edited),
            (self.tw_note.itemSelectionChanged, self.note_sel_changed),
            (self.tw_note.cellChanged, self.note_edited),
            (self.cb_state.currentIndexChanged, self.state_changed),
        )
        self.init()
        self.connect_all()

    def init(self):
        self.setWindowIcon(QIcon(utils.get_path(utils.load_config("style", "icon_note"))))
        self.pb_imp.setIcon(QIcon(utils.get_path(utils.load_config("style", "icon_imp"))))
        self.pb_exp.setIcon(QIcon(utils.get_path(utils.load_config("style", "icon_exp"))))
        self.pb_add.setIcon(QIcon(utils.get_path(utils.load_config("style", "icon_add"))))
        self.pb_del.setIcon(QIcon(utils.get_path(utils.load_config("style", "icon_del"))))
        self.filter = ''
        self.row_note = -1
        self.notes: list[note_utils.Note] = note_utils.get_list_by()
        self.note = None
        self.tw_note.setColumnCount(7)
        self.tw_note.setHorizontalHeaderLabels(["id", "Begin", "Last", "Process", "Desire", "Priority", "Content"])
        self.states = ["All", "To do", "Done"]
        self.state = 0
        self.tw_note.setColumnWidth(1, 110)
        self.tw_note.setColumnWidth(2, 110)
        for col in range(3, 7):
            self.tw_note.setColumnWidth(col, 80)
        self.tw_note.hideColumn(0)
        self.set_i18n()
        self.cb_state.addItems(self.states)
        self.update_table_note()

    def set_i18n(self):
        self.language = utils.load_config("global", "language")
        if self.language == "zh":
            self.states = ["全部", "待完成", "已完成"]
            self.tw_note.setHorizontalHeaderLabels(["id", "初始日期", "最后日期", "进度", "期望值", "优先级", "内容"])
            self.le_filter.setPlaceholderText("搜索...")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_D:
                return self.btn_del()
            if event.key() == Qt.Key.Key_N:
                return self.btn_add()
            if event.key() == Qt.Key.Key_I:
                return self.btn_imp()
            if event.key() == Qt.Key.Key_E:
                return self.btn_exp()
        else:
            return super().keyPressEvent(event)

    def btn_add(self):
        self.note = note_utils.add()
        self.notes.append(self.note)
        self.update_table_note()

    def btn_del(self):
        if self.note is None:
            return
        self.notes.remove(self.note)
        self.start_task(note_utils.delete, id=self.note.id)
        self.note = None
        self.update_table_note()

    def btn_imp(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Import from xlsx file", "", filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            note_utils.imp(file)
            self.notes = note_utils.get_list_by()
            self.note = None
            self.update_table_note()

    def btn_exp(self):
        file, _ = QFileDialog.getSaveFileName(self, "Export to xlsx file", "note.xlsx",
                                              filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            note_utils.exp(file)

    def state_changed(self):
        self.state = self.cb_state.currentIndex()
        self.update_table_note()

    def note_sel_changed(self):
        self.row_note = self.tw_note.currentRow()
        if self.row_note < 0:
            self.note = None
        else:
            id_row = self.get_table_value(self.tw_note, self.row_note, 0)
            for i in range(len(self.notes)):
                if self.notes[i].id == id_row:
                    self.note = self.notes[i]
                    break

    def filter_edited(self):
        filter_new = self.le_filter.text()
        if filter_new == self.filter:
            return
        self.filter = filter_new
        self.update_table_note()

    def note_edited(self, row, col):
        if self.note is None:
            return
        self.disconnect_all()
        note = self.note
        value = self.get_table_value(self.tw_note, row, col)
        if col == 1:
            note.begin = value
        elif col == 2:
            note.last = value
        elif col == 3:
            note.process = value
        elif col == 4:
            note.desire = value
        elif col == 5:
            note.priority = value
        elif col == 6:
            note.content = value
        self.start_task(note_utils.update, note)
        self.connect_all()

    def update_table_note(self):
        self.disconnect_all()
        tw = self.tw_note
        tw.setRowCount(len(self.notes))
        tw.setSortingEnabled(False)
        for row in range(tw.rowCount()):
            note = self.notes[row]
            self.set_table_value(tw, row, 0, note.id)
            self.set_table_value(tw, row, 1, note.begin, center=True)
            self.set_table_value(tw, row, 2, note.last, center=True)
            self.set_table_value(tw, row, 3, note.process, center=True)
            self.set_table_value(tw, row, 4, note.desire, center=True)
            self.set_table_value(tw, row, 5, note.priority, center=True)
            self.set_table_value(tw, row, 6, note.content)
            hidden = (len(self.filter) > 0 and self.filter.upper() not in str(note).upper()) or \
                (self.state == 1 and note.process >= 100) or (self.state == 2 and note.process < 100)
            tw.setRowHidden(row, hidden)
        tw.setSortingEnabled(True)
        if self.note is not None:
            for row in range(tw.rowCount()):
                if self.get_table_value(tw, row, 0) == note.id:
                    self.tw_note.selectRow(row)
                    self.row_note = row
                    break
        elif self.row_note > -1 and tw.rowCount() > 0:
            self.row_note = min(self.row_note, tw.rowCount() - 1)
            self.tw_note.selectRow(self.row_note)
            self.note_sel_changed()
        self.connect_all()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.ignore()
                return self.hide()
        return super().changeEvent(event)

    def closeEvent(self, event):
        event.ignore()
        return self.hide()