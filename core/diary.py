# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'diary.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCalendarWidget, QCheckBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Diary(object):
    def setupUi(self, Diary):
        if not Diary.objectName():
            Diary.setObjectName(u"Diary")
        Diary.resize(1000, 600)
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(12)
        Diary.setFont(font)
        Diary.setLocale(QLocale(QLocale.Chinese, QLocale.China))
        self.actionEXPORT = QAction(Diary)
        self.actionEXPORT.setObjectName(u"actionEXPORT")
        self.actionIMPORT = QAction(Diary)
        self.actionIMPORT.setObjectName(u"actionIMPORT")
        self.centralwidget = QWidget(Diary)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.calendar = QCalendarWidget(self.centralwidget)
        self.calendar.setObjectName(u"calendar")
        self.calendar.setMinimumSize(QSize(400, 400))
        self.calendar.setMaximumSize(QSize(400, 400))
        self.calendar.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.calendar.setSelectedDate(QDate(2024, 3, 8))
        self.calendar.setFirstDayOfWeek(Qt.Sunday)
        self.calendar.setGridVisible(False)
        self.calendar.setSelectionMode(QCalendarWidget.SingleSelection)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setNavigationBarVisible(True)
        self.calendar.setDateEditAcceptDelay(200)

        self.verticalLayout.addWidget(self.calendar)

        self.lb_lunar = QLabel(self.centralwidget)
        self.lb_lunar.setObjectName(u"lb_lunar")

        self.verticalLayout.addWidget(self.lb_lunar)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.cb_autosave = QCheckBox(self.centralwidget)
        self.cb_autosave.setObjectName(u"cb_autosave")
        self.cb_autosave.setChecked(True)

        self.horizontalLayout_4.addWidget(self.cb_autosave)

        self.pb_save = QPushButton(self.centralwidget)
        self.pb_save.setObjectName(u"pb_save")
        self.pb_save.setStyleSheet(u"")
        self.pb_save.setFlat(False)

        self.horizontalLayout_4.addWidget(self.pb_save)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.pb_export = QPushButton(self.centralwidget)
        self.pb_export.setObjectName(u"pb_export")

        self.horizontalLayout_4.addWidget(self.pb_export)

        self.pb_import = QPushButton(self.centralwidget)
        self.pb_import.setObjectName(u"pb_import")

        self.horizontalLayout_4.addWidget(self.pb_import)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lb_weather = QLabel(self.centralwidget)
        self.lb_weather.setObjectName(u"lb_weather")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_weather.sizePolicy().hasHeightForWidth())
        self.lb_weather.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.lb_weather)

        self.le_weather = QLineEdit(self.centralwidget)
        self.le_weather.setObjectName(u"le_weather")
        self.le_weather.setMaximumSize(QSize(100, 16777215))
        self.le_weather.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.le_weather)

        self.lb_location = QLabel(self.centralwidget)
        self.lb_location.setObjectName(u"lb_location")
        sizePolicy.setHeightForWidth(self.lb_location.sizePolicy().hasHeightForWidth())
        self.lb_location.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.lb_location)

        self.le_location = QLineEdit(self.centralwidget)
        self.le_location.setObjectName(u"le_location")
        self.le_location.setMaximumSize(QSize(100, 16777215))
        self.le_location.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.le_location)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pb_monthly = QPushButton(self.centralwidget)
        self.pb_monthly.setObjectName(u"pb_monthly")
        self.pb_monthly.setStyleSheet(u"")
        self.pb_monthly.setFlat(False)

        self.horizontalLayout_2.addWidget(self.pb_monthly)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.pb_daily = QPushButton(self.centralwidget)
        self.pb_daily.setObjectName(u"pb_daily")
        self.pb_daily.setStyleSheet(u"")
        self.pb_daily.setFlat(False)

        self.horizontalLayout_2.addWidget(self.pb_daily)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.tw_content = QTableWidget(self.centralwidget)
        self.tw_content.setObjectName(u"tw_content")
        self.tw_content.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tw_content.horizontalHeader().setStretchLastSection(True)
        self.tw_content.verticalHeader().setVisible(False)
        self.tw_content.verticalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.tw_content)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout.setStretch(1, 1)
        Diary.setCentralWidget(self.centralwidget)

        self.retranslateUi(Diary)

        self.pb_save.setDefault(False)
        self.pb_monthly.setDefault(False)
        self.pb_daily.setDefault(False)


        QMetaObject.connectSlotsByName(Diary)
    # setupUi

    def retranslateUi(self, Diary):
        Diary.setWindowTitle(QCoreApplication.translate("Diary", u"DIARY", None))
        self.actionEXPORT.setText(QCoreApplication.translate("Diary", u"EXPORT", None))
        self.actionIMPORT.setText(QCoreApplication.translate("Diary", u"IMPORT", None))
        self.lb_lunar.setText("")
        self.cb_autosave.setText(QCoreApplication.translate("Diary", u"AUTO", None))
        self.pb_save.setText(QCoreApplication.translate("Diary", u"SAVE", None))
        self.pb_export.setText(QCoreApplication.translate("Diary", u"EXP", None))
        self.pb_import.setText(QCoreApplication.translate("Diary", u"IMP", None))
        self.lb_weather.setText(QCoreApplication.translate("Diary", u"whether:", None))
        self.lb_location.setText(QCoreApplication.translate("Diary", u"location:", None))
        self.pb_monthly.setText(QCoreApplication.translate("Diary", u"MONTH", None))
        self.label_2.setText(QCoreApplication.translate("Diary", u"/", None))
        self.pb_daily.setText(QCoreApplication.translate("Diary", u"DAILY", None))
    # retranslateUi

