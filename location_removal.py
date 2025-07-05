import mediapipe as mp
import pandas as pd
import time
import cv2
import os

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

for file in os.listdir('videos/'):
    if 'seen' not in file:
        cap = cv2.VideoCapture(f'videos/{file}')
        locations = {}
        iter = -1

        success, img = cap.read()
        while True:
            iter += 1
            success, img = cap.read()
            if not success:
                break
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            if results.pose_landmarks:
                mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                for id, landmark in enumerate(results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(landmark.x*w), int(landmark.y* h)
                    if id > 10:
                        locations[id] = (cx, cy)
                        df = pd.DataFrame({'iter' : [iter], 'id' : [id], 'x' : [cx], 'y' : [cy]}) 
                        df.to_csv('landmarks.csv', mode='a', header=False, index=False)

        cap.release()
        print('broken')
        df = pd.DataFrame({'iter' : ['break'], 'id' : [''], 'x' : [''], 'y' : ['']}) 
        df.to_csv('landmarks.csv', mode='a', header=False, index=False)