import numpy as np
import tobii_research as tr

class EyeTracker:
    gazeData = None,

    def __init__(self):
        self.found_eyetrackers = tr.find_all_eyetrackers()
        if len(self.found_eyetrackers) > 0:
            self.tracker = self.found_eyetrackers[0]

        self.last_gaze_left_eye = 0
        self.last_gaze_right_eye = 0

        print("init eyetracker class - found" + str(len(self.found_eyetrackers)))

    def gaze_data_callback(self, gaze_data):
        self.gazeData = gaze_data

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
        return self.gazeData

    def getAvgEyePos(self):
        # check to see if the eyetracker is connected and turned on
        if self.tracker is None:
            raise ValueError("There is no eyetracker.")

        # access gaze data dictionary to get eye position tuples, given in
        lOriginXYZ = self.gazeData['left_gaze_point_on_display_area']
        rOriginXYZ = self.gazeData['right_gaze_point_on_display_area']

        # create arrays with positions of both eyes on x, y, and z axes
        xs = (lOriginXYZ[0], rOriginXYZ[0])
        ys = (lOriginXYZ[1], rOriginXYZ[1])

        # if all of the axes have data from at least one eye
        if not (np.isnan(xs)).all() or not (np.isnan(ys)).all():
            avgEyePos = (np.nanmean(xs), np.nanmean(ys))
        else:
            avgEyePos = (0, 0, 0)

        return avgEyePos
