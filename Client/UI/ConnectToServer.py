# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConnectToServer.ui'
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

class Ui_ConnectToServer(object):
    def setupUi(self, ConnectToServer):
        if not ConnectToServer.objectName():
            ConnectToServer.setObjectName(u"ConnectToServer")
        ConnectToServer.resize(400, 300)
        self.layoutWidget = QWidget(ConnectToServer)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 401, 285))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.widget = QWidget(self.layoutWidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3, 0, Qt.AlignHCenter)

        self.lineEdit_IP = QLineEdit(self.widget)
        self.lineEdit_IP.setObjectName(u"lineEdit_IP")

        self.verticalLayout.addWidget(self.lineEdit_IP)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer_2)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2, 0, Qt.AlignHCenter)

        self.lineEdit_port = QLineEdit(self.widget)
        self.lineEdit_port.setObjectName(u"lineEdit_port")

        self.verticalLayout.addWidget(self.lineEdit_port)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)


        self.horizontalLayout_2.addWidget(self.widget)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)

        self.retranslateUi(ConnectToServer)

        QMetaObject.connectSlotsByName(ConnectToServer)
    # setupUi

    def retranslateUi(self, ConnectToServer):
        ConnectToServer.setWindowTitle(QCoreApplication.translate("ConnectToServer", u"Connect To Server", None))
        self.label_3.setText(QCoreApplication.translate("ConnectToServer", u"IP", None))
        self.lineEdit_IP.setText(QCoreApplication.translate("ConnectToServer", u"localhost", None))
        self.label_2.setText(QCoreApplication.translate("ConnectToServer", u"Port", None))
        self.lineEdit_port.setText(QCoreApplication.translate("ConnectToServer", u"4450", None))
        self.pushButton.setText(QCoreApplication.translate("ConnectToServer", u"Connect", None))
    # retranslateUi

