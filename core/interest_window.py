from core.interest import Ui_Interest

from core import interest_utils, utils
from core.qt_base import BaseWindow, QFileDialog, QHeaderView, QMessageBox, QKeyEvent, Qt


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
            (self.tw_interest.cellChanged, self.interest_edited),
        )
        self.init()
        self.connect_all()

    def init(self):
        self.sorts = ["ALL", "MOVIE", "TV", "COMIC", "GAME", "BOOK", "MUSIC", "OTHERS"]
        self.sort = 0
        self.filter = ''
        self.row_interest = 0
        self.interests: list[interest_utils.Interest] = interest_utils.get_list_by(sort=self.sort)
        self.cb_sort.addItems(self.sorts)
        self.cb_sort.setCurrentIndex(self.sort)
        self.tw_interest.setColumnCount(11)
        self.tw_interest.setHorizontalHeaderLabels(["id", "Added", "Name", "Sort", "Progress",
                                                    "Publish", "Watched/Played", "Score (db)",
                                                    "Score (imdb)", "Score", "Remark"])
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
                                                        "发布日期", "最后观看/游玩", "评分 (db)",
                                                        "评分 (imdb)", "评分", "备注"])
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
        self.interests.append(interest_utils.add_new(sort=self.sort))
        self.update_table_interest()
        self.row_interest = len(self.interests) - 1

    def btn_del(self):
        if self.row_interest < 0:
            return
        id_row = self.get_table_value(self.tw_interest, self.row_interest, 0)
        for i in range(len(self.interests)):
            if self.interests[i].id == id_row:
                self.interests.pop(i)
                break
        interest_utils.delete(id=id_row)
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

    def filter_changed(self):
        filter_new = self.le_filter.text()
        if filter_new == self.filter:
            return
        self.filter = filter_new
        self.update_table_interest()

    def interest_edited(self, row, col):
        self.disconnect_all()
        tw = self.tw_interest
        id_row = self.get_table_value(tw, row, 0)
        for i in self.interests:
            if i.id == id_row:
                interest = i
                break
        value = self.get_table_value(tw, row, col)
        if col == 2:
            interest.name = value
        elif col == 3:
            interest.sort = self.sorts.index(value) if value in self.sorts else 0
            self.set_table_value(tw, row, col, self.sorts[interest.sort])
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
        interest_utils.update(interest)
        # self.set_table_value(tw, row, 11, interest.updated)
        self.connect_all()

    def update_table_interest(self):
        self.disconnect_all()
        tw = self.tw_interest
        tw.setRowCount(len(self.interests))
        tw.setSortingEnabled(False)
        tw.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for row in range(tw.rowCount()):
            interest = self.interests[row]
            self.set_table_value(tw, row, 0, interest.id)
            self.set_table_value(tw, row, 1, interest.added, False)
            self.set_table_value(tw, row, 2, interest.name)
            self.set_table_value(tw, row, 3, self.sorts[interest.sort])
            self.set_table_value(tw, row, 4, interest.progress)
            self.set_table_value(tw, row, 5, interest.publish)
            self.set_table_value(tw, row, 6, interest.date)
            self.set_table_value(tw, row, 7, float(interest.score_db))
            self.set_table_value(tw, row, 8, float(interest.score_imdb))
            self.set_table_value(tw, row, 9, float(interest.score))
            self.set_table_value(tw, row, 10, interest.remark)
            # self.set_table_value(tw, row, 11, interest.updated, False)
            if self.filter and self.filter not in str(interest):
                tw.setRowHidden(row, True)
            else:
                tw.setRowHidden(row, False)
        tw.setSortingEnabled(True)
        for col in range(tw.columnCount()):
            tw.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        tw.selectRow(self.row_interest)
        self.connect_all()
