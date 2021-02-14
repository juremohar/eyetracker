import tobii_research as tr
import time


class EyeTracker:
    last_gaze_left_eye = 0,
    last_gaze_right_eye = 0

    def __init__(self):
        self.found_eyetrackers = tr.find_all_eyetrackers()
        if len(self.found_eyetrackers) > 0:
            self.tracker = self.found_eyetrackers[0]

        self.last_gaze_left_eye = 0
        self.last_gaze_right_eye = 0

        print("init eyetracker class - found" + str(len(self.found_eyetrackers)))

    def gaze_data_callback(gaze_data):
        # Print gaze points of left and right eye
        EyeTracker.last_gaze_left_eye = gaze_data['left_gaze_point_on_display_area']
        EyeTracker.last_gaze_right_eye = gaze_data['right_gaze_point_on_display_area']
        #
        # print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
        #     gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
        #     gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))


    def start_tracking(self):
        if not self.tracker:
            print("error starting tracking - no device found")
            return
        self.tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)

        print("starting tracking")

    def stop_tracking(self):
        if not self.tracker:
            print("error stopping tracking - no device found")
            return

        self.tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)

    def get_data(self):
        print("s")
