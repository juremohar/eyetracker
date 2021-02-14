from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
from EyeTracker import *
import tobii_research as tr

import time

last_gaze_left_eye = 0
last_gaze_right_eye = 0

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("EyeTracker")

        self.setMinimumSize(1280, 860)

        label = QLabel("TEST TEST")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)


def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye

    last_gaze_right_eye = gaze_data['right_gaze_point_on_display_area']
    # print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
    #     gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
    #     gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

eye = EyeTracker()

eye.tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
# eye.start_tracking()

time.sleep(2)
print(last_gaze_right_eye)
app.exec_()




