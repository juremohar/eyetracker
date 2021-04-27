import sys

from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from EyeTracker import *
from Analysis import *
from TestSentence import *

import helpers

widthScreen = 1920
heightScreen = 1080


class UIMenu(QWidget):
    def __init__(self, parent=None):
        super(UIMenu, self).__init__(parent)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignCenter)

        self.startBtn = QPushButton('Start First Level', self)
        # self.startBtn.move(960, 540)

        self.calibrateBtn = QPushButton('Start calibrate', self)
        # self.calibrateBtn.move(960, 580)
        self.vbox.addWidget(self.startBtn)
        self.vbox.addWidget(self.calibrateBtn)
        self.setLayout(self.vbox)


class UIDotTracker(QWidget):
    def __init__(self, parent=None):
        super(UIDotTracker, self).__init__(parent)

        self.dot = UICalibrationCircle(self)
        self.dot.move(300, 300)

        self.testSentence = UITestSentence(self)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignCenter)
        # self.vbox.addWidget(self.testWord)
        self.vbox.addWidget(self.testSentence.testSentence)

        self.setLayout(self.vbox)

        self.tracker = EyeTracker()
        self.tracker.start_tracking()

        self.analysis = Analysis()

        self.timer = QTimer()
        self.timer.setInterval(350)
        self.timer.timeout.connect(self.moveDot)

        self.timer.start()

    def moveDot(self):
        coordinates = self.tracker.getAvgEyePos()
        x = widthScreen * coordinates[0]
        y = heightScreen * coordinates[1]

        self.dot.move(x, y)

        word = helpers.gazeOnWord(self.testSentence.wordMapping, x, y)
        self.analysis.addWordToWordOrder(word)
        self.analysis.printWordOrder()


class UICalibrationCircle(QWidget):
    def __init__(self, parent=None):
        super(UICalibrationCircle, self).__init__(parent)

        self.circle = QLabel(self)
        self.circle.resize(30, 30)
        self.circle.setStyleSheet("border: 3px solid blue; border-radius: 40px;")


class UICalibrate(QWidget):
    currentIndex = 0
    points_to_calibrate = [(0.1, 0.1), (0.1, 0.5), (0.1, 0.9), (0.5, 0.1), (0.5, 0.5), (0.5, 0.9), (0.9, 0.1),
                           (0.9, 0.5), (0.9, 0.9)]
    currentPoint = None
    calibration = None

    def __init__(self, parent=None):
        super(UICalibrate, self).__init__(parent)

        self.currentPoint = UICalibrationCircle(self)
        self.currentPoint.hide()

        self.backBtn = QPushButton('Back', self)
        self.backBtn.move(640, 480)

        self.dot = QtWidgets.QPushButton(self)
        self.dot.setGeometry(QtCore.QRect(100, 100, 28, 28))
        self.dot.setStyleSheet("border: 3px solid blue; border-radius: 40px;")

        # self.dot.move(300, 300)

        self.tracker = EyeTracker()
        self.tracker.start_tracking()

        self.calibration = tr.ScreenBasedCalibration(self.tracker.tracker)
        self.calibration.enter_calibration_mode()

    def moveCalibrationPoint(self):
        if self.currentIndex >= len(self.points_to_calibrate):
            self.timer.stop()
            print("stop")
            print("Computing and applying calibration.")

            calibration_result = self.calibration.compute_and_apply()

            # calibration_result = self.calibration.compute_and_apply()
            print(calibration_result)
            print("Compute and apply returned {0} and collected at {1} points.".format(calibration_result.status, len(
                calibration_result.calibration_points)))

            self.calibration.leave_calibration_mode()
            self.tracker.stop_tracking()
            return

        correctPoint = self.points_to_calibrate[self.currentIndex]
        self.currentPoint.move(int(widthScreen * correctPoint[0]), int(heightScreen * correctPoint[1]))
        self.currentPoint.show()
        self.currentIndex = int(self.currentIndex) + 1


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.setFixedSize(widthScreen, heightScreen)
        self.showMaximized()
        self.startUIMenu()

    def startUIMenu(self):
        self.Menu = UIMenu(self)
        self.setWindowTitle("UIMenu")
        self.setCentralWidget(self.Menu)
        self.Menu.calibrateBtn.clicked.connect(self.startUICalibration)
        self.Menu.startBtn.clicked.connect(self.startUIDotTracker)
        self.show()

    def startUICalibration(self):
        self.Calibrate = UICalibrate(self)
        self.setWindowTitle("Calibrate")
        self.setCentralWidget(self.Calibrate)
        self.Calibrate.backBtn.clicked.connect(self.startUIMenu)

        self.show()

        self.Calibrate.timer = QTimer()
        self.Calibrate.timer.setInterval(2500)
        self.Calibrate.timer.timeout.connect(self.Calibrate.moveCalibrationPoint)

        self.Calibrate.timer.start()

    def startUIDotTracker(self):
        self.DotTracker = UIDotTracker(self)
        self.setWindowTitle("UIDottracker")
        self.setCentralWidget(self.DotTracker)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
