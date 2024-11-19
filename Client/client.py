from main_window import MainWindow
import sys
from PySide6 import QtCore, QtWidgets, QtGui


if(__name__ == '__main__'):
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(800,600)
    main_window.show()

    app.exec()