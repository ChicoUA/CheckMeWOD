from .utils import check_close
from .json_reader import *
import logging

HIP_VALUE = 8
RIGHT_KNEE_VALUE = 10
LEFT_KNEE_VALUE = 13
RIGHT_SHOULDER_VALUE = 2
LEFT_SHOULDER_VALUE = 5
LEFT_ELBOW_VALUE = 6
LEFT_WRIST_VALUE = 7
RIGHT_ELBOW_VALUE = 3
RIGHT_WRIST_VALUE = 4

logging.basicConfig(filename="air_squat.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


class press:
    def __init__(self, reps, filename):
        self.logger = logging.getLogger()
        self.reps = reps
        self.json_reader = json_reader(filename)
        self.counted_reps = 0
        self.correct_reps = 0
        self.no_reps = 0
        self.json_reader.get_number_of_files()

<<<<<<< HEAD
    #  for refactoring choose side before doing everything else
=======
>>>>>>> 9eccf70e0673dc0c55a204a220f8ee9e100369f0
    def choose_side(self):
        pass

    def check_down_position(self, wrist_position, shoulder_position):
        if check_close(wrist_position[0], shoulder_position[0]) and check_close(wrist_position[1],
                                                                                shoulder_position[1]):
            return True
        return False

    def check_up_position(self, hip_x_position, knee_x_position, shoulder_x_position, elbow_x_position,
                          wrist_x_position):
        if check_close(hip_x_position, shoulder_x_position) and check_close(knee_x_position,
                                                                            hip_x_position) and check_close(
                elbow_x_position, shoulder_x_position) and check_close(elbow_x_position, wrist_x_position):
            return True

        return False

    def get_knee_value(self, iteration, axis):
        while True:
            knee_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_KNEE_VALUE,))
            knee_position_left, trust = self.json_reader.get_values(iteration, (LEFT_KNEE_VALUE,))

            if knee_position_left == knee_position_right == 0:
                iteration -= 1
                continue

            if axis == "x" and knee_position_right != 0:
                knee_position_right = knee_position_right[0]

            elif axis == "x" and knee_position_left != 0:
                knee_position_left = knee_position_left[0]

            elif axis == "y" and knee_position_left != 0:
                knee_position_left = knee_position_left[1]

            else:
                knee_position_right = knee_position_right[1]

            return knee_position_right if knee_position_right != 0 else knee_position_left

<<<<<<< HEAD
    def get_wrist_value(self, iteration):
        while True:
            wrist_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_WRIST_VALUE,))
            wrist_position_left , trust = self.json_reader.get_values(iteration, (LEFT_WRIST_VALUE,))

            if wrist_position_left == wrist_position_right == 0:
                iteration -= 1
                continue

            return wrist_position_right if wrist_position_right != 0 else wrist_position_left

=======
>>>>>>> 9eccf70e0673dc0c55a204a220f8ee9e100369f0
    def get_shoulder_value(self, iteration):
        while True:
            shoulder_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_SHOULDER_VALUE,))
            shoulder_position_left, trust = self.json_reader.get_values(iteration, (LEFT_SHOULDER_VALUE,))

            if shoulder_position_left == shoulder_position_right == 0:
                iteration -= 1
                continue

            return shoulder_position_right if shoulder_position_right != 0 else shoulder_position_left

<<<<<<< HEAD
    def get_hip_value(self, iteration):
        while True:
            hip_position, trust = self.json_reader.get_values(iteration, (HIP_VALUE,))
            if hip_position == 0:
                iteration -= 1
                continue
            return hip_position

=======
>>>>>>> 9eccf70e0673dc0c55a204a220f8ee9e100369f0
    def check_if_still_going_down(self, wrist_y_position, iteration):
        bigger_points = 0
        # check next 5 frames
        for i in range(0, 5):
            point, trust = self.json_reader.get_values(iteration + i + 1, (RIGHT_WRIST_VALUE,))
            if point >= wrist_y_position:
                bigger_points += 1

        if bigger_points >= 4:
            return True

        return False

    def check_if_still_going_up(self, wrist_y_position, iteration):
        lower_points = 0
        # check next 5 frames
        for i in range(0, 5):
            point, trust = self.json_reader.get_values(iteration + i + 1, (RIGHT_WRIST_VALUE,))
            if point <= wrist_y_position:
                lower_points += 1

        if lower_points >= 4:
            return True

        return False

<<<<<<< HEAD
    def check_exercise(self):
        last_value_x = 0
        last_value_y = 0
        new_value_y = 0
        going_down = False  # movement starts by going up
        for i in range(0, self.json_reader.number_of_files + 1):
            value, trust = self.json_reader.get_values(i, (RIGHT_ELBOW_VALUE,))

            if self.counted_reps == self.reps:
                break

            if not trust or value == 0:
                continue

            if i == 0:
                last_value_x = value[0]
                last_value_y = value[1]
                continue

            new_value_y = value[1]

            if going_down and last_value_y < new_value_y and not check_close(new_value_y, last_value_y):
                if not self.check_if_still_going_down(new_value_y, i):
                    shoulder_x_position = self.get_shoulder_value(i)[0]
                    wrist_x_position = self.get_wrist_value(i)[0]
                    self.counted_reps += 1
                    if self.check_down_position(wrist_x_position, shoulder_x_position):
                        self.correct_reps += 1
                    else:
                        self.no_reps += 1

                    going_down = False

            elif not going_down and last_value_y > new_value_y and not check_close(last_value_y, new_value_y):
                if not self.check_if_still_going_up(new_value_y, i):
                    knee_x_position = self.get_knee_value(i, "x")
                    shoulder_x_position = self.get_shoulder_value(i)[0]
                    wrist_x_position = self.get_wrist_value(i)[0]
                    hip_x_position = self.get_hip_value(i)[0]
                    self.counted_reps += 1
                    if self.check_up_position(hip_x_position, knee_x_position, shoulder_x_position[0], last_value_x, wrist_x_position):
                        self.correct_reps += 1
                    else:
                        self.no_reps += 1
                        if self.no_reps + self.correct_reps == self.counted_reps:
                            self.no_reps -= 1

                    going_down = True

            last_value_y = value[1]
            last_value_x = value[0]

        return self.correct_reps, self.no_reps

=======
    def check_press(self):
        pass
>>>>>>> 9eccf70e0673dc0c55a204a220f8ee9e100369f0
