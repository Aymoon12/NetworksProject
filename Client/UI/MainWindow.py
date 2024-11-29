# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QSpacerItem, QStatusBar,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setMaximumSize(QSize(800, 600))
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionSign_Up = QAction(MainWindow)
        self.actionSign_Up.setObjectName(u"actionSign_Up")
        self.actionSign_Up.setEnabled(False)
        self.actionLog_In = QAction(MainWindow)
        self.actionLog_In.setObjectName(u"actionLog_In")
        self.actionLog_In.setEnabled(False)
        self.actionConnect_to_Server = QAction(MainWindow)
        self.actionConnect_to_Server.setObjectName(u"actionConnect_to_Server")
        self.actionConnect_to_Server.setEnabled(True)
        self.actionUploadFile = QAction(MainWindow)
        self.actionUploadFile.setObjectName(u"actionUploadFile")
        self.actionUploadFile.setEnabled(False)
        icon = QIcon()
        icon.addFile(u"Icons/upload.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionUploadFile.setIcon(icon)
        self.actionCreateSubfolder = QAction(MainWindow)
        self.actionCreateSubfolder.setObjectName(u"actionCreateSubfolder")
        self.actionCreateSubfolder.setEnabled(False)
        icon1 = QIcon()
        icon1.addFile(u"Icons/folder-plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionCreateSubfolder.setIcon(icon1)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAccount = QMenu(self.menuFile)
        self.menuAccount.setObjectName(u"menuAccount")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menuFile.addAction(self.actionConnect_to_Server)
        self.menuFile.addAction(self.menuAccount.menuAction())
        self.menuAccount.addAction(self.actionSign_Up)
        self.menuAccount.addAction(self.actionLog_In)
        self.menuEdit.addAction(self.actionPreferences)
        self.toolBar.addAction(self.actionUploadFile)
        self.toolBar.addAction(self.actionCreateSubfolder)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"File Transmission Client", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.actionSign_Up.setText(QCoreApplication.translate("MainWindow", u"Sign Up", None))
        self.actionLog_In.setText(QCoreApplication.translate("MainWindow", u"Log In", None))
        self.actionConnect_to_Server.setText(QCoreApplication.translate("MainWindow", u"Connect to Server", None))
        self.actionUploadFile.setText(QCoreApplication.translate("MainWindow", u"UploadFile", None))
#if QT_CONFIG(tooltip)
        self.actionUploadFile.setToolTip(QCoreApplication.translate("MainWindow", u"Upload a file to the server", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionUploadFile.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+U", None))
#endif // QT_CONFIG(shortcut)
        self.actionCreateSubfolder.setText(QCoreApplication.translate("MainWindow", u"CreateSubfolder", None))
#if QT_CONFIG(tooltip)
        self.actionCreateSubfolder.setToolTip(QCoreApplication.translate("MainWindow", u"Create a subfolder on the server", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionCreateSubfolder.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Current Folder: /", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuAccount.setTitle(QCoreApplication.translate("MainWindow", u"Account", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

