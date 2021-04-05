import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import tobii_research as tr

class EyeTracker(QtCore.QObject):
    positionChanged = QtCore.pyqtSignal(float, float)
    test = pyqtSignal(object)
    x = 0
    y = 0

    def __init__(self, tracker, parent=None):
        super(EyeTracker, self).__init__(parent)
        self._tracker = tracker

        self.test.connect(self.izpis)

    @property
    def tracker(self):
        return self._tracker

    def start(self):
        self.tracker.subscribe_to(
            tr.EYETRACKER_GAZE_DATA, self._callback, as_dictionary=True
        )

    def _callback(self, gaze_data_):
        #print(gaze_data_)
        self.x = gaze_data_['left_gaze_point_on_display_area']
        self.y = gaze_data_['right_gaze_point_on_display_area']
        self.positionChanged.emit(
            gaze_data_['left_gaze_point_on_display_area'],
            gaze_data_['right_gaze_point_on_display_area']
        )


class UIMenu(QWidget):
    def __init__(self, parent=None):
        super(UIMenu, self).__init__(parent)
        self.startBtn = QPushButton('Start', self)
        self.startBtn.move(640, 480)

        self.calibrateBtn = QPushButton('Start calibrate', self)
        self.calibrateBtn.move(640, 580)


class UICalibrationCircle(QWidget):
    def __init__(self, parent=None):
        super(UICalibrationCircle, self).__init__(parent)

        self.circle = QLabel(self)
        self.circle.resize(30, 30)
        self.circle.setStyleSheet("border: 3px solid blue; border-radius: 40px;")


class UICalibrate(QWidget):
    currentIndex = 0
    points_to_calibrate = [(0.5, 0.5), (0.1, 0.1), (0.1, 0.9), (0.9, 0.1), (0.9, 0.9)]
    currentPoint = None
    def __init__(self, parent=None):
        super(UICalibrate, self).__init__(parent)

        self.currentPoint = UICalibrationCircle(self)
        self.currentPoint.hide()

        self.dot = QtWidgets.QPushButton(self)
        self.dot.setGeometry(QtCore.QRect(100, 100, 28, 28))
        self.dot.move(300, 300)

        # eyetrackers = tr.find_all_eyetrackers()
        # self.tracker = EyeTracker(eyetrackers[0])
        # print(self.tracker.positionChanged)
        # self.tracker.positionChanged.connect(self.move)
        # self.tracker.start()


    def moveCalibrationPoint(self):
        if self.currentIndex >= len(self.points_to_calibrate):
            self.timer.stop()
            print("stop")
            return

        correctPoint = self.points_to_calibrate[self.currentIndex]
        self.currentPoint.move(int(1280*correctPoint[0]), int(860*correctPoint[1]))
        self.currentPoint.show()
        self.currentIndex = int(self.currentIndex) + 1


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedSize(1280, 860)
        self.startUIMenu()

    def startUIMenu(self):
        self.Menu = UIMenu(self)
        self.setWindowTitle("UIMenu")
        self.setCentralWidget(self.Menu)
        self.Menu.calibrateBtn.clicked.connect(self.startUICalibration)
        self.show()

    def startUICalibration(self):
        self.Calibrate = UICalibrate(self)
        self.setWindowTitle("Calibrate")
        self.setCentralWidget(self.Calibrate)
        # self.Calibrate.backBtn.clicked.connect(self.startUIMenu)

        self.show()

        self.Calibrate.timer = QTimer()
        self.Calibrate.timer.setInterval(1000)
        self.Calibrate.timer.timeout.connect(self.Calibrate.moveCalibrationPoint)

        self.Calibrate.timer.start()

        # self.Calibrate.startCalibration()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
