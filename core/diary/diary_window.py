import sys
import time

from core.diary import diary_utils
from core.diary.diary import Ui_Diary
from core.util.qt_utils import (BaseWindow, TextEdit, QKeyEvent, QIcon, QAction, QDate, Qt, QEvent,
                                QLocale, QMenu, QSystemTrayIcon, QFileDialog, QHeaderView, QPixmap, QApplication,
                                QMessageBox)
from core.util import utils, config_utils, dbconfig_utils
from core.util.i18n_utils import tr


class DiaryWindow(Ui_Diary, BaseWindow):
    VIEW_DAILY = 0
    VIEW_MONTHLY = 1

    def __init__(self):
        BaseWindow.__init__(self)
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
            (self.pb_exp.clicked, self.btn_export),
            (self.pb_imp.clicked, self.btn_import),
            (self.cb_autosave.clicked, self.cb_autosave_changed),
        )
        self.init()
        self.connect_all()

    def init(self):
        self.time_logined = time.time()
        self.logo_path = utils.get_path(config_utils.load_config("style", "logo"))
        self.expired = int(config_utils.load_config("global", "login_expired"))
        self.show_lunar = int(config_utils.load_config("global", "show_lunar"))
        self.show_bill = int(config_utils.load_config("global", "show_bill"))
        self.show_interest = int(config_utils.load_config("global", "show_interest"))
        self.show_note = int(config_utils.load_config("global", "show_note"))
        self.setWindowIcon(QIcon(self.logo_path))
        self.pb_imp.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_imp"))))
        self.pb_exp.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_exp"))))
        self.pb_save.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_save"))))
        self.pb_monthly.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_month"))))
        self.pb_daily.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_day"))))
        icon_weather = QPixmap(utils.get_path(
            config_utils.load_config("style", "icon_weather")))
        icon_location = QPixmap(utils.get_path(
            config_utils.load_config("style", "icon_location")))
        self.lb_weather.setFixedSize(25, 25)
        self.lb_location.setFixedSize(20, 20)
        self.lb_weather.setPixmap(icon_weather.scaled(self.lb_weather.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.lb_location.setPixmap(icon_location.scaled(self.lb_location.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.WEEK_DAYS = [tr(day) for day in (
            "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")]
        self.add_tray()
        self.cb_autosave.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_auto"))))
        # self.cb_autosave.setText(tr("AUTO"))
        # self.lb_location.setText(tr("location"))
        # self.lb_weather.setText(tr("whether"))
        self.action_diary.setText(tr("Diary"))
        self.action_interest.setText(tr("Interest"))
        self.action_bill.setText(tr("Bill"))
        self.action_note.setText(tr("Note"))
        self.action_exit.setText(tr("Exit"))

        self.window_last = self
        self.window_interest = None
        self.window_bill = None
        self.window_note = None
        self.pb_save.setHidden(True)
        self.tw_content.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tw_content.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        first_day_of_week = int(config_utils.load_config("global", "first_day_of_week")) % 7
        if first_day_of_week == 0:
            first_day_of_week += 7
        self.first_day_of_week = first_day_of_week
        self.last_day_of_week = first_day_of_week + \
            6 if first_day_of_week < 2 else first_day_of_week - 1
        self.calendar.setFirstDayOfWeek(Qt.DayOfWeek(first_day_of_week))
        self.date = QDate.currentDate()
        self.diaries = diary_utils.get_month_diary(self.date.year(), self.date.month())
        self.calendar.setSelectedDate(self.date)
        self.set_daily_view()
        self.update_day_selected()

    def cb_autosave_changed(self):
        self.pb_save.setHidden(self.cb_autosave.isChecked())

    def add_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(self.logo_path))
        tray_menu = QMenu(self)
        tray_menu.setStyleSheet("QMenu{color:black; background:white;\
                                selection-background-color:#e4e4e4;\
                                font-family:Arial,Microsoft YaHei; font-size:15px;}\
                                QMenu::item {color: black;}")

        self.action_diary = QAction("&Diary", tray_menu)
        self.action_interest = QAction("&Interest", tray_menu)
        self.action_bill = QAction("&Bill", tray_menu)
        self.action_note = QAction("&Note", tray_menu)
        self.action_exit = QAction("&Exit", tray_menu)

        self.action_diary.setIcon(QIcon(self.logo_path))
        self.action_interest.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_interest"))))
        self.action_bill.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_bill"))))
        self.action_note.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_note"))))
        self.action_exit.setIcon(QIcon(utils.get_path(
            config_utils.load_config("style", "icon_exit"))))

        self.action_diary.triggered.connect(self.show_or_hide_window)
        self.action_interest.triggered.connect(self.open_interest_window)
        self.action_bill.triggered.connect(self.open_bill_window)
        self.action_note.triggered.connect(self.open_note_window)
        self.action_exit.triggered.connect(self.close_window)

        tray_menu.addAction(self.action_diary)
        if self.show_interest:
            tray_menu.addAction(self.action_interest)
        if self.show_bill:
            tray_menu.addAction(self.action_bill)
        if self.show_note:
            tray_menu.addAction(self.action_note)
        tray_menu.addSeparator()
        tray_menu.addAction(self.action_exit)

        self.tray.setContextMenu(tray_menu)
        self.tray.setToolTip(tr("Diary"))
        self.tray.activated.connect(self.tray_activated)
        self.tray.show()

    def month_changed(self):
        self.date = QDate(self.calendar.yearShown(),
                          self.calendar.monthShown(), 1)
        self.diaries = diary_utils.get_month_diary(
            self.date.year(), self.date.month())
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
            self.diaries = diary_utils.get_month_diary(
                self.date.year(), self.date.month())
        if self.view == self.VIEW_DAILY:
            self.update_daily_diary()
        else:
            if date_ori.year() == date.year() and date_ori.month() == date.month():
                self.disconnect_all()
                for row in range(6):
                    for col in range(7):
                        te = self.tw_content.get_text(row, col)
                        if te.date == self.date:
                            te.setFocus()
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
        tw.setHorizontalHeaderLabels(
            (self.WEEK_DAYS[self.date.dayOfWeek() - 1],))
        diary = self.diaries.get(utils.date2int(self.date.toPython()))
        te = tw.get_text(0, 0)
        self.reconnect(te.focusOut, self.diary_edited)
        te.setPlainText("")
        te.setEnabled(True)
        te.setStyleSheet("background-color: transparent;")
        if diary is not None:
            te.setPlainText(diary.content)
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
        tw_labels = self.WEEK_DAYS[self.first_day_of_week -
                                   1:] + self.WEEK_DAYS[:self.first_day_of_week - 1]
        tw.setHorizontalHeaderLabels(tw_labels)
        day = self.get_first_day_of_current_page()
        for row in range(6):
            for col in range(7):
                _id = utils.date2int(day.toPython())
                te = tw.get_text(row, col)
                self.reconnect(te.focusOut, self.diary_edited)
                te.setPlainText("")
                if _id in self.diaries:
                    te.setPlainText(self.diaries[_id].content)
                te.setEnabled(True)
                te.setStyleSheet("background-color: transparent;")
                if day_first.daysTo(day) < 0 or day_last.daysTo(day) > 0:
                    te.setEnabled(False)
                    te.setStyleSheet("background-color: grey;")
                te.date = day
                day = day.addDays(1)
        self.connect_all()

    def update_day_selected(self):
        location = config_utils.load_config(
            "global", "location") or QLocale.countryToCode(self.locale().country())
        date_info = ""
        if location == "CN":
            date_info = utils.lunar_string(self.date.toPython())
        holiday = utils.get_holiday(self.date.toPython(), location)
        if holiday is not None:
            if date_info:
                date_info += "\n"
            date_info += holiday
        self.lb_lunar.setText(date_info)
        diary = self.diaries.get(utils.date2int(self.date.toPython()))
        if diary is None:
            self.le_location.setText("")
            self.le_weather.setText("")
        else:
            self.le_weather.setText(diary.weather)
            self.le_location.setText(diary.location)

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
        n = 0
        while day.dayOfWeek() != self.first_day_of_week:
            day = day.addDays(-1)
            n += 1
        if n == 0:
            day = day.addDays(-7)
        return day

    def diary_edited(self):
        _id = utils.date2int(self.date.toPython())
        if _id not in self.diaries:
            self.diaries[_id] = diary_utils.Diary(_id)
        diary = self.diaries[_id]
        obj = self.sender()
        updated = False
        if obj == self.le_location:
            text_new = self.le_location.text()
            if diary.location != text_new:
                updated = True
                diary.location = text_new
        elif obj == self.le_weather:
            text_new = self.le_weather.text()
            if diary.weather != text_new:
                updated = True
                diary.weather = text_new
        else:
            te: TextEdit = obj
            text_new = te.toPlainText()
            if diary.content != text_new:
                updated = True
                diary.content = text_new
        if self.cb_autosave.isChecked() and updated:
            self.start_task(diary_utils.update_diary, (diary,))

    def btn_save(self):
        _id = utils.date2int(self.date.toPython())
        if _id not in self.diaries:
            self.diaries[_id] = diary_utils.Diary(_id)
        diary = self.diaries[_id]
        tw = self.tw_content
        row = tw.currentRow()
        col = tw.currentColumn()
        te = tw.get_text(row, col)
        self.reconnect(te.focusOut, self.diary_edited)
        text_new = te.toPlainText()
        if diary.content != text_new:
            diary.content = text_new
        self.start_task(diary_utils.update_diaries, (self.diaries,))

    def btn_export(self):
        file, _ = QFileDialog.getSaveFileName(self, tr(
            "Export to xlsx file"), "", filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            diary_utils.exp(file)

    def btn_import(self):
        file, _ = QFileDialog.getOpenFileName(
            self, tr("Import from xlsx file [REPLACE!]"), "", filter="Excel File (*.xlsx);; All Files (*);")
        if file:
            diary_utils.imp(file)
            self.month_changed()

    def login_expired(self):
        if self.expired > 0:
            self.tray.setVisible(False)
            if time.time() - self.time_logined > self.expired:
                if not dbconfig_utils.login(max_input=1):
                    self.tray.setVisible(True)
                    return True
                self.time_logined = time.time()
        self.tray.setVisible(True)
        return False

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.open_last_window()

    def open_last_window(self):
        ui_default = config_utils.load_config("global", "ui_default", "none")
        if ui_default == "bill":
            self.open_bill_window()
        elif ui_default == "diary":
            self.show_or_hide_window()
        elif ui_default == "interest":
            self.open_interest_window()
        elif ui_default == "note":
            self.open_note_window()
        else:
            if self.window_last == self:
                self.show_or_hide_window()
            elif self.window_last == self.window_bill:
                self.open_bill_window()
            elif self.window_last == self.window_interest:
                self.open_interest_window()
            elif self.window_last == self.window_note:
                self.open_note_window()

    def open_interest_window(self):
        if self.window_interest is None:
            from core.interest.interest_window import InterestWindow
            self.window_interest = InterestWindow()
        if self.window_interest.isHidden():
            if self.login_expired():
                return
            if self.window_interest.isMaximized():
                self.window_interest.showMaximized()
            elif self.window_interest.isMinimized():
                self.window_interest.showNormal()
            else:
                self.window_interest.show()
            self.window_interest.activateWindow()
        else:
            self.window_interest.hide()
        self.window_last = self.window_interest

    def open_bill_window(self):
        if self.window_bill is None:
            from core.bill.bill_window import BillWindow
            self.window_bill = BillWindow()
        if self.window_bill.isHidden():
            if self.login_expired():
                return
            if self.window_bill.isMaximized():
                self.window_bill.showMaximized()
            elif self.window_bill.isMinimized():
                self.window_bill.showNormal()
            else:
                self.window_bill.show()
            self.window_bill.activateWindow()
        else:
            self.window_bill.hide()
        self.window_last = self.window_bill

    def open_note_window(self):
        if self.window_note is None:
            from core.note.note_window import NoteWindow
            self.window_note = NoteWindow()
        if self.window_note.isHidden():
            if self.login_expired():
                return
            if self.window_note.isMaximized():
                self.window_note.showMaximized()
            elif self.window_note.isMinimized():
                self.window_note.showNormal()
            else:
                self.window_note.show()
            self.window_note.activateWindow()
        else:
            self.window_note.hide()
        QApplication.processEvents()
        self.window_note.update_table_note()
        self.window_last = self.window_note

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_S:
                self.btn_save()
            elif event.key() == Qt.Key.Key_I:
                if self.show_interest:
                    self.open_interest_window()
            elif event.key() == Qt.Key.Key_B:
                if self.show_bill:
                    self.open_bill_window()
            elif event.key() == Qt.Key.Key_N:
                if self.show_note:
                    self.open_note_window()
            elif event.key() == Qt.Key.Key_M:
                self.set_monthly_view()
            elif event.key() == Qt.Key.Key_D:
                self.set_daily_view()
            elif event.key() == Qt.Key.Key_P:
                dbconfig_utils.change_pwd()
        else:
            return super().keyPressEvent(event)

    def closeEvent(self, event):
        event.ignore()
        return self.hide()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.ignore()
                self.hide()
                return
        return super().changeEvent(event)

    def show_or_hide_window(self):
        if self.isHidden():
            if self.login_expired():
                return
            if self.isMaximized():
                self.showMaximized()
            elif self.isMinimized():
                self.showNormal()
            else:
                self.show()
            self.activateWindow()
        else:
            self.hide()
        self.window_last = self

    def close_window(self):
        confirm_at_exit = int(config_utils.load_config("global", "confirm_at_exit"))
        if confirm_at_exit:
            ok_pressed = QMessageBox.question(self, tr("Exit Program"), tr("Are you sure to exit program?"),
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if ok_pressed == QMessageBox.No:
                return
        sys.exit()
