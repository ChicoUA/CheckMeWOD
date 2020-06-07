from checkmewod.video_evaluation_src.utils import check_close, check_close2
from checkmewod.video_evaluation_src.json_reader import *
import logging

LEFT_WRIST_VALUE = 7
RIGHT_WRIST_VALUE = 4
NOSE_VALUE = 0
LEFT_ELBOW_VALUE = 6
LEFT_SHOULDER_VALUE = 5
RIGHT_SHOULDER_VALUE = 2
RIGHT_ELBOW_VALUE = 3


logging.basicConfig(filename="air_squat.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


class muscle_up:
    def __init__(self, reps, filename):
        self.logger = logging.getLogger()
        self.reps = reps
        self.json_reader = json_reader(filename)
        self.counted_reps = 0
        self.correct_reps = 0
        self.no_reps = 0
        self.json_reader.get_number_of_files()

    def check_up_position(self, nose_position, wrist_y_position, wrist_x_position, elbow_x_position, shoulder_x_position):
        if nose_position < wrist_y_position + 10 and check_close(wrist_x_position, elbow_x_position) and check_close(elbow_x_position, shoulder_x_position):
            return True

        return False

    def check_down_position(self, wrist_position, elbow_position, shoulder_position):
        if check_close2(wrist_position, elbow_position) and check_close2(elbow_position, shoulder_position):
            return True

        return False

    def get_shoulder_value(self, iteration):
        while True:
            shoulder_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_SHOULDER_VALUE,))
            shoulder_position_left, trust = self.json_reader.get_values(iteration, (LEFT_SHOULDER_VALUE,))

            if shoulder_position_left == shoulder_position_right == 0:
                iteration -= 1
                continue

            return shoulder_position_right if shoulder_position_right != 0 else shoulder_position_left

    def get_wrist_value(self, iteration):
        while True:
            wrist_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_WRIST_VALUE,))
            wrist_position_left, trust = self.json_reader.get_values(iteration, (LEFT_WRIST_VALUE,))

            if wrist_position_left == wrist_position_right == 0:
                iteration -= 1
                continue

            return wrist_position_right if wrist_position_right != 0 else wrist_position_left

    def get_elbow_value(self, iteration):
        while True:
            elbow_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_ELBOW_VALUE,))
            elbow_position_left, trust = self.json_reader.get_values(iteration, (LEFT_ELBOW_VALUE,))

            if elbow_position_left == elbow_position_right == 0:
                iteration -= 1
                continue

            return elbow_position_right if elbow_position_right != 0 else elbow_position_left

    def check_if_still_going_down(self, nose_y_position, iteration):
        bigger_points = 0
        # check next 5 frames
        for i in range(0, 5):
            if iteration + i >= self.json_reader.number_of_files - 1:
                break
            point, trust = self.json_reader.get_values(iteration + i + 1, (NOSE_VALUE,))
            if point[1] >= nose_y_position:
                bigger_points += 1

            nose_y_position = point[1]

        if bigger_points >= 2:
            return True

        return False

    def check_if_still_going_up(self, nose_y_position, iteration):
        lower_points = 0
        # check next 5 frames
        for i in range(0, 5):
            if iteration + i > self.json_reader.number_of_files - 1:
                break
            point, trust = self.json_reader.get_values(iteration + i + 1, (NOSE_VALUE,))
            if point[1] <= nose_y_position:
                lower_points += 1

            nose_y_position = point[1]

        if lower_points >= 2:
            return True

        return False

    def check_exercise(self):
        list_of_frames = {}
        was_no_rep = False
        last_value_x = 0
        last_value_y = 0
        new_value_y = 0
        first_rep_detected = False
        first_rep_y_value = 0
        going_down = False  # movement starts by going up
        for i in range(0, self.json_reader.number_of_files + 1):
            value, trust = self.json_reader.get_values(i, (NOSE_VALUE,))

            if self.counted_reps == self.reps:
                break

            if i == self.json_reader.number_of_files + 1:
                list_of_frames[i] = "no_rep"
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

            if going_down and last_value_y < new_value_y:
                if first_rep_detected is True and new_value_y < first_rep_y_value - 100:
                    pass

                elif not self.check_if_still_going_down(new_value_y, i):
                    shoulder_x_position = self.get_shoulder_value(i)[0]
                    wrist_x_position = self.get_wrist_value(i)[0]
                    elbow_x_position = self.get_elbow_value(i)[0]
                    self.counted_reps += 1

                    if first_rep_detected is False:
                        first_rep_detected = True
                        first_rep_y_value = last_value_y

                    if not self.check_down_position(wrist_x_position, elbow_x_position, shoulder_x_position) or was_no_rep:
                        print("fez mal baixo", i)
                        self.correct_reps += 1
                        list_of_frames[i] = "no rep"
                    else:
                        print("fez bem baixo ", i, last_value_y, new_value_y)
                        self.no_reps += 1
                        list_of_frames[i] = "rep"

                    going_down = False

            elif not going_down and last_value_y > new_value_y:
                if first_rep_detected is True and new_value_y > first_rep_y_value - 20:
                    pass

                elif not self.check_if_still_going_up(new_value_y, i):
                    wrist_position = self.get_wrist_value(i)
                    shoulder_x_position = self.get_shoulder_value(i)[0]
                    elbow_x_position = self.get_elbow_value(i)[0]
                    if not self.check_up_position(new_value_y, wrist_position[1], wrist_position[0], elbow_x_position, shoulder_x_position):
                        print("fez mal cima ", i)
                        was_no_rep = True
                    else:
                        print("fez bem cima ", i)
                        was_no_rep = False

                    going_down = True

            last_value_y = value[1]
            last_value_x = value[0]

        return self.correct_reps, self.no_reps, list_of_frames

