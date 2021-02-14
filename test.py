import os
import time

from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtMultimediaWidgets
import tobii_research as tr


class EyeTracker(QtCore.QObject):
    positionChanged = QtCore.pyqtSignal(float, float)
    x = 0
    y = 0

    def __init__(self, tracker, parent=None):
        super(EyeTracker, self).__init__(parent)
        self._tracker = tracker

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


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        # first window,just have a single button for play the video
        self.resize(1280, 860)
        self.btn_show_dot = QtWidgets.QPushButton(self)
        self.btn_show_dot.setGeometry(QtCore.QRect(200, 100, 28, 28))
        self.btn_show_dot.setObjectName("show_tracking")
        self.btn_show_dot.setText("Try")
        self.btn_show_dot.clicked.connect(self.move)

        self.dot = QtWidgets.QPushButton(self)
        self.dot.setGeometry(QtCore.QRect(100, 100, 28, 28))
        self.dot.move(300, 300)

        eyetrackers = tr.find_all_eyetrackers()
        self.tracker = EyeTracker(eyetrackers[0])
        self.tracker.positionChanged.connect(self.dot.move)
        self.tracker.start()


    def move(self):

        # print(self.tracker.x)
        # print(self.tracker.y)
        # left = (self.tracker.x[0] * 1280, self.tracker.x[1] * 860)
        # right = (self.tracker.y[1] * 1280, self.tracker.y[1] * 860)

        # test tracking
        x = (self.tracker.x[0] + self.tracker.x[0])/2 * 1280
        y = (self.tracker.y[1] + self.tracker.y[1])/2 * 860

        self.dot.move(x, y)
        self.update()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
