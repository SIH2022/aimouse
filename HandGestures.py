# Importing Modules..

import cv2
import time
import HandTrackingModule as htm
from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Key, Controller as keyboardController
import os
import ctypes
from PIL import ImageTk
import PIL.Image
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
# import AImouse as ai

# ai = ai.AIMouse()
mouse = mouseController()
keyboard = keyboardController()
wCam, hCam = 640, 480
# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)
detector = htm.handDetector()
frameR = 100


class HandGesture:
    def handGestures(self, frame):
        flag = 0
        # detecting Hand...
        enableMouse = False
        img = detector.findHands(frame)
        lmList, bbox = detector.findPosition(img)

        if len(lmList) != 0:
            # x1 = lmList[8][1:]
            # y1 = lmList[12][1:]

            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 255, 255), 2)

            # Scrolling Up Down Gesture...
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, info = detector.findDistance(8, 12, img)
                if length <= 30:
                    keyboard.press(Key.up)
                    keyboard.release(Key.up)
                    time.sleep(0.5)
                    cv2.circle(img, (info[4], info[5]), 10, (0, 255, 0), cv2.FILLED)

                if length > 30:
                    keyboard.press(Key.down)
                    keyboard.release(Key.down)
                    time.sleep(0.5)

            # Index
            # print(fingers)
            # if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            #     print("Index is showing...")
            #     index_root = tk.Toplevel()
            #     canvas = tk.Canvas(index_root, width=100,height=100)
            #     canvas.pack()
            #     folder_path = "/home/vikasjoshis001/Desktop/Handtracking/FingerImages"
            #     img_list = os.listdir(folder_path)
            #     for imPath in img_list:
            #         img = ImageTk.PhotoImage(PIL.Image.open(f'{folder_path}/{imPath}'))
            #     canvas.create_image(20, 20, anchor=NW,image=img)
            #     index_root.mainloop()

            # Enable Mouse
            # if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 1:
            #     if not enableMouse:
            #         enableMouse = True
            #     else:
            #         enableMouse = False
            #
            # if enableMouse:
            #     ai.aiMouse(frame)

            # Save File Gesture...
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                print("Save Gesture running...")
                with keyboard.pressed(Key.ctrl):
                    keyboard.press("S")
                    keyboard.release("S")

            # Exit File Gesture...
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                print("Exit Gesture running...")
                with keyboard.pressed(Key.ctrl):
                    keyboard.press(Key.f4)
                    keyboard.release(Key.f4)

            # Lock Unlock Screen Gesture...
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                print("Lock Gesture running...")
                try:
                    os.popen('gnome-screensaver-command --lock')
                except:
                    ctypes.windll.user32.LockWorkStation()

            # Shutdown Gesture...
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                print("Shutting Down...")
                cfrmCommand = "poweroff"
                cancelCommand = "shutdown -c"
                HandGesture().generateBox("Shutdown", cfrmCommand, cancelCommand)
                exit()

            # Restart Gesture...
            if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                print("Restarting Down...")
                cfrmCommand = "reboot"
                cancelCommand = "shutdown -c"
                if flag == 0:
                    HandGesture().generateBox("Restart", cfrmCommand, cancelCommand)
                    flag = 1

            # im = cv2.imshow("Image", img)
            return img

    def msgBox(self, msg, cfrmCommand, cancelCommand):
        res = mb.askquestion('Exit Application',
                             'Do you really want to ' + msg)
        if res == 'yes':
            os.system(cfrmCommand)

        else:
            return

    def generateBox(self, msg, cfrmCommand, cancelCommand):
        root = tk.Tk()
        HandGesture().msgBox(msg, cfrmCommand, cancelCommand)
        print("HELLO")
        return

# def main():
#     # Coding Gestures...
#     while True:
#         # Taking Image...
#         success, img = cap.read()
#         img = detector.findHands(img)
#         gesture = HandGesture()
#         gesture.handGestures(img)
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
# #
# if __name__ == "__main__":
#     main()
