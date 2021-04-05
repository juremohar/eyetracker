# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindowUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QRunnable, QThreadPool
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow

from EyeTracker import *
import tobii_research as tr


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(350, 190, 21, 21))
        self.frame.setStyleSheet("\n background-color: rgb(126, 34, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.tracker = EyeTracker()
        self.tracker.start_tracking()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.moveDot)

        self.timer.start()

    def moveDot(self):

        coordinates = self.tracker.getAvgEyePos()
        x = 1920 * coordinates[0]
        y = 1080 * coordinates[1]
        self.centralwidget.move(x, y)
        # self.centralwidget.move(random.randint(0, 200), random.randint(0, 200))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

class UICalibrationCircle(QWidget):
    def __init__(self, parent=None):
        super(UICalibrationCircle, self).__init__(parent)

        self.circle = QLabel(self)
        self.circle.resize(30, 30)
        self.circle.setStyleSheet("border: 3px solid blue; border-radius: 40px;")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())