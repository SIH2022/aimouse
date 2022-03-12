# Importing Modules..

import cv2
import time
import HandTrackingModule as htm
from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Key, Controller as keyboardController
from tkinter import *

mouse = mouseController()
keyboard = keyboardController()
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector()
frameR = 100
root = Tk()

def isAccepted():
    print("yes")

# Coding Gestures...
while True:
    # Taking Image...
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Create a frame...
    app = Frame(root, bg="white")
    app.grid()

    if len(lmList) != 0:
        x1 = lmList[8][1:]
        y1 = lmList[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 255, 255), 2)

        # Scrolling Up Down Gesture...
        # if fingers[1] == 1 and fingers[2] == 1:
        #     length, img, info = detector.findDistance(8, 12, img)
        #     if length <= 30:
        #         keyboard.press(Key.up)
        #         keyboard.release(Key.up)

            # if length > 30:
            #     keyboard.press(Key.down)
            #     keyboard.release(Key.down)

        # Exit File Gesture...
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[2] == 0:
            print("Exit File Working....")
            with keyboard.pressed(Key.ctrl):
                keyboard.press("S")
                keyboard.release("S")

        # Save File Gesture...
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[2] == 0:
            with keyboard.pressed(Key.ctrl):
                keyboard.press("S")
                keyboard.release("S")



    cv2.imshow("Image", img)
    cv2.waitKey(1)
