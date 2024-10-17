# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QCommandLinkButton, QPushButton,
    QSizePolicy, QToolButton, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 571)
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(200, 250, 80, 23))
        self.toolButton = QToolButton(Widget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(480, 270, 24, 22))
        self.checkBox = QCheckBox(Widget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(250, 350, 83, 21))
        self.commandLinkButton = QCommandLinkButton(Widget)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        self.commandLinkButton.setGeometry(QRect(610, 440, 172, 41))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"PushButton", None))
        self.toolButton.setText(QCoreApplication.translate("Widget", u"...", None))
        self.checkBox.setText(QCoreApplication.translate("Widget", u"CheckBox", None))
        self.commandLinkButton.setText(QCoreApplication.translate("Widget", u"CommandLinkButton", None))
    # retranslateUi

