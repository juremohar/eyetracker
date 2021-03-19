import sys

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

class UICalibrate(QWidget):
    def __init__(self, parent=None):
        super(UICalibrate, self).__init__(parent)

        #
        # self.dot = QtWidgets.QPushButton(self)
        # self.dot.setGeometry(QtCore.QRect(100, 100, 28, 28))
        #self.dot.move(300, 300)

        # self.tracker.positionChanged.connect(self.dot.move)
        #self.tracker.positionChanged.connect(self.testEmit)

        # self.tracker.positionChanged.connect(self.move)
        self.backBtn = QPushButton("Back", self)
        self.backBtn.move(640, 480)

        self.topLeft = UICalibrationCircle(self)
        self.topLeft.move(30, 30)

        self.topRight = UICalibrationCircle(self)
        self.topRight.move(1220, 30)

        self.bottomLeft = UICalibrationCircle(self)
        self.bottomLeft.move(30, 800)

        self.bottomRight = UICalibrationCircle(self)
        self.bottomRight.move(1220, 800)

        self.dot = QtWidgets.QPushButton(self)
        self.dot.setGeometry(QtCore.QRect(100, 100, 28, 28))
        self.dot.move(300, 300)

        eyetrackers = tr.find_all_eyetrackers()
        self.tracker = EyeTracker(eyetrackers[0])
        print(self.tracker.positionChanged)
        self.tracker.positionChanged.connect(self.move)
        self.tracker.start()


    def move(self):
        print("move")
        # print(self.tracker.x)
        # print(self.tracker.y)
        # left = (self.tracker.x[0] * 1280, self.tracker.x[1] * 860)
        # right = (self.tracker.y[1] * 1280, self.tracker.y[1] * 860)

        # test tracking
        x = (self.tracker.x[0] + self.tracker.x[0])/2 * 1280
        y = (self.tracker.y[1] + self.tracker.y[1])/2 * 860

        self.dot.move(x, y)
        self.update()


class UICalibrationCircle(QWidget):
    def __init__(self, parent=None):
        super(UICalibrationCircle, self).__init__(parent)

        self.circle = QLabel(self)
        self.circle.resize(30, 30)
        self.circle.setStyleSheet("border: 3px solid blue; border-radius: 40px;")

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
        self.Calibrate.backBtn.clicked.connect(self.startUIMenu)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
