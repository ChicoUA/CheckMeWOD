from __future__ import absolute_import, unicode_literals

from celery import shared_task
from checkmewod.models import VideoSubmission
from checkmewod.video_evaluation_src.body_detection_openpose import body_detect
from checkmewod.video_evaluation_src.air_squat import air_squat
from checkmewod.video_evaluation_src.front_squat import front_squat
from checkmewod.video_evaluation_src.press import press
from checkmewod.video_evaluation_src.pull_up import pull_up
from checkmewod.video_evaluation_src.push_up import push_up
import os, shutil

@shared_task
def evaluate_video(id):
    info = VideoSubmission.objects.get(video_id=id)
    body_detect(str(info.video_file))
    json_folder = "/home/daniel/uni/CheckMeWOD/checkmewod_project/checkmewod/video_evaluation_src/output_json/"
    reps = None
    no_reps = None
    if str(info.exercise_in_video) == "Air Squat":
        air_squat_exerc = air_squat(int(info.number_reps), json_folder)
        reps, no_reps = air_squat_exerc.check_exercise()
        print("reps: " + str(reps))
        print("no_reps: " + str(no_reps))

    elif str(info.exercise_in_video) == "Press":
        press_exerc = press(int(info.number_reps), json_folder)
        reps, no_reps = press_exerc.check_exercise()
        print("reps: " + str(reps))
        print("no_reps: " + str(no_reps))

    elif str(info.exercise_in_video) == "Pull Up":
        pull_up_exerc = pull_up(int(info.number_reps), json_folder)
        reps, no_reps = pull_up_exerc.check_exercise()
        print("reps: " + str(reps))
        print("no_reps: " + str(no_reps))

    elif str(info.exercise_in_video) == "Push Up":
        push_up_exerc = push_up(int(info.number_reps), json_folder)
        reps, no_reps = push_up_exerc.check_exercise()
        print("reps: " + str(reps))
        print("no_reps: " + str(no_reps))
    
    elif str(info.exercise_in_video) == "Front Squat":
        front_squat_exerc = front_squat(int(info.number_reps), json_folder)
        reps, no_reps = front_squat_exerc.check_exercise()
        print("reps: " + str(reps))
        print("no_reps: " + str(no_reps))

    else:
        print("alguma coisa correu mal no teste das squats")

    info.number_correct_reps = str(reps)
    info.number_incorrect_reps = str(no_reps)
    info.video_status="evaluated"
    info.save()

    for filename in os.listdir(json_folder):
        file_path = os.path.join(json_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))