from .utils import check_close
from .json_reader import *
import logging

HIP_VALUE = 8
LEFT_WRIST_VALUE = 7
RIGHT_WRIST_VALUE = 4
NECK_VALUE = 1
RIGHT_SHOULDER_VALUE = 2
LEFT_SHOULDER_VALUE = 5
RIGHT_ELBOW_VALUE = 3
LEFT_ELBOW_VALUE = 6

logging.basicConfig(filename="air_squat.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


class push_up:
    def __init__(self, reps, filename):
        self.logger = logging.getLogger()
        self.reps = reps
        self.json_reader = json_reader(filename)
        self.counted_reps = 0
        self.correct_reps = 0
        self.no_reps = 0
        self.json_reader.get_number_of_files()

    def check_down_position(self, hip_y_position, neck_y_position, wrist_y_position):
        if check_close(hip_y_position, neck_y_position) and check_close(neck_y_position - 20, wrist_y_position):
            self.logger.debug("Good down position")
            return True
        else:
            self.logger.debug("Bad down position" )
            return False

    def check_up_position(self, shoulder_x_position, elbow_x_position, wrist_x_position):
        if check_close(shoulder_x_position, elbow_x_position) and check_close(elbow_x_position, wrist_x_position):
            self.logger.debug("Good up position")
            return True
        else:
            self.logger.debug("Good up position")
            return False
