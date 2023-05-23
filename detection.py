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

img_1 = cv2.imread("images/namaskar.jpg")
resize_img_1 = rescale_frames(img_1)
cv2.imshow("Namaskar Pose", resize_img_1)

img_2 = cv2.imread("images/t-pose.jpg")

resize_img_2 = rescale_frames(img_2)
cv2.imshow("T-Pose", resize_img_2)

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
            shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
            incline_left = calculate_angle(hip_left, shoulder_left, elbow_left)
            angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)
            incline_right = calculate_angle(hip_right, shoulder_right, elbow_right)

            gap = distance(wrist_right, wrist_left)

            # cv2.putText(image, str(angle_left),
            #             tuple(np.multiply(elbow_left, [640, 480]).astype(int)),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # cv2.putText(image, str(angle_right),
            #             tuple(np.multiply(elbow_right, [640, 480]).astype(int)),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # T-pose:
            if angle_left >= 160 and angle_right >= 160 and incline_right >= 70 and incline_left >= 70:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1),
                                          mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
                cv2.putText(image, "T-Pose completed!", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 3)

            # Namaskar pose:
            if angle_left <= 60 and angle_right <= 60 and gap <= 0.07:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1),
                                          mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
                cv2.putText(image, "Namaskar completed!", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 3)
        except:
            pass

        cv2.imshow("Mediapipe Image", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

def stopping():
  cap.release()
  cv2.destroyAllWindows()



main()