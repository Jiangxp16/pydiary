# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bill.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QDoubleSpinBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Bill(object):
    def setupUi(self, Bill):
        if not Bill.objectName():
            Bill.setObjectName(u"Bill")
        Bill.resize(600, 800)
        self.centralwidget = QWidget(Bill)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.hs_sort = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.hs_sort)

        self.sb_start = QSpinBox(self.centralwidget)
        self.sb_start.setObjectName(u"sb_start")
        self.sb_start.setAlignment(Qt.AlignCenter)
        self.sb_start.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.sb_start.setMaximum(99999999)
        self.sb_start.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.horizontalLayout_2.addWidget(self.sb_start)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.sb_end = QSpinBox(self.centralwidget)
        self.sb_end.setObjectName(u"sb_end")
        self.sb_end.setAlignment(Qt.AlignCenter)
        self.sb_end.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.sb_end.setMaximum(99999999)
        self.sb_end.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.horizontalLayout_2.addWidget(self.sb_end)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tw_bill = QTableWidget(self.centralwidget)
        self.tw_bill.setObjectName(u"tw_bill")
        self.tw_bill.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.tw_bill.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_bill.setTextElideMode(Qt.ElideNone)
        self.tw_bill.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_bill.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_bill.setSortingEnabled(True)
        self.tw_bill.horizontalHeader().setCascadingSectionResizes(True)
        self.tw_bill.horizontalHeader().setDefaultSectionSize(60)
        self.tw_bill.horizontalHeader().setProperty("showSortIndicator", False)
        self.tw_bill.horizontalHeader().setStretchLastSection(True)
        self.tw_bill.verticalHeader().setVisible(True)

        self.verticalLayout.addWidget(self.tw_bill)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lb_total = QLabel(self.centralwidget)
        self.lb_total.setObjectName(u"lb_total")

        self.horizontalLayout.addWidget(self.lb_total)

        self.dsb_total = QDoubleSpinBox(self.centralwidget)
        self.dsb_total.setObjectName(u"dsb_total")
        self.dsb_total.setAlignment(Qt.AlignCenter)
        self.dsb_total.setReadOnly(True)
        self.dsb_total.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.dsb_total.setMinimum(-99999999.000000000000000)
        self.dsb_total.setMaximum(99999999.000000000000000)

        self.horizontalLayout.addWidget(self.dsb_total)

        self.le_filter = QLineEdit(self.centralwidget)
        self.le_filter.setObjectName(u"le_filter")
        self.le_filter.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout.addWidget(self.le_filter)

        self.hs_operate = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.hs_operate)

        self.pb_imp = QPushButton(self.centralwidget)
        self.pb_imp.setObjectName(u"pb_imp")
        self.pb_imp.setMinimumSize(QSize(40, 0))
        self.pb_imp.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.pb_imp)

        self.pb_exp = QPushButton(self.centralwidget)
        self.pb_exp.setObjectName(u"pb_exp")
        self.pb_exp.setMinimumSize(QSize(40, 0))
        self.pb_exp.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.pb_exp)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.pb_add = QPushButton(self.centralwidget)
        self.pb_add.setObjectName(u"pb_add")
        self.pb_add.setMinimumSize(QSize(40, 0))
        self.pb_add.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.pb_add)

        self.pb_del = QPushButton(self.centralwidget)
        self.pb_del.setObjectName(u"pb_del")
        self.pb_del.setMinimumSize(QSize(40, 0))
        self.pb_del.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.pb_del)


        self.verticalLayout.addLayout(self.horizontalLayout)

        Bill.setCentralWidget(self.centralwidget)

        self.retranslateUi(Bill)

        QMetaObject.connectSlotsByName(Bill)
    # setupUi

    def retranslateUi(self, Bill):
        Bill.setWindowTitle(QCoreApplication.translate("Bill", u"Bill", None))
        self.label.setText(QCoreApplication.translate("Bill", u"~", None))
        self.lb_total.setText(QCoreApplication.translate("Bill", u"Total:", None))
        self.le_filter.setPlaceholderText(QCoreApplication.translate("Bill", u"Search here.", None))
#if QT_CONFIG(tooltip)
        self.pb_imp.setToolTip(QCoreApplication.translate("Bill", u"Ctrl+I: IMPORT", None))
#endif // QT_CONFIG(tooltip)
        self.pb_imp.setText("")
#if QT_CONFIG(tooltip)
        self.pb_exp.setToolTip(QCoreApplication.translate("Bill", u"Ctrl+E: EXPORT", None))
#endif // QT_CONFIG(tooltip)
        self.pb_exp.setText("")
#if QT_CONFIG(tooltip)
        self.pb_add.setToolTip(QCoreApplication.translate("Bill", u"Ctrl+N", None))
#endif // QT_CONFIG(tooltip)
        self.pb_add.setText("")
#if QT_CONFIG(tooltip)
        self.pb_del.setToolTip(QCoreApplication.translate("Bill", u"Ctrl+D", None))
#endif // QT_CONFIG(tooltip)
        self.pb_del.setText("")
    # retranslateUi

