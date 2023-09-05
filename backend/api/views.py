from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework import viewsets
from .models import Video
from .serializers import VideoSerializer
from noddingpigeon.inference import predict_video
from noddingpigeon.video import VideoSegment  # Optional.
import os
import logging
import cv2
import numpy as np


logger = logging.getLogger(__name__)

face_cascade = cv2.CascadeClassifier(r'C:\Users\Umang\Desktop\reactdjangop2\backend\api\haarcascade_frontalface_default.xml')


var = 0
y_old = flag_y = x_old = flag_x = 0
sign_x = sign_y = sign_a = sign_b = 0
del_x = del_y = 0
Yes = No = 0

def help(path):
    global sign_a, sign_b, flag_x, del_x, del_y, No, flag_y, del_x, del_y, flag_f_y, Yes, var, y_old, x_old, sign_x, sign_y
    def face_return(faces):  # Removes background faces 
        maxx = faces[0, 2] + faces[0, 3]
        face = faces[0, :]
        for x, y, w, h in faces:
            if (h + w) > maxx:
                face = np.array([x, y, w, h])

        face = face.reshape(1, 4)
        return face  # Returning face closest to cam


    def yes():  # Counts number of head nods
        global flag_y, del_x, del_y, flag_f_y, Yes
        if flag_y > 0:
            flag_y -= 1

        if del_y <= 3 and del_y >= -3 and flag_y > 0:
            Yes += 1
            flag_y = 0

        if del_y < -6:
            flag_y = 10
        else:
            flag_y -= 1


    def no():  # Counts number of head shakes
        global sign_a, sign_b, flag_x, del_x, del_y, No
        if del_x > 6 and sign_a == 0:
            sign_a = 15
        elif del_x < -6 and sign_b == 0:
            sign_b = 15

        if sign_a > 0:
            sign_a -= 1
        elif sign_b > 0:
            sign_b -= 1

        if sign_a > 0 and sign_b > 0 and flag_x == 0:
            flag_x = 20

        if flag_x > 0:
            if del_x > -4 and del_x < 4:
                No += 1
                flag_x = 0
                sign_a = 0
                sign_b = 0
            else:
                flag_x -= 1
                if flag_x == 0:
                    sign_a = 0
                    sign_b = 0

    video_capture = cv2.VideoCapture(path)  # Replace 'path_to_video' with the actual video file path

# Get video dimensions and calculate output window size
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    window_size = (width, height)

    # Initialize font scale based on video resolution
    font_scale = min(width, height) / 1000.0

    # Initializing variables and flags
    var = 0
    y_old = flag_y = x_old = flag_x = 0
    sign_x = sign_y = sign_a = sign_b = 0
    del_x = del_y = 0
    Yes = No = 0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter('processed/output.mp4', fourcc, 20.0, window_size)

    cv2.namedWindow("video", cv2.WINDOW_NORMAL)  # Create a resizable window
    cv2.resizeWindow("video", window_size)  # Set window size to match video resolution

    while True:
        ret, frame = video_capture.read()

        if not ret:  # Break loop if video reading is finished
            break

        # Draw "Yes" and "No" text on the frame
        text = "Yes = " + str(Yes)
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
        cv2.putText(frame, text, (30, 50 + text_size[1] * 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 2)

        text = "No = " + str(No)
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
        cv2.putText(frame, text, (30, 76 + text_size[1] * 3), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 2)

        # cv2.imshow("video", frame)
        output_video.write(frame)  # Write frame to output video

        # Taking every third frame
        if var % 3 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Skips current iteration if no face is detected
            if isinstance(faces, tuple):
                continue

            face = faces[0, :]
            face = face_return(faces)  # Calling face_return function to remove background faces

            for (x, y, w, h) in face:
                # Code to calculate forehead position if user changes position
                if del_x > 5 or del_x < -5:
                    sign_x += 1
                    if sign_x > 20:
                        x_old = x + w / 2
                        y_old = y + h / 3
                        flag_f_y = sign_a = sign_b = flag_x = flag_y = 0
                else:
                    sign_x = 0

                if del_y > 5 or del_y < -5:
                    sign_y += 1
                    if sign_y > 20:
                        x_old = x + w / 2
                        y_old = y + h / 3
                        flag_f_y = sign_a = sign_b = flag_x = flag_y = 0
                else:
                    sign_y = 0

                # Calculating distance moved by forehead
                del_y = ((y_old - (y + h / 3)) / h) * 100
                del_x = ((x_old - (x + w / 2)) / w) * 100

                # Functions to calculate head nods and shakes
                yes()
                no()

        var = var + 1
        if cv2.waitKey(1) == 27:  # Press Escape to close program
            break

    video_capture.release()
    output_video.release()  # Release the output video writer
    cv2.destroyAllWindows()
    return os.path.abspath('processed/output.mp4')


def process_video(video_path):
    # Open the video file
    print("4")
    print(video_path)
    try:
        result=help(video_path)
    # Continue with the code to handle the result
    except Exception as e:
    # Handle the exception or error case
        print("An error occurred during video prediction:", str(e))
    print(result)
    return result

def process_uploaded_video(video):
    video_path = video.video_file.path

    processed_result = process_video(video_path)
    return processed_result

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        video = serializer.save()
        processed_result = process_uploaded_video(video)
        serializer.instance.processed_result = processed_result
        video.video_file.delete()
        video.delete()
        # serializer.save()