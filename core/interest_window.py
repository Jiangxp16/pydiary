from core.interest import Ui_Interest

from core import interest_utils, utils
from core.qt_base import BaseWindow, QEvent, QFileDialog, QMessageBox, QKeyEvent, Qt, QPixmap


class InterestWindow(Ui_Interest, BaseWindow):

    def __init__(self, parent=None):
        BaseWindow.__init__(self, parent)
        self.setupUi(self)
        self.connections = (
            (self.pb_add.clicked, self.btn_add),
            (self.pb_del.clicked, self.btn_del),
            (self.pb_imp.clicked, self.btn_imp),
            (self.pb_exp.clicked, self.btn_exp),
            (self.le_filter.editingFinished, self.filter_edited),
            (self.tw_interest.itemSelectionChanged, self.interest_sel_changed),
            (self.cb_sort.currentIndexChanged, self.sort_sel_changed),
            (self.tw_interest.cellChanged, self.interest_edited),
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
        self.start_task(interest_utils.delete, id=self.interest.id)
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

    def filter_edited(self):
        filter_new = self.le_filter.text()
        if filter_new == self.filter:
            return
        self.filter = filter_new
        self.update_table_interest()

    def interest_edited(self, row, col):
        if col == 3:
            return
        self.disconnect_all()
        tw = self.tw_interest
        interest = self.interest
        value = self.get_table_value(tw, row, col)
        interest.set_param(col, value)
        self.start_task(interest_utils.update, interest)
        self.connect_all()

    def sort_edited(self):
        if not self.interest:
            return
        cb = self.sender()
        self.interest.sort = cb.currentIndex() + 1
        self.set_table_value(self.tw_interest, self.row_interest, 3, self.sorts[self.interest.sort])
        self.start_task(interest_utils.update, self.interest)

    def update_table_interest(self):
        self.disconnect_all()
        tw = self.tw_interest
        tw.clearContents()
        tw.setRowCount(len(self.interests))
        tw.setSortingEnabled(False)
        for row in range(tw.rowCount()):
            interest = self.interests[row]
            cb_sort = self.get_table_combo(tw, row, 3, self.sorts[1:])
            cb_sort.setCurrentIndex(interest.sort - 1)
            self.reconnect(cb_sort.currentIndexChanged, self.sort_edited)
            self.set_table_value(tw, row, 0, interest.id)
            self.set_table_value(tw, row, 1, interest.added, False, center=True)
            self.set_table_value(tw, row, 2, interest.name)
            self.set_table_value(tw, row, 3, self.sorts[interest.sort], center=True)
            self.set_table_value(tw, row, 4, interest.progress, center=True)
            self.set_table_value(tw, row, 5, interest.publish, center=True)
            self.set_table_value(tw, row, 6, interest.date, center=True)
            self.set_table_value(tw, row, 7, float(interest.score_db), center=True)
            self.set_table_value(tw, row, 8, float(interest.score_imdb), center=True)
            self.set_table_value(tw, row, 9, float(interest.score), center=True)
            self.set_table_value(tw, row, 10, interest.remark)
            tw.setRowHidden(row, len(self.filter) > 0 and self.filter.upper() not in str(interest).upper())
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
