# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interest.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Interest(object):
    def setupUi(self, Interest):
        if not Interest.objectName():
            Interest.setObjectName(u"Interest")
        Interest.resize(1280, 720)
        self.centralwidget = QWidget(Interest)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.hs_sort = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.hs_sort)

        self.cb_sort = QComboBox(self.centralwidget)
        self.cb_sort.setObjectName(u"cb_sort")

        self.horizontalLayout_2.addWidget(self.cb_sort)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tw_interest = QTableWidget(self.centralwidget)
        self.tw_interest.setObjectName(u"tw_interest")
        self.tw_interest.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.tw_interest.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_interest.setTextElideMode(Qt.ElideNone)
        self.tw_interest.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_interest.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_interest.setSortingEnabled(True)
        self.tw_interest.horizontalHeader().setCascadingSectionResizes(True)
        self.tw_interest.horizontalHeader().setDefaultSectionSize(60)
        self.tw_interest.horizontalHeader().setProperty("showSortIndicator", False)
        self.tw_interest.horizontalHeader().setStretchLastSection(True)
        self.tw_interest.verticalHeader().setVisible(True)

        self.verticalLayout.addWidget(self.tw_interest)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
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

        Interest.setCentralWidget(self.centralwidget)

        self.retranslateUi(Interest)

        QMetaObject.connectSlotsByName(Interest)
    # setupUi

    def retranslateUi(self, Interest):
        Interest.setWindowTitle(QCoreApplication.translate("Interest", u"INTEREST", None))
        self.le_filter.setPlaceholderText(QCoreApplication.translate("Interest", u"Search here.", None))
#if QT_CONFIG(tooltip)
        self.pb_imp.setToolTip(QCoreApplication.translate("Interest", u"Ctrl+I: IMPORT", None))
#endif // QT_CONFIG(tooltip)
        self.pb_imp.setText("")
#if QT_CONFIG(tooltip)
        self.pb_exp.setToolTip(QCoreApplication.translate("Interest", u"Ctrl+E: EXPORT", None))
#endif // QT_CONFIG(tooltip)
        self.pb_exp.setText("")
#if QT_CONFIG(tooltip)
        self.pb_add.setToolTip(QCoreApplication.translate("Interest", u"Ctrl+N", None))
#endif // QT_CONFIG(tooltip)
        self.pb_add.setText("")
#if QT_CONFIG(tooltip)
        self.pb_del.setToolTip(QCoreApplication.translate("Interest", u"Ctrl+D", None))
#endif // QT_CONFIG(tooltip)
        self.pb_del.setText("")
    # retranslateUi

