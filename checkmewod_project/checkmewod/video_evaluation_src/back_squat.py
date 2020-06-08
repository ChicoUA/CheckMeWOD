from checkmewod.video_evaluation_src.utils import check_close, check_close2, check_close3, check_close4, check_close6
from checkmewod.video_evaluation_src.json_reader import *
import logging

HIP_VALUE = 8
LEFT_ELBOW_VALUE = 6
RIGHT_ELBOW_VALUE = 3
LEFT_WRIST_VALUE = 7
RIGHT_WRIST_VALUE = 4
RIGHT_KNEE_VALUE = 10
LEFT_KNEE_VALUE = 13
RIGHT_SHOULDER_VALUE = 2
LEFT_SHOULDER_VALUE = 5


logging.basicConfig(filename="back_squat.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


class back_squat:
    def __init__(self, reps, filename):
        self.logger = logging.getLogger()
        self.reps = reps
        self.json_reader = json_reader(filename)
        self.counted_reps = 0
        self.correct_reps = 0
        self.no_reps = 0
        self.json_reader.get_number_of_files()

    def check_down_position(self, hip_y_position, knee_y_position, elbow_position, wrist_position, shoulder_position):
        if hip_y_position > knee_y_position or check_close3(hip_y_position, knee_y_position):
            
            if elbow_position[1] > shoulder_position[1] and (elbow_position[0] < shoulder_position[0] or check_close3(elbow_position[0], shoulder_position[0])):
                
                if check_close4(wrist_position[0], shoulder_position[0]) and check_close4(wrist_position[1], shoulder_position[1]):
                    
                    self.logger.debug("Good down position: " + str(hip_y_position) + " - " + str(knee_y_position))
                    return True
        else:
            self.logger.debug("Bad down position: " + str(hip_y_position) + " - " + str(knee_y_position))
            return False

    def check_up_position(self, shoulder_position, hip_x_position, knee_x_position, elbow_position, wrist_position):
        if check_close6(shoulder_position[0], hip_x_position) and check_close6(hip_x_position, knee_x_position):
            if elbow_position[1] > shoulder_position[1] and (elbow_position[0] < shoulder_position[0] or check_close3(elbow_position[0], shoulder_position[0])):
                
                if check_close4(wrist_position[0], shoulder_position[0]) and check_close4(wrist_position[1], shoulder_position[1]):
                    self.logger.debug("Good up position: " + str(hip_x_position) + " - " + str(knee_x_position) + " - " + str(
                        shoulder_position[0]))
                    return True
        else:
            self.logger.debug("Good up position: " + str(hip_x_position) + " - " + str(knee_x_position) + " - " + str(
                shoulder_position[0]))
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
            if knee_position_left[0] == knee_position_right[0] == 0:
                iteration -= 1

            elif knee_position_left[0] != 0 or knee_position_right[0] != 0:
                break

        return knee_position_right if knee_position_right != 0 else knee_position_left

    def get_shoulder_value(self, iteration):
        while True:
            shoulder_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_SHOULDER_VALUE,))
            shoulder_position_left, trust = self.json_reader.get_values(iteration, (LEFT_SHOULDER_VALUE,))

            if shoulder_position_left[0] == shoulder_position_right[0] == 0:
                iteration -= 1
                continue

            return shoulder_position_right if shoulder_position_right != 0 else shoulder_position_left

    # TODO
    def get_elbow_value(self, iteration):
        while True:
            elbow_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_ELBOW_VALUE,))
            elbow_position_left, trust = self.json_reader.get_values(iteration, (LEFT_ELBOW_VALUE,))
            
            if elbow_position_left[0] == elbow_position_right[0] == 0:
                iteration -= 1
                continue

            return elbow_position_right if elbow_position_right != 0 else elbow_position_left

    # TODO
    def get_wrist_value(self, iteration):
        while True:
            wrist_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_WRIST_VALUE,))
            wrist_position_left, trust = self.json_reader.get_values(iteration, (LEFT_WRIST_VALUE,))

            if wrist_position_left[0] == wrist_position_right[0] == 0:
                iteration -= 1
                continue

            return wrist_position_right if wrist_position_right != 0 else wrist_position_left

    def check_exercise(self):
        list_of_frames = {}
        was_no_rep = False
        last_value_x = 0
        last_value_y = 0
        new_value_y = 0
        first_rep_detected = False
        first_rep_y_value = 0
        going_down = False  # movement starts by going down
        for i in range(0, self.json_reader.number_of_files):
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

            if not going_down and last_value_y < new_value_y:
                if first_rep_detected is True and new_value_y < first_rep_y_value + 50:
                    pass

                elif not self.check_if_still_going_up(new_value_y, i):
                    knee_y_position = self.get_knee_value(i)[1]
                    wrist_position = self.get_wrist_value(i)
                    elbow_position = self.get_elbow_value(i)
                    shoulder_position = self.get_shoulder_value(i)
                    if not self.check_down_position(last_value_y, knee_y_position, elbow_position, wrist_position, shoulder_position):
                        print("fez mal baixo ", i)
                        # self.correct_reps += 1
                        was_no_rep = True
                    else:
                        print("fez bem baixo ", i, last_value_y, new_value_y)
                        was_no_rep = False

                    going_down = True

            elif going_down and last_value_y > new_value_y:
                if not self.check_if_still_going_down(new_value_y, i):
                    knee_x_position = self.get_knee_value(i)[0]
                    shoulder_position = self.get_shoulder_value(i)
                    wrist_position = self.get_wrist_value(i)
                    elbow_position = self.get_elbow_value(i)
                    self.counted_reps += 1
                    #print(last_value_x, shoulder_position[0], knee_x_position)
                    if first_rep_detected is False:
                        first_rep_detected = True
                        first_rep_y_value = last_value_y
                    if self.check_up_position(shoulder_position, last_value_x, knee_x_position, elbow_position, wrist_position) and not was_no_rep:
                        print("fez bem cima ", i, first_rep_y_value)
                        self.correct_reps += 1
                        list_of_frames[i] = "rep"
                    else:
                        print("fez mal cima ", i)
                        self.no_reps += 1
                        list_of_frames[i] = "no rep"
                        #if self.no_reps + self.correct_reps == self.counted_reps:
                            #self.no_reps -= 1

                    going_down = False

            last_value_y = value[1]
            last_value_x = value[0]

        return self.correct_reps, self.no_reps, list_of_frames


def main():
    squat = back_squat(3, "output_json/")
    reps, no_reps, list_of_frames = squat.check_exercise()
    print(reps, no_reps, list_of_frames)


if __name__ == "__main__":
    main()

