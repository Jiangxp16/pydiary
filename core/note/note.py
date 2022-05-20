# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'note.ui'
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

class Ui_Note(object):
    def setupUi(self, Note):
        if not Note.objectName():
            Note.setObjectName(u"Note")
        Note.resize(800, 800)
        self.centralwidget = QWidget(Note)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.hs_sort = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.hs_sort)

        self.cb_state = QComboBox(self.centralwidget)
        self.cb_state.setObjectName(u"cb_state")

        self.horizontalLayout_2.addWidget(self.cb_state)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tw_note = QTableWidget(self.centralwidget)
        self.tw_note.setObjectName(u"tw_note")
        self.tw_note.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.tw_note.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_note.setTextElideMode(Qt.ElideNone)
        self.tw_note.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_note.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_note.setSortingEnabled(True)
        self.tw_note.horizontalHeader().setCascadingSectionResizes(True)
        self.tw_note.horizontalHeader().setDefaultSectionSize(60)
        self.tw_note.horizontalHeader().setProperty("showSortIndicator", False)
        self.tw_note.horizontalHeader().setStretchLastSection(True)
        self.tw_note.verticalHeader().setVisible(True)

        self.verticalLayout.addWidget(self.tw_note)

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

        Note.setCentralWidget(self.centralwidget)

        self.retranslateUi(Note)

        QMetaObject.connectSlotsByName(Note)
    # setupUi

    def retranslateUi(self, Note):
        Note.setWindowTitle(QCoreApplication.translate("Note", u"NOTE", None))
        self.le_filter.setPlaceholderText(QCoreApplication.translate("Note", u"Search here.", None))
#if QT_CONFIG(tooltip)
        self.pb_imp.setToolTip(QCoreApplication.translate("Note", u"Ctrl+I: Import", None))
#endif // QT_CONFIG(tooltip)
        self.pb_imp.setText("")
#if QT_CONFIG(tooltip)
        self.pb_exp.setToolTip(QCoreApplication.translate("Note", u"Ctrl+E: Export", None))
#endif // QT_CONFIG(tooltip)
        self.pb_exp.setText("")
#if QT_CONFIG(tooltip)
        self.pb_add.setToolTip(QCoreApplication.translate("Note", u"Ctrl+N", None))
#endif // QT_CONFIG(tooltip)
        self.pb_add.setText("")
#if QT_CONFIG(tooltip)
        self.pb_del.setToolTip(QCoreApplication.translate("Note", u"Ctrl+D", None))
#endif // QT_CONFIG(tooltip)
        self.pb_del.setText("")
    # retranslateUi

