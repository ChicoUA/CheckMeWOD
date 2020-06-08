from checkmewod.video_evaluation_src.utils import check_close, check_close2, check_close3, check_close4, check_close5
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
LEFT_HEEL_VALUE = 21
RIGHT_HEEL_VALUE = 24

logging.basicConfig(filename="deadlift.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


class deadlift:
    def __init__(self, reps, filename):
        self.logger = logging.getLogger()
        self.reps = reps
        self.json_reader = json_reader(filename)
        self.counted_reps = 0
        self.correct_reps = 0
        self.no_reps = 0
        self.json_reader.get_number_of_files()
        self.body_orientation = None

    def check_body_orientation(self, hip_x_position, shoulder_x_position):
        if hip_x_position > shoulder_x_position:
            #face facing left side
            self.body_orientation = "LEFT"
        else:
            #face facing right side
            self.body_orientation = "RIGHT"

    def check_down_position(self, hip_position, knee_position, shoulder_position, elbow_position, wrist_position, heel_position):   
        if elbow_position[1] > shoulder_position[1]:
            if heel_position[1] > knee_position[1] > hip_position[1]:
                if self.body_orientation == "LEFT":
                    if knee_position[0] < heel_position[0] < hip_position[0]:
                        self.logger.debug("Good down position: " + str(hip_position[1]) + " - " + str(knee_position[1]))
                        return True
                elif self.body_orientation == "RIGHT":
                    if knee_position[0] < heel_position[0] < hip_position[0]:
                        self.logger.debug("Good down position: " + str(hip_position[1]) + " - " + str(knee_position[1]))
                        return True
        else:
            self.logger.debug("Bad down position: " + str(hip_position[1]) + " - " + str(knee_position[1]))
            return False

    def check_up_position(self, shoulder_x_position, hip_x_position, knee_x_position):
        if check_close4(shoulder_x_position, hip_x_position) and check_close4(hip_x_position, knee_x_position):
            self.logger.debug("Good up position: " + str(hip_x_position) + " - " + str(knee_x_position) + " - " + str(
                shoulder_x_position))
            return True
        else:
            self.logger.debug("Good up position: " + str(hip_x_position) + " - " + str(knee_x_position) + " - " + str(
                shoulder_x_position))
            return False

    def check_if_still_going_down(self, shoulder_y_position, iteration):
        bigger_points = 0
        # check next 5 frames
        for i in range(0, 5):
            point = self.get_shoulder_value(iteration + i +1)
            if point[1] <= shoulder_y_position or check_close5(point[1], shoulder_y_position):
                bigger_points += 1

            shoulder_y_position = point[1]

        if bigger_points >= 3:
            return True

        return False

    def check_if_still_going_up(self, shoulder_y_position, iteration):
        lower_points = 0
        # check next 5 frames
        for i in range(0, 5):
            point = self.get_shoulder_value(iteration + i +1)
            if point[1] >= shoulder_y_position or check_close5(point[1], shoulder_y_position):
                lower_points += 1

            shoulder_y_position = point[1]

        if lower_points >= 3:
            return True

        return False

    def get_hip_value(self, iteration):
        while True:
            hip_position, trust = self.json_reader.get_values(iteration, (HIP_VALUE,))
            if hip_position[0] == 0:
                iteration -= 1

            elif hip_position[0] != 0:
                break

        return hip_position

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
    
    def get_elbow_value(self, iteration):
        while True:
            elbow_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_ELBOW_VALUE,))
            elbow_position_left, trust = self.json_reader.get_values(iteration, (LEFT_ELBOW_VALUE,))
            
            if elbow_position_left[0] == elbow_position_right[0] == 0:
                iteration -= 1
                continue

            return elbow_position_right if elbow_position_right != 0 else elbow_position_left

    def get_wrist_value(self, iteration):
        while True:
            wrist_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_WRIST_VALUE,))
            wrist_position_left, trust = self.json_reader.get_values(iteration, (LEFT_WRIST_VALUE,))
            if wrist_position_left[0] == wrist_position_right[0] == 0:
                iteration -= 1
                continue

            return wrist_position_right if wrist_position_right != 0 else wrist_position_left
    
    def get_heel_value(self, iteration):
        while True:
            heel_position_right, trust = self.json_reader.get_values(iteration, (RIGHT_HEEL_VALUE,))
            heel_position_left, trust = self.json_reader.get_values(iteration, (LEFT_HEEL_VALUE,))

            if heel_position_left[0] == heel_position_right[0] == 0:
                iteration -= 1
                continue

            return heel_position_right if heel_position_right != 0 else heel_position_left

    def check_exercise(self):
        list_of_frames = {}
        was_no_rep = False
        last_value_x = 0
        last_value_y = 0
        new_value_y = 0
        new_value_x = 0
        first_rep_detected = False
        first_rep_y_value = 0
        going_down = False  # movement starts by going down
        for i in range(0, self.json_reader.number_of_files):
            value = self.get_shoulder_value(i)

            if self.counted_reps == self.reps:
                break

            if i == 0:
                last_value_x = value[0]
                last_value_y = value[1]
                continue

            new_value_y = value[1]
            new_value_x = value[0]
            
            if not going_down and last_value_y > new_value_y:
                
                if first_rep_detected is True and new_value_y < first_rep_y_value + 50:
                    pass

                elif not self.check_if_still_going_up(new_value_y, i):
                    knee_position = self.get_knee_value(i)
                    hip_position = self.get_hip_value(i)
                    elbow_position = self.get_elbow_value(i)
                    wrist_position = self.get_wrist_value(i)
                    heel_position = self.get_heel_value(i)
                    self.check_body_orientation(hip_position[0], new_value_x)
                    if not self.check_down_position(hip_position, knee_position, [new_value_x, new_value_y], elbow_position, wrist_position, heel_position ):
                        print("fez mal baixo ", i)
                        # self.correct_reps += 1
                        was_no_rep = True
                    else:
                        print("fez bem baixo ", i, last_value_y, new_value_y)
                        was_no_rep = False

                    going_down = True

            elif going_down and last_value_y < new_value_y:
                if not self.check_if_still_going_down(new_value_y, i):
                    knee_x_position = self.get_knee_value(i)[0]
                    hip_x_position = self.get_hip_value(i)[0]
                    self.counted_reps += 1
                    #print(last_value_x, shoulder_x_position, knee_x_position)
                    if first_rep_detected is False:
                        first_rep_detected = True
                        first_rep_y_value = last_value_y
                    if self.check_up_position(hip_x_position, new_value_x, knee_x_position) and not was_no_rep:
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
    dead = deadlift(2, "output_json/")
    reps, no_reps, list_of_frames = dead.check_exercise()
    print(reps, no_reps, list_of_frames)


if __name__ == "__main__":
    main()

