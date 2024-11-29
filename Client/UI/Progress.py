# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Progress.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Progress(object):
    def setupUi(self, Progress):
        if not Progress.objectName():
            Progress.setObjectName(u"Progress")
        Progress.resize(200, 79)
        Progress.setMinimumSize(QSize(200, 75))
        Progress.setMaximumSize(QSize(200, 79))
        self.verticalLayout = QVBoxLayout(Progress)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelType = QLabel(Progress)
        self.labelType.setObjectName(u"labelType")

        self.verticalLayout.addWidget(self.labelType)

        self.labelKb = QLabel(Progress)
        self.labelKb.setObjectName(u"labelKb")

        self.verticalLayout.addWidget(self.labelKb)

        self.progressBar = QProgressBar(Progress)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)


        self.retranslateUi(Progress)

        QMetaObject.connectSlotsByName(Progress)
    # setupUi

    def retranslateUi(self, Progress):
        Progress.setWindowTitle(QCoreApplication.translate("Progress", u"Progress", None))
        self.labelType.setText(QCoreApplication.translate("Progress", u"Uploading", None))
        self.labelKb.setText(QCoreApplication.translate("Progress", u"0 Kb", None))
    # retranslateUi

