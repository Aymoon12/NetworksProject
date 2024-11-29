# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UploadFolder.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_UploadFolder(object):
    def setupUi(self, UploadFolder):
        if not UploadFolder.objectName():
            UploadFolder.setObjectName(u"UploadFolder")
        UploadFolder.resize(200, 100)
        UploadFolder.setMinimumSize(QSize(200, 100))
        UploadFolder.setMaximumSize(QSize(200, 100))
        self.horizontalLayout_3 = QHBoxLayout(UploadFolder)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(UploadFolder)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditFolderName = QLineEdit(UploadFolder)
        self.lineEditFolderName.setObjectName(u"lineEditFolderName")

        self.horizontalLayout.addWidget(self.lineEditFolderName)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButtonUpload = QPushButton(UploadFolder)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")

        self.horizontalLayout_2.addWidget(self.pushButtonUpload)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout)


        self.retranslateUi(UploadFolder)

        QMetaObject.connectSlotsByName(UploadFolder)
    # setupUi

    def retranslateUi(self, UploadFolder):
        UploadFolder.setWindowTitle(QCoreApplication.translate("UploadFolder", u"Add Folder", None))
        self.label.setText(QCoreApplication.translate("UploadFolder", u"Folder Name", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("UploadFolder", u"Upload", None))
    # retranslateUi

