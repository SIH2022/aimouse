import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller as mouseController

wCam, hCam = 640, 480
pTime = 0
frameR = 100
smoothening = 10
keyboard = Controller()
mouse_ = mouseController()

plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=2)
wScr, hScr = 1368, 768
print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, 0)

    # 2. Get the tip of the index and middle finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingerUp()

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen value
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (x3 - plocY) / smoothening

            # 7. Move Mouse
            autopy.mouse.move(int(wScr - x3), int(y3))
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Drag and Drop
        if fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen value
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (x3 - plocY) / smoothening

            # 7. Move Mouse
            # autopy.mouse.move(wScr-x3,y3)
            mouseController.position = (wScr - x3, y3)
            length, img, lineInfo = detector.findDistance(4, 8, img)
            # print("len ",length)
            # cv2.circle(img,(x1,y1),8,(255,0,255),cv2.FILLED)
            plocX, plocY = clocX, clocY
            while mouseController.position != (wScr - x3, y3):
                pass

            # print(length)
            # 10.Click mouse if distance short
            print(length)
            if (length < 50):
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 9, (0, 255, 0), cv2.FILLED)
                mouse_.press(Button.left)
            else:
                mouse_.release(Button.left)

        # 8. Both Index and Middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # print(length)
            # 10.Click mouse if distance short
            if (length < 40):
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 9, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
