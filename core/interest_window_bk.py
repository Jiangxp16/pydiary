from core.interest import Ui_Interest

from core import interest_utils, utils
from core.qt_base import BaseWindow, QTableWidget, TextEdit, QSizePolicy, QEvent, QFileDialog, QHeaderView, QMessageBox, QKeyEvent, Qt, QPixmap


class InterestWindow(Ui_Interest, BaseWindow):

    def __init__(self, parent=None):
        BaseWindow.__init__(self, parent)
        self.setupUi(self)
        self.connections = (
            (self.pb_add.clicked, self.btn_add),
            (self.pb_del.clicked, self.btn_del),
            (self.pb_imp.clicked, self.btn_imp),
            (self.pb_exp.clicked, self.btn_exp),
            (self.le_filter.editingFinished, self.filter_changed),
            (self.tw_interest.itemSelectionChanged, self.interest_sel_changed),
            (self.cb_sort.currentIndexChanged, self.sort_sel_changed),
        )
        self.init()
        self.connect_all()

    def init(self):
        self.logo_path = utils.get_path(utils.load_config("style", "logo"))
        self.setWindowIcon(QPixmap(self.logo_path))
        self.sorts = ["All", "Movie", "TV", "Comic", "Game", "Book", "Music", "Others"]
        self.sort = 0
        self.filter = ''
        self.row_interest = -1
        self.interests: list[interest_utils.Interest] = interest_utils.get_list_by(sort=self.sort)
        self.interest = None
        self.cb_sort.addItems(self.sorts)
        self.cb_sort.setCurrentIndex(self.sort)
        self.tw_interest.setColumnCount(11)
        self.tw_interest.setHorizontalHeaderLabels(["id", "Added", "Name", "Sort", "Prog",
                                                    "Pub", "Last", "Score\r\n(db)",
                                                    "Score\r\n(imdb)", "Score", "Remark"])
        for col in range(11):
            self.tw_interest.setColumnWidth(col, 80)
        self.tw_interest.setColumnWidth(2, 360)
        self.tw_interest.hideColumn(0)
        self.tw_interest.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.set_i18n()
        self.update_table_interest()

    def set_i18n(self):
        self.language = utils.load_config("global", "language")
        if self.language == "zh":
            self.sorts = ["全部", "电影", "电视剧", "动漫", "游戏", "书籍", "音乐", "其他"]
            self.cb_sort.clear()
            self.cb_sort.addItems(self.sorts)
            self.cb_sort.setCurrentIndex(self.sort)
            self.tw_interest.setHorizontalHeaderLabels(["id", "添加日期", "名称", "分类", "进度",
                                                        "发布", "最后日期", "评分\r\n(db)",
                                                        "评分\r\n(imdb)", "评分", "备注"])
            self.le_filter.setPlaceholderText("搜索...")
            self.pb_exp.setText("导出")
            self.pb_imp.setText("导入")
            # self.pb_add.setText("添加")
            # self.pb_del.setText("删除")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_D:
            ok_pressed = QMessageBox.question(self, 'WARNING', 'Delete information in current page?', QMessageBox.Yes | QMessageBox.No,
                                              QMessageBox.No)
            if ok_pressed == QMessageBox.No:
                return
            interest_utils.delete(sort=self.sort)
            self.interests = interest_utils.get_list_by(sort=self.sort)
            self.update_table_interest()
        else:
            return super().keyPressEvent(event)

    def btn_add(self):
        if self.sort > 0:
            self.interest = interest_utils.add(sort=self.sort)
        else:
            self.interest = interest_utils.add(sort=len(self.sorts) - 1)
        self.interests.append(self.interest)
        self.update_table_interest()

    def btn_del(self):
        if self.interest is None:
            return
        self.interests.remove(self.interest)
        if self.multi_thread:
            self.start_task(interest_utils.delete, id=self.interest.id)
        else:
            interest_utils.delete(id=self.interest.id)
        self.interest = None
        self.update_table_interest()

    def btn_imp(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Import from xlsx file [REPLACE!]", "", filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            interest_utils.imp(file)
            self.interests = interest_utils.get_list_by(sort=self.sort)
            self.update_table_interest()

    def btn_exp(self):
        file, _ = QFileDialog.getSaveFileName(self, "Export to xlsx file", "", filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            interest_utils.exp(file, self.sort)

    def sort_sel_changed(self):
        self.sort = self.cb_sort.currentIndex()
        self.interests = interest_utils.get_list_by(sort=self.sort)
        self.update_table_interest()

    def interest_sel_changed(self):
        self.row_interest = self.tw_interest.currentRow()
        id_row = self.get_table_value(self.tw_interest, self.row_interest, 0)
        for i in range(len(self.interests)):
            if self.interests[i].id == id_row:
                self.interest = self.interests[i]
                break

    def filter_changed(self):
        filter_new = self.le_filter.text()
        if filter_new == self.filter:
            return
        self.filter = filter_new
        self.update_table_interest()

    def interest_edited_ori(self, row, col):
        self.disconnect_all()
        tw = self.tw_interest
        interest = self.interest
        value = self.get_table_value(tw, row, col)
        if col == 2:
            interest.name = value
        elif col == 4:
            interest.progress = value
        elif col == 5:
            interest.publish = value
        elif col == 6:
            interest.date = value
        elif col == 7:
            interest.score_db = value
        elif col == 8:
            interest.score_imdb = value
        elif col == 9:
            interest.score = value
        elif col == 10:
            interest.remark = value
        else:
            return
        if self.multi_thread:
            self.start_task(interest_utils.update, interest)
        else:
            interest_utils.update(interest)
        self.connect_all()

    def interest_edited(self):
        tw = self.tw_interest
        row = tw.currentRow()
        col = tw.currentColumn()
        widget = self.sender()
        if col == 3:
            self.interest.sort = widget.currentIndex() + 1
            self.set_table_value(self.tw_interest, row, 3, self.sorts[self.interest.sort])
        elif col == 2:
            self.interest.name = widget.text()
            self.set_table_value(self.tw_interest, row, 2, self.interest.name)
        elif col == 4:
            self.interest.progress = widget.text()
            self.set_table_value(self.tw_interest, row, 4, self.interest.progress)
        elif col == 5:
            self.interest.publish = widget.value()
            self.set_table_value(self.tw_interest, row, 5, self.interest.publish)
        elif col == 6:
            self.interest.date = widget.value()
            self.set_table_value(self.tw_interest, row, 6, self.interest.date)
        elif col == 7:
            self.interest.score_db = widget.value()
            self.set_table_value(self.tw_interest, row, 7, self.interest.score_db)
        elif col == 8:
            self.interest.score_imdb = widget.value()
            self.set_table_value(self.tw_interest, row, 8, self.interest.score_imdb)
        elif col == 9:
            self.interest.score = widget.value()
            self.set_table_value(self.tw_interest, row, 9, self.interest.score)
        elif col == 10:
            self.interest.remark = widget.text()
            self.set_table_value(self.tw_interest, row, 10, self.interest.remark)
        else:
            return
        if self.multi_thread:
            self.start_task(interest_utils.update, self.interest)
        else:
            interest_utils.update(self.interest)

    def update_table_interest(self):
        self.disconnect_all()
        tw = self.tw_interest
        tw.clearContents()
        tw.setRowCount(len(self.interests))
        tw.setSortingEnabled(False)
        for row in range(tw.rowCount()):
            interest = self.interests[row]
            self.set_table_value(tw, row, 0, interest.id)
            self.set_table_value(tw, row, 1, interest.added, False, center=True)

            le = self.get_table_line(tw, row, 2)
            le.setText(interest.name)
            self.reconnect(le.focusOut, self.interest_edited)
            self.set_table_value(tw, row, 2, interest.name)

            cb_sort = self.get_table_combo(tw, row, 3)
            cb_sort.clear()
            cb_sort.addItems(self.sorts[1:])
            if interest.sort > 0:
                cb_sort.setCurrentIndex(interest.sort - 1)
            else:
                cb_sort.setCurrentIndex(len(self.sorts) - 2)
            self.reconnect(cb_sort.currentIndexChanged, self.interest_edited)
            self.set_table_value(tw, row, 3, self.sorts[interest.sort], center=True)

            le = self.get_table_line(tw, row, 4)
            le.setText(interest.progress)
            self.reconnect(le.focusOut, self.interest_edited)
            self.set_table_value(tw, row, 4, interest.progress, center=True)

            sb = self.get_table_sb(tw, row, 5)
            sb.setValue(interest.publish)
            self.reconnect(sb.valueChanged, self.interest_edited)
            self.set_table_value(tw, row, 5, interest.publish, center=True)

            sb = self.get_table_sb(tw, row, 6)
            sb.setValue(interest.date)
            self.reconnect(sb.valueChanged, self.interest_edited)
            self.set_table_value(tw, row, 6, interest.date, center=True)

            dsb = self.get_table_sb(tw, row, 7)
            dsb.setValue(interest.score_db)
            self.reconnect(dsb.valueChanged, self.interest_edited)
            self.set_table_value(tw, row, 7, float(interest.score_db), center=True)

            dsb = self.get_table_sb(tw, row, 8)
            dsb.setValue(interest.score_imdb)
            self.reconnect(dsb.valueChanged, self.interest_edited)
            self.set_table_value(tw, row, 8, float(interest.score_imdb), center=True)

            dsb = self.get_table_sb(tw, row, 9)
            dsb.setValue(interest.score)
            self.reconnect(dsb.valueChanged, self.interest_edited)
            self.set_table_value(tw, row, 9, float(interest.score), center=True)

            le = self.get_table_line(tw, row, 10)
            le.setText(interest.remark)
            self.reconnect(le.focusOut, self.interest_edited)
            self.set_table_value(tw, row, 10, interest.remark)

            if self.filter and self.filter.upper() not in str(interest).upper():
                tw.setRowHidden(row, True)
            else:
                tw.setRowHidden(row, False)
        tw.setSortingEnabled(True)
        if self.interest is not None:
            for row in range(tw.rowCount()):
                if self.get_table_value(tw, row, 0) == interest.id:
                    self.tw_interest.selectRow(row)
                    self.row_interest = row
                    break
        elif self.row_interest > -1 and tw.rowCount() > 0:
            self.tw_interest.selectRow(self.row_interest)
            self.interest_sel_changed()
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