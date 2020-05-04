# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import json
import numpy as np
import argparse

# check openpose installation folder before executing
# paths might need to be changed acording to the openpose installation folder
def body_detect(video):
    try:
        # Import Openpose (Windows/Ubuntu/OSX)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('/home/daniel/openpose/build/python/');
            
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            
            # este import esta a estragar o celery

            import pyopenpose as op
            
        except ImportError as e:
            print(e)
            print(
                'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

        # Flags
        parser = argparse.ArgumentParser()
        parser.add_argument("--video", default="/home/daniel/uni/CheckMeWOD/checkmewod_project/"+video, help="Process a video.")
        args = parser.parse_known_args()
        
        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = '/home/daniel/openpose/models/'
        params["face"] = False
        params["hand"] = False

        # Add others in path?
        for i in range(0, len(args[1])):
            curr_item = args[1][i]
            if i != len(args[1]) - 1:
                next_item = args[1][i + 1]
            else:
                next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-', '')
                if key not in params:  params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-', '')
                if key not in params: params[key] = next_item

        # Construct it from system arguments
        # op.init_argv(args[1])
        # oppython = op.OpenposePython()

        # Starting OpenPose
        
        keypointlist = []
        keypointdict = {}

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        
        opWrapper.configure(params)
        
        opWrapper.start()

        # Process video
        datum = op.Datum()
        
        frame_num = 0
        
        cap = cv2.VideoCapture(args[0].video)
        
        while (cap.isOpened()):
            hasframe, frame = cap.read()
            
            if hasframe == True:
                
                datum.cvInputData = frame
                
                opWrapper.emplaceAndPop([datum])
                
                # Display video
                keypointdict['body keypoint'] = np.array(datum.poseKeypoints).tolist()
                
                keypointlist.append(keypointdict.copy())  # must be the copy!!!
                
                #cv2.imshow("OpenPose 1.5.0 - Tutorial Python API", datum.cvOutputData)
                
                filename = "/home/daniel/uni/CheckMeWOD/checkmewod_project/checkmewod/video_evaluation_src/output_json/frame_number_" + str(frame_num) + ".json"
                
                with open(filename, "a") as f:
                
                    json.dump(keypointlist, f, indent=0)
                frame_num += 1
                
                cv2.waitKey(1)
            else:
                break
    except Exception as e:
        # print(e)      
        sys.exit(-1)
