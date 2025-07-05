import pandas as pd
import statistics
import os
import cv2
import math
import time

videos = []

for file in os.listdir('videos/'):
    videos.append(file)

file = pd.read_csv('landmarks.csv')

current_row = '0'
hip, knee, ankle, shoulder, left_wrist, right_wrist, elbow = None, None, None, None, None, None, None
knee_angle, hand_distance, hip_angle, elbow_angle, stage = '', '', '', '', ''
knees = []

landmark_pairs = {
    'hip': ('23', '24'),
    'knee': ('25', '26'), 
    'ankle': ('27', '28'),
    'shoulder': ('11', '12'),
    'elbow': ('13', '14'),
    'left_wrist': ('15', '15'),
    'right_wrist': ('16', '16')
}

landmarks = {}
if 'seen' not in videos[0]:
    for row in file.iterrows():
        dicted = row[1].to_dict()

        if dicted['iter'] == 'break':
            cap = cv2.VideoCapture(f'videos/{videos[0]}')
            success, img = cap.read()
            while True:
                success, img = cap.read()
                try:
                    cv2.imshow('Video', img)
                    time.sleep(0.02)
                    cv2.waitKey(1)
                except Exception as e:
                    print(e)
                    break

            cap.release()
            cv2.destroyAllWindows()
            rating = input("""Please rate this rowers technique with this criteria: 1 = Good Tech, 2 = Lean back too far, 3 = Lean forward too far,
                        4 = Pulling hands too early, 5 = Heels to wheels, 6 = Hands not close together, 7 = Dipping at the catch,
                        8 = Hanging at the catch, 9 = Hanging at the finish, 10 = Back swinging too early, 11 = Extending hands too early """)
            
            df = pd.DataFrame({
                'stage' : [''],
                'knee_angle' : [''],
                'hand_distance' : [''],
                'hip_angle' : [''],
                'elbow_angle' : [''],
                'Rating' : [rating]
            })

            df.to_csv('cleaned.csv', mode='a', header=False, index=False)
            os.rename(f'videos/{videos[0]}', f'videos/seen_{videos[0]}')
            videos.pop(0)
        
        if str(dicted['iter']) == current_row:
            landmarks[str(dicted['id'])] = [dicted['x'], dicted['y']]
            
        else:
            processed = {}
            for body_part, (left_id, right_id) in landmark_pairs.items():
                left = landmarks.get(str(float(left_id)))
                right = landmarks.get(str(float(right_id)))

                if left and right:
                    processed[body_part] = [(left[0] + right[0]) / 2, (left[1] + right[1]) / 2]
                elif left:
                    processed[body_part] = left
                elif right:
                    processed[body_part] = right

            if 'knee' in processed:
                knee = processed['knee']
            if 'hip' in processed:
                hip = processed['hip']
            if 'shoulder' in processed:
                shoulder = processed['shoulder']
            if 'ankle' in processed:
                ankle = processed['ankle']
            if 'elbow' in processed:
                elbow = processed['elbow']
            if 'left_wrist' in processed:
                left_wrist = processed['left_wrist']
            if 'right_wrist' in processed:
                right_wrist = processed['right_wrist']

            if len(knees) >= 2:
                if knee[1] > knees[-1] and knee[1] > knees[-2] and knee[1] > knees[-3]:
                    stage = 'Drive'
                else:
                    stage = 'Recovery'

            if hip and knee and ankle:
                ankle_knee = math.sqrt(abs(knee[1] - ankle[1]) ** 2 + abs(knee[0] - ankle[0]) ** 2)
                hip_knee = math.sqrt(abs(knee[1] - hip[1]) ** 2 + abs(knee[0] - hip[0]) ** 2)
                ankle_hip = math.sqrt(abs(ankle[1] - hip[1]) ** 2 + abs(ankle[0] - hip[0]) ** 2)

                divider = ankle_knee ** 2 - (hip_knee **2 + ankle_hip ** 2) 
                ratio = divider / (-2 * hip_knee * ankle_hip )
                knee_angle = math.degrees(math.acos(ratio))

            if hip and shoulder:
                hip_angle = math.degrees(math.atan(abs(shoulder[1] - hip[1]) / abs(shoulder[0] - hip[0])))

            if left_wrist and right_wrist:
                hand_distance = abs(right_wrist[1] - left_wrist[1])

            if right_wrist and shoulder and elbow:
                wrist_elbow = math.sqrt(abs(right_wrist[0] - elbow[0]) ** 2 + abs(right_wrist[1] - elbow[1]) ** 2)
                shoulder_elbow = math.sqrt(abs(shoulder[0] - elbow[0]) ** 2 + abs(shoulder[1] - elbow[1]) ** 2)
                wrist_shoulder = math.sqrt(abs(right_wrist[0] - shoulder[0]) ** 2 + abs(right_wrist[1] - shoulder[1]) ** 2)

                divider = wrist_shoulder ** 2 - (shoulder_elbow ** 2 + wrist_elbow ** 2)
                if shoulder_elbow and wrist_elbow != 0:
                    ratio = divider / (-2 * shoulder_elbow * wrist_elbow)
                elbow_angle = math.degrees(math.acos(ratio))


            df = pd.DataFrame({
                'stage' : [stage],
                'knee_angle' : [knee_angle],
                'hand_distance' : [hand_distance],
                'hip_angle' : [hip_angle],
                'elbow_angle' : [elbow_angle],
                'Rating' : [''],

            })

            df.to_csv('cleaned.csv', mode='a', header=False, index=False)

            if knee:
                knees.append(knee[1])
            hip, knee, ankle, shoulder, left_wrist, right_wrist, elbow = None, None, None, None, None, None, None


            current_row = str(dicted['iter'])

else:
    videos.pop(0)