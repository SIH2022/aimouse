import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
from pynput.keyboard import Key,Controller
from pynput.mouse import Button\
    ,Controller as mouse_c
import keyboard as kboard

###########################################
wCam,hCam = 640,480
pTime =0
frameR = 100 #Frame Reduction
smoothening = 20
#############################################
#############################################
keyboard = Controller()
mouse_ = mouse_c()
############################################
plocX,plocY = 0,0
clocX,clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)
wScr,hScr = autopy.screen.size()
print(wScr,hScr)

while True:
    #1. Find hand Landmarks
    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    #2. Get the tip of the index and middle finger
    if len(lmList) !=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        #print(x1,y1,x2,y2)
    #3. Check which fingers are up
        fingers = detector.fingerUp()
        print(fingers)
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        #4. Only Index Finger : Moving Mode
        if fingers[1] ==1 and fingers[2] == 0:
        #5. Convert Coordinates
           x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
           y3 = np.interp(y1, (frameR,hCam-frameR), (0, hScr))
           #6. Smoothen value
           clocX = plocX + (x3-plocX)/smoothening
           clocY = plocY + (x3 - plocY) / smoothening


           #7. Move Mouse
           autopy.mouse.move(wScr-x3,y3)
           cv2.circle(img,(x1,y1),8,(255,0,255),cv2.FILLED)
           plocX,plocY = clocX,clocY

        ## Drag and Drop
        if fingers[1] ==1 and fingers[0] == 1:
        #5. Convert Coordinates
           x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
           y3 = np.interp(y1, (frameR,hCam-frameR), (0, hScr))
           #6. Smoothen value
           clocX = plocX + (x3-plocX)/smoothening
           clocY = plocY + (x3 - plocY) / smoothening

           #7. Move Mouse
           #autopy.mouse.move(wScr-x3,y3)
           mouse_c.position = (wScr-x3,y3)
           length, img, lineInfo = detector.findDistance(4, 8, img)
           #cv2.circle(img,(x1,y1),8,(255,0,255),cv2.FILLED)
           plocX, plocY = clocX, clocY
           while mouse_c.position != (wScr-x3,y3):
               pass

          # print(length)
          # 10.Click mouse if distance short
           print(length)
           if (length < 50):
               cv2.circle(img, (lineInfo[4], lineInfo[5]), 9, (0, 255, 0), cv2.FILLED)
               mouse_.press(Button.left)
           else:
               mouse_.release(Button.left)


        #8. Both Index and Middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between fingers
            length,img,lineInfo = detector.findDistance(8,12,img)
            #print(length)
            # 10.Click mouse if distance short
            if(length<40):
                cv2.circle(img,(lineInfo[4],lineInfo[5]),9,(0,255,0),cv2.FILLED)
                autopy.mouse.click()

        # Scroll Up
        if fingers[4] == 1:
            kboard.press_and_release("down arrow")
        # Scroll Down
        if fingers[0] == 1:
            kboard.press_and_release("up arrow")
        # select and move
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] ==1:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen value
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (x3 - plocY) / smoothening

            # 7. Move Mouse
            autopy.mouse.click()
            autopy.mouse.move(wScr - x3, y3)
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        # Copy
        '''if fingers[4] == 1:
            autopy.mouse.click()
            kboard.press_and_release('ctrl+c')
        if fingers[3] == 1 and fingers[4] == 1:
            kboard.press('ctrl+v')'''



    #11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)




