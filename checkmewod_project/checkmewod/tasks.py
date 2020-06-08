from __future__ import absolute_import, unicode_literals

from celery import shared_task
from checkmewod.models import VideoSubmission
from checkmewod.video_evaluation_src.body_detection_openpose import body_detect
from checkmewod.video_evaluation_src.air_squat import air_squat
from checkmewod.video_evaluation_src.front_squat import front_squat
from checkmewod.video_evaluation_src.press import press
from checkmewod.video_evaluation_src.pull_up import pull_up
from checkmewod.video_evaluation_src.push_up import push_up
from checkmewod.video_evaluation_src.back_squat import back_squat
from checkmewod.video_evaluation_src.deadlift import deadlift 
from django.conf import settings
from django.core.mail import send_mail
from checkmewod_project import settings
import os, shutil
from moviepy.editor import *


@shared_task
def send_email(id):
    info = VideoSubmission.objects.get(video_id=id)
    video_name = str(info.video_file).split("/")

    print(settings.EMAIL_HOST_PASSWORD)

    subject = 'Video Submission results'
    from_ = 'checkmewod@gmail.com'
    to_ = [str(info.user_email.email)]

    message = 'Hi ' + str(info.user_email.first_name) + ', \n\nYou recently submitted a video by the name of ' + video_name[-1] + ' where you were performing ' + str(info.exercise_in_video) + ' and executed ' + str(info.number_reps) + ' repetitions. Your results just came out and are the following:\n \
        ' + str(info.number_correct_reps) + ' correct repetitions \n \
        ' + str(info.number_incorrect_reps) + ' incorrect repetitions \n\nYou can visit your profile and check the corresponding video to see which repetitions you failed and which you passed. \n\nBest Regards, \nThe CheckMeWOD Team'

    send_mail(subject, message, from_, to_)


@shared_task
def border_video(frames_per_rep, id):
    info = VideoSubmission.objects.get(video_id=id)
    start_time=0
    video = VideoFileClip(str(info.video_file))
    frame_rate=video.fps
    duration = video.duration

    cnt = 1
    num = len(frames_per_rep)

    list=[]

    if video.rotation in (90, 270):
        video = video.resize(video.size[::-1])
        video.rotation = 0
    
    for frame in frames_per_rep.keys():
        if cnt == num:
            end_time = duration
        else:
            end_time = frame/frame_rate
        clip1 = video.subclip(start_time, end_time)
        if frames_per_rep[frame] == "rep":
            clip1 = clip1.margin(top=80, bottom=80, left=80, right=80, color=(124,252,0))
        elif frames_per_rep[frame] == "no rep":
            clip1 = clip1.margin(top=80, bottom=80, left=80, right=80, color=(255,0,0))
        list.append(clip1)
        start_time = end_time
        cnt+=1

    final_clip = concatenate_videoclips(list)
    temp_location = "checkmewod/static/media/videos/uploaded_files/temporary.mp4"
    final_clip.write_videofile(temp_location )
    os.remove(str(info.video_file))
    os.rename(temp_location, str(info.video_file))

@shared_task
def evaluate_video(id):
    info = VideoSubmission.objects.get(video_id=id)
    body_detect(str(info.video_file))
    json_folder = "/home/daniel/uni/CheckMeWOD/checkmewod_project/checkmewod/video_evaluation_src/output_json/"
    reps = None
    no_reps = None
    frames_per_rep = None
    if str(info.exercise_in_video) == "Air Squat":
        air_squat_exerc = air_squat(int(info.number_reps), json_folder)
        reps, no_reps, frames_per_rep = air_squat_exerc.check_exercise()

    elif str(info.exercise_in_video) == "Press":
        press_exerc = press(int(info.number_reps), json_folder)
        reps, no_reps, frames_per_rep = press_exerc.check_exercise()

    elif str(info.exercise_in_video) == "Pull Up":
        pull_up_exerc = pull_up(int(info.number_reps), json_folder)
        reps, no_reps, frames_per_rep = pull_up_exerc.check_exercise()

    elif str(info.exercise_in_video) == "Push Up":
        push_up_exerc = push_up(int(info.number_reps), json_folder)
        reps, no_reps, frames_per_rep = push_up_exerc.check_exercise()
    
    elif str(info.exercise_in_video) == "Front Squat":
        front_squat_exerc = front_squat(int(info.number_reps), json_folder)
        reps, no_reps, frames_per_rep = front_squat_exerc.check_exercise()

    elif str(info.exercise_in_video) == "Back Squat":
        back_squat_exerc = back_squat(int(info.number_reps), json_folder)
        reps, no_reps, frames_per_rep = back_squat_exerc.check_exercise()

    elif str(info.exercise_in_video) == "Deadlift":
        deadlift_exerc = deadlift(int(info.number_reps), json_folder)
        reps, no_reps, frames_per_rep = deadlift_exerc.check_exercise()

    else:
        print("alguma coisa correu mal no teste das squats")

    print("reps: " + str(reps))
    print("no_reps: " + str(no_reps))
    print("frames_per_rep: " + str(frames_per_rep))
    info.number_correct_reps = str(reps)
    info.number_incorrect_reps = str(no_reps)
    info.frames_per_rep = str(frames_per_rep)
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

    send_email(id)
    border_video(frames_per_rep, id)



    