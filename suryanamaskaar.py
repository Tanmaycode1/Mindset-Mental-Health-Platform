import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def rescale_frames(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

cap = cv2.VideoCapture(0)
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    degrees = np.abs(radians * 180.0 / np.pi)

    if degrees > 180:
        degrees = 360 - degrees

    return degrees
def distance(a, b):
    a = np.array(a)
    b = np.array(b)

    length = np.sqrt(np.square(a[0]-b[0]) + np.square(a[1]-b[1]))

    return length
def main():
 with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                   mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                   mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        try:
            landmarks = results.pose_landmarks.landmark
            shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow_left = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist_left = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee_left = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle_left = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee_right = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
            incline_left = calculate_angle(hip_left, shoulder_left, elbow_left)
            bottom_angle_left = calculate_angle(ankle_left, knee_left, hip_left)
            torso_angle_left = calculate_angle(knee_left, hip_left, shoulder_left)

            angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)
            incline_right = calculate_angle(hip_right, shoulder_right, elbow_right)
            bottom_angle_right = calculate_angle(shoulder_right, elbow_right, hip_right)
            torso_angle_right = calculate_angle(knee_right, hip_right, shoulder_right)

            gap = distance(wrist_right, wrist_left)

            if incline_left >= 10 and incline_right >= 10 and angle_right <= 45 and angle_left <= 45 and torso_angle_right >= 150 and torso_angle_left >= 150 and bottom_angle_right >= 80 and bottom_angle_left >= 80 and gap <= 0.07:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1),
                                                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
                    p1 = True
                    cv2.putText(image, "Pose1 completed!", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 3)

            if torso_angle_right >= 160 and torso_angle_left >= 160 and angle_right >= 90 and angle_left >= 90 and incline_right >= 100 and incline_left >= 100:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1),
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
                    p2 = True
                    cv2.putText(image, "Pose2 completed!", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 3)

            if incline_left >= 60 and incline_right >= 60 and angle_right >= 90 and angle_left >= 90 and torso_angle_right >= 90 and torso_angle_left >= 90 and bottom_angle_left >= 100 :
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1),
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
                    p3 = True
                    cv2.putText(image, "Pose3 completed!", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 3)

            if torso_angle_right >= 170 and torso_angle_left >= 170 and angle_left >= 90 and angle_right >= 90 and bottom_angle_right <= 150 and bottom_angle_left <= 150:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1),
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
                    p4 = True
                    cv2.putText(image, "Pose4 completed!", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 3)

            if angle_left <= 30 and angle_right <= 30 and gap <= 0.07 and torso_angle_left >= 170 and torso_angle_right >= 170 and bottom_angle_right <= 70 and bottom_angle_left <= 70 and incline_right >= 150 and incline_right >= 150:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1),
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
                    cv2.putText(image, "Pose5 completed!", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 3)

        except:
            pass

        cv2.imshow("Mediapipe Image", image)

def stop():
 cap.release()
 cv2.destroyAllWindows()






