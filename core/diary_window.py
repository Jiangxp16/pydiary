import sys
from core import sqlutils, utils
from core.diary import Ui_Diary
from PySide6.QtGui import QCloseEvent, QKeyEvent, QPixmap, QIcon, QAction
from PySide6.QtCore import QDate, Qt, QEvent, QLocale
from PySide6.QtWidgets import QMainWindow, QMenu, QSystemTrayIcon, QFileDialog, QPlainTextEdit, QHeaderView, QItemEditorFactory, QTableWidgetItem, QStyledItemDelegate


class QTextEditFactory(QItemEditorFactory):

    def __init__(self) -> None:
        super().__init__()

    def createEditor(self, userType, parent):
        return QPlainTextEdit(parent)


class DiaryWindow(Ui_Diary, QMainWindow):
    VIEW_DAILY = 0
    VIEW_MONTHLY = 1
    WEEK_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connections = (
            (self.calendar.currentPageChanged, self.month_changed),
            (self.calendar.selectionChanged, self.date_changed),
            (self.pb_daily.clicked, self.set_daily_view),
            (self.pb_monthly.clicked, self.set_monthly_view),
            (self.tw_content.itemSelectionChanged, self.diary_selected_changed),
            (self.tw_content.cellChanged, self.diary_edited),
            (self.le_location.editingFinished, self.diary_edited),
            (self.le_weather.editingFinished, self.diary_edited),
            (self.pb_save.clicked, self.btn_save),
            (self.pb_export.clicked, self.btn_export),
            (self.pb_import.clicked, self.btn_import),
            (self.cb_autosave.clicked, self.cb_autosave_changed),
        )
        self.init()
        self.connect_all()

    def init(self):
        self.set_i18n()
        self.pb_save.setEnabled(False)
        self.tw_content.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tw_content.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        delegate = QStyledItemDelegate()
        delegate.setItemEditorFactory(QTextEditFactory())
        self.tw_content.setItemDelegate(delegate)
        self.logo_path = utils.get_path(utils.load_config("style", "logo"))
        self.setWindowIcon(QPixmap(self.logo_path))
        self.add_tray()
        first_day_of_week = int(utils.load_config("global", "first_day_of_week")) % 7
        if first_day_of_week == 0:
            first_day_of_week += 7
        self.first_day_of_week = first_day_of_week
        self.last_day_of_week = first_day_of_week + 6 if first_day_of_week < 2 else first_day_of_week - 1
        self.calendar.setFirstDayOfWeek(Qt.DayOfWeek(first_day_of_week))
        self.date = QDate.currentDate()
        self.diaries = sqlutils.get_month_diary(self.date.year(), self.date.month())
        self.calendar.setSelectedDate(self.date)
        self.set_daily_view()
        self.update_day_selected()

    def cb_autosave_changed(self):
        self.pb_save.setEnabled(not self.cb_autosave.isChecked())

    def set_i18n(self):
        self.language = utils.load_config("global", "language")
        if self.language == "zh":
            self.calendar.setLocale(self.locale())
            self.setWindowTitle("日记")
            self.WEEK_DAYS[:] = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            self.pb_daily.setText("日视图")
            self.pb_monthly.setText("月视图")
            self.pb_save.setText("保存")
            self.pb_export.setText("导出")
            self.pb_import.setText("导入")
            self.cb_autosave.setText("自动")
            self.lb_location.setText("地点")
            self.lb_weather.setText("天气")

    def add_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(self.logo_path))
        tray_menu = QMenu(self)
        action_show = QAction("Show/Hide", tray_menu)
        action_exit = QAction("Exit", tray_menu)
        action_show.triggered.connect(self.show_or_hide_window)
        action_exit.triggered.connect(self.close_window)
        tray_menu.addAction(action_show)
        tray_menu.addAction(action_exit)
        self.tray.setContextMenu(tray_menu)
        self.tray.setToolTip("Diary")
        self.tray.activated.connect(self.tray_activated)
        self.tray.show()

    def month_changed(self):
        self.date = QDate(self.calendar.yearShown(), self.calendar.monthShown(), 1)
        self.diaries = sqlutils.get_month_diary(self.date.year(), self.date.month())
        self.calendar.selectedDate()
        if self.view == self.VIEW_DAILY:
            self.update_daily_diary()
        else:
            self.update_monthly_diary()

    def date_changed(self):
        date = self.calendar.selectedDate()
        if self.date == date:
            return
        date_ori = self.date
        self.date = date
        if date_ori.year() != date.year() or date_ori.month() != date.month():
            self.diaries = sqlutils.get_month_diary(self.date.year(), self.date.month())
        if self.view == self.VIEW_DAILY:
            self.update_daily_diary()
        else:
            if date_ori.year() == date.year() and date_ori.month() == date.month():
                self.disconnect_all()
                for i in range(6):
                    for j in range(7):
                        item = self.tw_content.item(i, j)
                        item.setSelected(False)
                        if item.date == self.date:
                            item.setSelected(True)
                self.connect_all()
            else:
                self.update_monthly_diary()
        self.update_day_selected()

    def set_daily_view(self):
        self.view = self.VIEW_DAILY
        self.update_daily_diary()

    def set_monthly_view(self):
        self.view = self.VIEW_MONTHLY
        self.update_monthly_diary()

    def update_daily_diary(self):
        self.disconnect_all()
        tw = self.tw_content
        tw.setRowCount(1)
        tw.setColumnCount(1)
        tw.setHorizontalHeaderLabels((self.WEEK_DAYS[self.date.dayOfWeek() - 1],))
        diary = self.diaries.get(sqlutils.date2int(self.date.toPython()))
        item = tw.item(0, 0)
        if item is None:
            item = QTableWidgetItem()
            tw.setItem(0, 0, item)
        item.setText("")
        if diary is not None:
            item.setText(diary[0])
        item.setTextAlignment(Qt.AlignmentFlag.AlignTop & Qt.AlignmentFlag.AlignLeft)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEnabled)
        self.connect_all()

    def update_monthly_diary(self):
        self.disconnect_all()
        day_last = self.date
        day_first = QDate(self.date.year(), self.date.month(), 1)
        while day_last.addDays(1).month() == self.date.month():
            day_last = day_last.addDays(1)
        tw = self.tw_content
        tw.setRowCount(6)
        tw.setColumnCount(7)
        tw_labels = self.WEEK_DAYS[self.first_day_of_week - 1:] + self.WEEK_DAYS[:self.first_day_of_week - 1]
        tw.setHorizontalHeaderLabels(tw_labels)
        day = self.get_first_day_of_current_page()
        for i in range(6):
            for j in range(7):
                _id = sqlutils.date2int(day.toPython())
                item = tw.item(i, j)
                if item is None:
                    item = QTableWidgetItem()
                    tw.setItem(i, j, item)
                item.setText("")
                if _id in self.diaries:
                    item.setText(self.diaries[_id][0])
                item.setTextAlignment(Qt.AlignmentFlag.AlignTop & Qt.AlignmentFlag.AlignLeft)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEnabled)
                if day_first.daysTo(day) < 0 or day_last.daysTo(day) > 0:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                item.date = day
                day = day.addDays(1)
        self.connect_all()

    def update_day_selected(self):
        location = QLocale.countryToCode(self.locale().country())
        date_info = ""
        if location == "CN":
            date_info = utils.lunar_tostring(utils.solar_to_lunar(self.date.toPython()))
        holiday = utils.get_holiday(self.date.toPython(), location)
        if holiday is not None:
            if date_info:
                date_info += "\n"
            date_info += holiday
        self.lb_lunar.setText(date_info)
        diary = self.diaries.get(sqlutils.date2int(self.date.toPython()))
        if diary is None:
            self.le_location.setText("")
            self.le_weather.setText("")
        else:
            self.le_weather.setText(diary[1])
            self.le_location.setText(diary[2])

    def diary_selected_changed(self):
        if self.view == self.VIEW_DAILY:
            return
        self.disconnect_all()
        row = self.tw_content.currentRow()
        col = self.tw_content.currentColumn()
        day_first = self.get_first_day_of_current_page()
        current_day = day_first.addDays(row * 7 + col)
        self.date = current_day
        self.calendar.setSelectedDate(current_day)
        self.update_day_selected()
        self.connect_all()

    def get_first_day_of_current_page(self):
        day = QDate(self.date.year(), self.date.month(), 1)
        while day.dayOfWeek() != self.first_day_of_week:
            day = day.addDays(-1)
        return day

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

    def diary_edited(self):
        _id = sqlutils.date2int(self.date.toPython())
        if _id not in self.diaries:
            self.diaries[_id] = ["", "", ""]
        diary = self.diaries[_id]
        obj = self.sender()
        updated = False
        if obj == self.le_location:
            text_new = self.le_location.text()
            if diary[2] != text_new:
                updated = True
                diary[2] = text_new
        elif obj == self.le_weather:
            text_new = self.le_weather.text()
            if diary[1] != text_new:
                updated = True
                diary[1] = text_new
        else:
            tw = self.tw_content
            row = tw.currentRow()
            col = tw.currentColumn()
            item = tw.item(row, col)
            text_new = item.text()
            if diary[0] != text_new:
                updated = True
                diary[0] = text_new
        if self.cb_autosave.isChecked() and updated:
            sqlutils.update_diary(_id, diary)

    def btn_save(self):
        _id = sqlutils.date2int(self.date.toPython())
        if _id not in self.diaries:
            self.diaries[_id] = ["", "", ""]
        diary = self.diaries[_id]
        tw = self.tw_content
        row = tw.currentRow()
        col = tw.currentColumn()
        item = tw.item(row, col)
        text_new = item.text()
        if diary[0] != text_new:
            diary[0] = text_new
        sqlutils.update_diaries(self.diaries)

    def btn_export(self):
        file, _ = QFileDialog.getSaveFileName(self, "Export to xlsx file", "", filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            sqlutils.export_to_file(file)

    def btn_import(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Import from xlsx file [REPLACE!]", "", filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            sqlutils.import_from_file(file)
            self.month_changed()

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_or_hide_window()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.ignore()
                return self.hide()
        return super().changeEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_S:
            self.btn_save()
        else:
            return super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        return self.hide()

    def show_or_hide_window(self):
        if self.isHidden():
            if self.isMaximized():
                self.showMaximized()
            elif self.isMinimized():
                self.showNormal()
            else:
                self.show()
            self.activateWindow()
        else:
            self.hide()

    def close_window(self):
        sqlutils.close_connection()
        sys.exit(0)
