import datetime

from core.bill import bill_utils
from core.bill.bill import Ui_Bill
from core.util.qt_utils import BaseWindow, NoSelectionDelegate, QEvent, QFileDialog, Qt, QIcon, QKeyEvent, QHeaderView
from core.util import utils, config_utils
from core.util.i18n_utils import tr


class BillWindow(Ui_Bill, BaseWindow):

    def __init__(self, parent=None):
        BaseWindow.__init__(self, parent)
        self.setupUi(self)
        self.connections = (
            (self.pb_add.clicked, self.btn_add),
            (self.pb_del.clicked, self.btn_del),
            (self.pb_imp.clicked, self.btn_imp),
            (self.pb_exp.clicked, self.btn_exp),
            (self.le_filter.editingFinished, self.filter_edited),
            (self.tw_bill.itemSelectionChanged, self.bill_sel_changed),
            (self.tw_bill.cellChanged, self.bill_edited),
            (self.sb_start.valueChanged, self.date_changed),
            (self.sb_end.valueChanged, self.date_changed),
        )
        self.init()
        self.connect_all()

    def init(self):
        self.setWindowIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_bill"))))
        self.pb_imp.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_imp"))))
        self.pb_exp.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_exp"))))
        self.pb_add.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_add"))))
        self.pb_del.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_del"))))
        today = datetime.date.today()
        self.day_start = utils.date2int(
            datetime.date(today.year, today.month, 1))
        self.day_end = utils.date2int(
            utils.get_last_day(today.year, today.month))
        self.sb_start.setValue(self.day_start)
        self.sb_end.setValue(self.day_end)
        self.filter = ''
        self.row_bill = -1
        self.bills: list[bill_utils.Bill] = bill_utils.get_between_dates(
            self.day_start, self.day_end)
        self.bill = None
        self.tw_bill.setColumnCount(6)
        self.tw_bill.setHorizontalHeaderLabels(
            [tr(x) for x in ["id", "Date", "Inout", "Type", "Amount", "Item"]])
        self.tw_bill.setAlternatingRowColors(True)
        self.inouts = [tr("Out"), tr("In")]
        self.lb_total.setText(tr("Total"))
        self.lb_in.setText(tr("In"))
        self.lb_out.setText(tr("Out"))
        self.le_filter.setPlaceholderText(tr("Search..."))
        font_style = "*{font-size:12px;}"
        self.sb_start.setStyleSheet(font_style)
        self.sb_end.setStyleSheet(font_style)
        self.dsb_total.setStyleSheet(font_style)
        self.dsb_in.setStyleSheet(font_style)
        self.dsb_out.setStyleSheet(font_style)
        self.lb_total.setStyleSheet(font_style)
        self.lb_in.setStyleSheet(font_style)
        self.lb_out.setStyleSheet(font_style)
        self.tw_bill.setColumnWidth(1, 110)
        self.tw_bill.setColumnWidth(2, 60)
        for col in range(4, 6):
            self.tw_bill.setColumnWidth(col, 80)
        self.tw_bill.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tw_bill.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tw_bill.hideColumn(0)
        self.tw_bill.setItemDelegate(NoSelectionDelegate())
        self.update_table_bill()

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
        self.bill = bill_utils.add()
        self.bills.append(self.bill)
        self.update_table_bill()

    def btn_del(self):
        if self.bill is None:
            return
        self.bills.remove(self.bill)
        self.start_task(bill_utils.delete, id=self.bill.id)
        self.bill = None
        self.update_table_bill()

    def btn_imp(self):
        file, _ = QFileDialog.getOpenFileName(
            self, tr("Import from xlsx file"), "", filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            bill_utils.imp(file)
            self.bills = bill_utils.get_between_dates(
                self.day_start, self.day_end)
            self.bill = None
            self.update_table_bill()

    def btn_exp(self):
        file, _ = QFileDialog.getSaveFileName(self, tr("Export to xlsx file"), "bill.xlsx",
                                              filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            bill_utils.exp(file, self.day_start, self.day_end)

    def date_changed(self):
        widget = self.sender()
        if widget == self.sb_start:
            self.day_start = self.sb_start.value()
        elif widget == self.sb_end:
            self.day_end = self.sb_end.value()
        self.bills = bill_utils.get_between_dates(self.day_start, self.day_end)
        self.bill = None
        self.update_table_bill()

    def bill_sel_changed(self):
        self.row_bill = self.tw_bill.currentRow()
        if self.row_bill < 0:
            self.bill = None
        else:
            id_row = self.get_table_value(self.tw_bill, self.row_bill, 0)
            for i in range(len(self.bills)):
                if self.bills[i].id == id_row:
                    self.bill = self.bills[i]
                    break

    def filter_edited(self):
        filter_new = self.le_filter.text()
        if filter_new == self.filter:
            return
        self.filter = filter_new
        self.update_table_bill()

    def bill_edited(self, row, col):
        if col == 2 or self.bill is None:
            return
        self.disconnect_all()
        bill = self.bill
        value = self.get_table_value(self.tw_bill, row, col)
        if col == 1:
            bill.date = value
        elif col == 3:
            bill.type = value
        elif col == 4:
            bill.amount = value
        elif col == 5:
            bill.item = value
        self.start_task(bill_utils.update, bill)
        self.connect_all()
        self.update_total()

    def inout_edited(self):
        if not self.bill:
            return
        cb_inout = self.sender()
        self.bill.inout = -1 if cb_inout.currentIndex() == 0 else 1
        self.set_table_value(self.tw_bill, self.row_bill, 2, self.bill.inout)
        self.start_task(bill_utils.update, self.bill)
        self.update_total()

    def update_table_bill(self):
        self.disconnect_all()
        tw = self.tw_bill
        tw.setRowCount(len(self.bills))
        tw.setSortingEnabled(False)
        for row in range(tw.rowCount()):
            bill = self.bills[row]
            self.set_table_value(tw, row, 0, bill.id)
            self.set_table_value(tw, row, 1, bill.date, center=True)
            cb_inout = self.get_table_combo(tw, row, 2, self.inouts)
            cb_inout.setCurrentIndex(0 if bill.inout < 0 else 1)
            self.reconnect(cb_inout.currentIndexChanged, self.inout_edited)
            self.set_table_value(tw, row, 2, bill.inout, center=True)
            self.set_table_value(tw, row, 3, bill.type, center=True)
            self.set_table_value(tw, row, 4, float(bill.amount), center=True)
            self.set_table_value(tw, row, 5, bill.item)
            tw.setRowHidden(row, len(self.filter) >
                            0 and self.filter.upper() not in str(bill).upper())
        tw.setSortingEnabled(True)
        if self.bill is not None:
            for row in range(tw.rowCount()):
                if self.get_table_value(tw, row, 0) == bill.id:
                    self.tw_bill.selectRow(row)
                    self.row_bill = row
                    break
        elif self.row_bill > -1 and tw.rowCount() > 0:
            self.row_bill = min(self.row_bill, tw.rowCount() - 1)
            self.tw_bill.selectRow(self.row_bill)
            self.bill_sel_changed()
        self.connect_all()
        self.update_total()

    def update_total(self):
        total = 0.
        total_in = 0.
        total_out = 0.
        for bill in self.bills:
            if len(self.filter) > 0 and self.filter.upper() not in str(bill).upper():
                continue
            total += bill.amount * bill.inout
            if bill.inout > 0:
                total_in += bill.amount
            else:
                total_out += bill.amount
        self.dsb_total.setValue(total)
        self.dsb_in.setValue(total_in)
        self.dsb_out.setValue(total_out)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.ignore()
                return self.hide()
        return super().changeEvent(event)

    def closeEvent(self, event):
        event.ignore()
        return self.hide()
