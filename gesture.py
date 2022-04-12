import cv2
from cvzone.HandTrackingModule import HandDetector

import cv2
import numpy as np
import time
import autopy
from pynput.keyboard import Key,Controller
from pynput.mouse import Button,Controller as mouseController
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


############## PyCaw #####################

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
min_vol = volRange[0]
max_vol = volRange[1]
#volume.SetMasterVolumeLevel(-20.0, None)
######################################

###########################################
wCam,hCam = 640,480
pTime =0
frameR = 70 #Frame Reduction
smoothening = 10

plocX,plocY = 0,0
clocX,clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
wScr,hScr = autopy.screen.size()
#print(wScr,hScr)
#############################################

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8,maxHands=2)

while True:
    success,img = cap.read()
    hands,img= detector.findHands(img,flipType=False)
    #hands, img = detector.findHands(img)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)


    if len(hands) == 2:
        hand2 = hands[1]
        hand1 = hands[0]
        lmList2 = hand2['lmList']
        #print(lmList2)
    elif len(hands) == 1:
        hand1 = hands[0]
        lmList1 = hand1['lmList']
        bbox1 = hand1["bbox"]
        centerPoint1= hand1["center"]
        handType1 = hand1["type"]
        fingers1 = detector.fingersUp(hand1)

        x1, y1 = lmList1[8][:2]
        x2, y2 = lmList1[12][:2]

        if fingers1[1] ==1 and fingers1[2] ==0 :
           #print(lmList1[8])
        #5. Convert Coordinates
           x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
           y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))
           #6. Smoothen value
           clocX = plocX + (x3 - plocX)/smoothening
           clocY = plocY + (y3 - plocY)/smoothening

           #7. Move Mouse
           try:
               autopy.mouse.move(wScr - x3, y3)
               cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
           except:
               continue
           plocX,plocY = clocX,clocY

        if fingers1[1] ==1 and fingers1[2] ==1 :
            length,info,img = detector.findDistance(lmList1[8][:2],lmList1[12][:2],img)
            print(info)
            if length<20:
                autopy.mouse.click()
        #print(fingers1)
        #print(lmList1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)