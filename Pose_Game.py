import cv2
import mediapipe as mp
import time
import random
HEIGHT = 720
WIDTH = 1280
recSize = 100
mpPose = mp.solutions.pose
pose = mpPose.Pose()
cap = cv2.VideoCapture(0)
t = 0
points = 0
mpDraw = mp.solutions.drawing_utils

recX = random.randint(0, WIDTH - recSize)
recY = random.randint(0, HEIGHT - recSize)


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            if id == 19 or id == 20:    
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 20, (255, 0, 0), cv2.FILLED)
                if cx > recX and cx < (recX + recSize) and cy > recY and cy < (recY + recSize):
                    points += 1
                    recX = random.randint(0, WIDTH - recSize)
                    recY = random.randint(0, HEIGHT - recSize)


    cTime = time.time()
    fps = 1/(cTime - t)
    t = cTime



    cv2.putText(img, "FPS:" + str(int(fps)), (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv2.putText(img, "Points:" + str(points), (70, 130), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv2.rectangle(img, (recX, recY), (recX + recSize, recY + recSize), (0, 255, 0), cv2.FILLED)


    cv2.imshow("image", img)
    cv2.waitKey(1)