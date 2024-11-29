# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Preferences.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        if not Preferences.objectName():
            Preferences.setObjectName(u"Preferences")
        Preferences.resize(200, 100)
        Preferences.setMinimumSize(QSize(200, 100))
        Preferences.setMaximumSize(QSize(200, 100))
        self.verticalLayout = QVBoxLayout(Preferences)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBoxDarkMode = QCheckBox(Preferences)
        self.checkBoxDarkMode.setObjectName(u"checkBoxDarkMode")

        self.verticalLayout.addWidget(self.checkBoxDarkMode)

        self.pushButtonSavePreferences = QPushButton(Preferences)
        self.pushButtonSavePreferences.setObjectName(u"pushButtonSavePreferences")

        self.verticalLayout.addWidget(self.pushButtonSavePreferences)


        self.retranslateUi(Preferences)

        QMetaObject.connectSlotsByName(Preferences)
    # setupUi

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle(QCoreApplication.translate("Preferences", u"Preferences", None))
        self.checkBoxDarkMode.setText(QCoreApplication.translate("Preferences", u"Dark Mode", None))
        self.pushButtonSavePreferences.setText(QCoreApplication.translate("Preferences", u"Save Preferences", None))
    # retranslateUi

