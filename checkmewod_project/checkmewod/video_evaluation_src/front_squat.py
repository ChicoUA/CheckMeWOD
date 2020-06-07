from checkmewod.video_evaluation_src.utils import check_close, check_close2, check_close4
from checkmewod.video_evaluation_src.json_reader import *
import logging

HIP_VALUE = 8
RIGHT_KNEE_VALUE = 10
LEFT_KNEE_VALUE = 13
RIGHT_SHOULDER_VALUE = 2
LEFT_SHOULDER_VALUE = 5
RIGHT_ELBOW_VALUE = 3
LEFT_ELBOW_VALUE = 6
LEFT_WRIST_VALUE = 7
RIGHT_WRIST_VALUE = 4

logging.basicConfig(filename="air_squat.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


class front_squat:
    def __init__(self, reps, filename):
        self.logger = logging.getLogger()
        self.reps = reps
        self.json_reader = json_reader(filename)
        self.counted_reps = 0
        self.correct_reps = 0
        self.no_reps = 0
        self.json_reader.get_number_of_files()

    def check_down_position(self, hip_y_position, knee_y_position, shoulder_y_position, wrist_y_position):
        if hip_y_position > knee_y_position and check_close2(shoulder_y_position, wrist_y_position):
            self.logger.debug("Good down position: " + str(hip_y_position) + " - " + str(knee_y_position))
            return True
        else:
            self.logger.debug("Bad down position: " + str(hip_y_position) + " - " + str(knee_y_position))
            return False

    def check_up_position(self, shoulder_x_position, hip_x_position, knee_x_position, shoulder_y_position, wrist_y_position):
        if check_close(shoulder_x_position, hip_x_position) and check_close(hip_x_position, knee_x_position) \
                and check_close4(shoulder_y_position, wrist_y_position):
            self.logger.debug("Good up position: " + str(hip_x_position) + " - " + str(knee_x_position) + " - " + str(
                shoulder_x_position))
            return True
        else:
            self.logger.debug("Good up position: " + str(hip_x_position) + " - " + str(knee_x_position) + " - " + str(
                shoulder_x_position))
            return False

    def check_if_still_going_down(self, hip_y_position, iteration):
        bigger_points = 0
        # check next 5 frames
        for i in range(0, 5):
            point, trust = self.json_reader.get_values(iteration + i + 1, (HIP_VALUE,))
            if point[1] <= hip_y_position:
                bigger_points += 1

            hip_y_position = point[1]

        if bigger_points >= 3:
            return True

        return False

    def check_if_still_going_up(self, hip_y_position, iteration):
        lower_points = 0
        # check next 5 frames
        for i in range(0, 5):
            point, trust = self.json_reader.get_values(iteration + i + 1, (HIP_VALUE,))
            if point[1] >= hip_y_position:
                lower_points += 1

            hip_y_position = point[1]

        if lower_points >= 3:
            return True

        return False

    def get_knee_value(self, iteration):
        while True:
            knee_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_KNEE_VALUE,))
            knee_position_left, trust = self.json_reader.get_values(iteration, (LEFT_KNEE_VALUE,))

            if knee_position_left == knee_position_right == 0:
                iteration += 1
                continue

            return knee_position_right if knee_position_right != 0 else knee_position_left

    def get_shoulder_value(self, iteration):
        while True:
            shoulder_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_SHOULDER_VALUE,))
            shoulder_position_left, trust = self.json_reader.get_values(iteration, (LEFT_SHOULDER_VALUE,))

            if shoulder_position_left == shoulder_position_right == 0:
                iteration += 1
                continue

            return shoulder_position_right if shoulder_position_right != 0 else shoulder_position_left

    def get_wrist_value(self, iteration):
        while True:
            wrist_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_WRIST_VALUE,))
            wrist_position_left, trust = self.json_reader.get_values(iteration, (LEFT_WRIST_VALUE,))

            if wrist_position_left[1] == 0 and wrist_position_right[1] == 0:
                iteration += 1
                continue

            return wrist_position_right if wrist_position_right[0] != 0 else wrist_position_left

    def get_elbow_value(self, iteration):
        while True:
            elbow_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_ELBOW_VALUE,))
            elbow_position_left, trust = self.json_reader.get_values(iteration, (LEFT_ELBOW_VALUE,))

            if elbow_position_left == elbow_position_right == 0:
                iteration += 1
                continue

            return elbow_position_right if elbow_position_right != 0 else elbow_position_left

    def check_exercise(self):
        list_of_frames = {}
        was_no_rep = False
        last_value_x = 0
        last_value_y = 0
        new_value_y = 0
        first_rep_detected = False
        first_rep_y_value = 0
        going_down = False  # movement starts by going down
        for i in range(0, self.json_reader.number_of_files + 1):
            value, trust = self.json_reader.get_values(i, (HIP_VALUE,))

            if self.counted_reps == self.reps:
                break

            if not trust or value == 0:
                continue

            if i == 0:
                last_value_x = value[0]
                last_value_y = value[1]
                first_rep_y_value = value[1]
                first_rep_detected = True
                continue

            new_value_y = value[1]

            if not going_down and last_value_y < new_value_y:
                if first_rep_detected is True and new_value_y < first_rep_y_value + 20:
                    pass

                elif not self.check_if_still_going_up(new_value_y, i):
                    knee_y_position = self.get_knee_value(i)[1]
                    wrist_y_position = self.get_wrist_value(i)[1]
                    shoulder_y_position = self.get_shoulder_value(i)[1]
                    if not self.check_down_position(new_value_y, knee_y_position, shoulder_y_position, wrist_y_position):
                        print("fez mal baixo ", i)
                        # self.correct_reps += 1
                        was_no_rep = True
                    else:
                        print("fez bem baixo ", i, last_value_y, new_value_y)
                        was_no_rep = False

                    going_down = True

            elif going_down and last_value_y > new_value_y:
                if first_rep_detected is True and new_value_y > first_rep_y_value + 20:
                    pass

                elif not self.check_if_still_going_down(new_value_y, i):
                    knee_x_position = self.get_knee_value(i)[0]
                    shoulder_position = self.get_shoulder_value(i)
                    wrist_y_position = self.get_wrist_value(i)[1]
                    self.counted_reps += 1

                    if first_rep_detected is False:
                        first_rep_detected = True
                        first_rep_y_value = last_value_y

                    if self.check_up_position(shoulder_position[0], last_value_x, knee_x_position, shoulder_position[1], wrist_y_position) and not was_no_rep:
                        print("fez bem cima ", i, first_rep_y_value)
                        self.correct_reps += 1
                        list_of_frames[i] = "rep"
                    else:
                        print("fez mal cima ", i)
                        self.no_reps += 1
                        list_of_frames[i] = "no rep"

                    going_down = False

            last_value_y = value[1]
            last_value_x = value[0]

        return self.correct_reps, self.no_reps, list_of_frames