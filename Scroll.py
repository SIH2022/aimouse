import cv2
import time

import keyboard

import HandTrackingModule as htm
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller

mouse = Controller()
keyboard = Controller()
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector()
frameR = 100

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1 = lmList[8][1:]
        y1 = lmList[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 255, 255), 2)

        if fingers[1] == 1 and fingers[2] == 1:
            length, img, info = detector.findDistance(8, 12, img)
            print(length)
            if length <= 30:
                keyboard.press(Key.up)
                keyboard.release(Key.up)
                cv2.circle(img, (info[4], info[5]), 10, (0, 255, 0), cv2.FILLED)

            if length > 30 and length <= 50:
                keyboard.press(Key.down)
                keyboard.release(Key.down)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
