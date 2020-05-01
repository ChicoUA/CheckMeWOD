<<<<<<< HEAD
from .utils import check_close
from .json_reader import *
=======
from utils import check_close
from json_reader import *
>>>>>>> 9eccf70e0673dc0c55a204a220f8ee9e100369f0
import logging

HIP_VALUE = 8
RIGHT_KNEE_VALUE = 10
LEFT_KNEE_VALUE = 13
RIGHT_SHOULDER_VALUE = 2
LEFT_SHOULDER_VALUE = 5

logging.basicConfig(filename="air_squat.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


class air_squat:
    def __init__(self, reps, filename):
        self.logger = logging.getLogger()
        self.reps = reps
        self.json_reader = json_reader(filename)
        self.counted_reps = 0
        self.correct_reps = 0
        self.no_reps = 0
        self.json_reader.get_number_of_files()

    def check_down_position(self, hip_y_position, knee_y_position):
        if hip_y_position < knee_y_position:
            self.logger.debug("Good down position: " + str(hip_y_position) + " - " + str(knee_y_position))
            return True
        else:
            self.logger.debug("Bad down position: " + str(hip_y_position) + " - " + str(knee_y_position))
            return False

    def check_up_position(self, shoulder_x_position, hip_x_position, knee_x_position):
        if check_close(shoulder_x_position, hip_x_position) and check_close(hip_x_position, knee_x_position):
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
            if point[1] >= hip_y_position:
                bigger_points += 1

        if bigger_points >= 4:
            return True

        return False

    def check_if_still_going_up(self, hip_y_position, iteration):
        lower_points = 0
        # check next 5 frames
        for i in range(0, 5):
            point, trust = self.json_reader.get_values(iteration + i + 1, (HIP_VALUE,))
            if point[1] <= hip_y_position:
                lower_points += 1

        if lower_points >= 4:
            return True

        return False

    def get_knee_value(self, iteration):
        while True:
            knee_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_KNEE_VALUE,))
            knee_position_left, trust = self.json_reader.get_values(iteration, (LEFT_KNEE_VALUE,))

            if knee_position_left == knee_position_right == 0:
                iteration -= 1
                continue

            return knee_position_right if knee_position_right != 0 else knee_position_left

    def get_shoulder_value(self, iteration):
        while True:
            shoulder_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_SHOULDER_VALUE,))
            shoulder_position_left, trust = self.json_reader.get_values(iteration, (LEFT_SHOULDER_VALUE,))

            if shoulder_position_left == shoulder_position_right == 0:
                iteration -= 1
                continue

            return shoulder_position_right if shoulder_position_right != 0 else shoulder_position_left

<<<<<<< HEAD
    def check_exercise(self):
=======
    def check_squat(self):
>>>>>>> 9eccf70e0673dc0c55a204a220f8ee9e100369f0
        last_value_x = 0
        last_value_y = 0
        new_value_y = 0
        going_down = True  # movement starts by going down
        for i in range(0, self.json_reader.number_of_files + 1):
            value, trust = self.json_reader.get_values(i, (HIP_VALUE,))

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
<<<<<<< HEAD
                    knee_y_position = self.get_knee_value(i)[1]
                    self.counted_reps += 1
                    if self.check_down_position(last_value_y, knee_y_position):
=======
                    knee_y_position = self.get_knee_value(i)
                    self.counted_reps += 1
                    if self.check_down_position(last_value_y, knee_y_position[1]):
>>>>>>> 9eccf70e0673dc0c55a204a220f8ee9e100369f0
                        self.correct_reps += 1
                    else:
                        self.no_reps += 1

                    going_down = False

            elif not going_down and last_value_y > new_value_y and not check_close(last_value_y, new_value_y):
                if not self.check_if_still_going_up(new_value_y, i):
<<<<<<< HEAD
                    knee_x_position = self.get_knee_value(i)[0]
                    shoulder_x_position = self.get_shoulder_value(i)[0]
                    self.counted_reps += 1
                    if self.check_up_position(shoulder_x_position, last_value_x, knee_x_position):
=======
                    knee_x_position = self.get_knee_value(i)
                    shoulder_x_position = self.get_shoulder_value(i)
                    self.counted_reps += 1
                    if self.check_up_position(shoulder_x_position[0], last_value_x, knee_x_position[0]):
>>>>>>> 9eccf70e0673dc0c55a204a220f8ee9e100369f0
                        self.correct_reps += 1
                    else:
                        self.no_reps += 1
                        if self.no_reps + self.correct_reps == self.counted_reps:
                            self.no_reps -= 1

                    going_down = True

            last_value_y = value[1]
            last_value_x = value[0]

        return self.correct_reps, self.no_reps


def main():
    squat = air_squat(3, "output_json/")
<<<<<<< HEAD
    reps, no_reps = squat.check_exercise()
=======
    reps, no_reps = squat.check_squat()
>>>>>>> 9eccf70e0673dc0c55a204a220f8ee9e100369f0
    print(reps, no_reps)


if __name__ == "__main__":
    main()
