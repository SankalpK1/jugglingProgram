import cv2
import numpy as np
# import math
# import colorsys
from window_info import *


cam = cv2.VideoCapture(0)
i=0
global img

frameNum = []

numClicked = 0

numBalls = 0

hsv_values = []

hsv_values2 = []

hsv_ranges = []

positions = []

existsLine = 0

xVelocity = []

yVelocity = []

xVelocityPrev = []

yVelocityPrev = []
speed=65
numThrown = 0
timestamp=0
check=False
cpts=[]
play=True
def main():
    global speed
    global play
    global i
    global timestamp
    global cam
    global check
    global img

    global frameNum

    global numClicked

    global numBalls

    global hsv_values

    global hsv_values2

    global hsv_ranges

    global positions

    global existsLine

    global xVelocity

    global yVelocity

    global xVelocityPrev

    global yVelocityPrev

    global numThrown


    cam = cv2.VideoCapture("hopefully.mp4")

    frameNum = []

    numClicked = 0

    numBalls = 0

    hsv_values = []

    hsv_values2 = []

    hsv_ranges = []

    positions = []

    existsLine = 0

    xVelocity = []

    yVelocity = []

    xVelocityPrev = []

    yVelocityPrev = []

    yHeight = 300

    isAbove = []
    global cpts




    numThrown = 0
    def onmouse(event, x, y, flags, param):
        global numBalls
        global cpts
        global numClicked
        if event == cv2.EVENT_LBUTTONDOWN:
            cpts.append((x,y))
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            (h,s,v) = cv2.split(img2)
            print(h[y][x])
            # print(countSelected)
            hsv_values.append([h[y][x],s[y][x],v[y][x]])
            print (hsv_values)
            numClicked+=1
            if numClicked == 3:
                numBalls+=1
                hsv_ranges.append(max(hsv_values[numBalls*3-3][0], hsv_values[numBalls*3-2][0], hsv_values[numBalls*3-1][0]))
                hsv_ranges[numBalls*3-3] -= min(hsv_values[numBalls*3-3][0], hsv_values[numBalls*3-2][0], hsv_values[numBalls*3-1][0])
                hsv_ranges.append(max(hsv_values[numBalls*3-3][1], hsv_values[numBalls*3-2][1], hsv_values[numBalls*3-1][1]))
                hsv_ranges[numBalls*3-2] -= min(hsv_values[numBalls*3-3][1], hsv_values[numBalls*3-2][1], hsv_values[numBalls*3-1][1])
                hsv_ranges.append(max(hsv_values[numBalls*3-3][2], hsv_values[numBalls*3-2][2], hsv_values[numBalls*3-1][2]))
                hsv_ranges[numBalls*3-1] -= min(hsv_values[numBalls*3-3][2], hsv_values[numBalls*3-2][2], hsv_values[numBalls*3-1][2])
                hsv_values2.append([np.uint8(round((np.int(hsv_values[numBalls*3-3][0]) + np.int(hsv_values[numBalls*3-2][0]) + np.int(hsv_values[numBalls*3-1][0]))//3)),
                                               np.uint8(round((np.int(hsv_values[numBalls*3-3][1]) + np.int(hsv_values[numBalls*3-2][1]) + np.int(hsv_values[numBalls*3-1][1]))//3)),
                                               np.uint8(round((np.int(hsv_values[numBalls*3-3][2]) + np.int(hsv_values[numBalls*3-2][2]) + np.int(hsv_values[numBalls*3-1][2]))//3))])
                numClicked = 0
                positions.append([[0, 0]])
                frameNum.append(0)
                xVelocity.append(0)
                yVelocity.append(0)
                xVelocityPrev.append(0)
                yVelocityPrev.append(0)
                isAbove.append(0)

    _, img = cam.read()
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    drawn=img.copy()
    while True:
        if numClicked < 1:
            cpts.clear()
            img = cv2.resize(img, (wid,hgt))

            drawn = img.copy()
            cv2.putText(drawn, "click a ball to begin selection", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0),
                        5)
            cv2.putText(drawn, "or hit space to continue", (10, 90), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0),
                        5)
            cv2.putText(drawn, "balls selected: " + str(numBalls), (10, hgt - 50), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (0, 0, 0), 5)
            cv2.putText(drawn, "click a ball to begin selection", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
            cv2.putText(drawn, "or hit space to continue", (10, 90), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255),
                        2)
            cv2.putText(drawn,"balls selected: "+str(numBalls),(10,hgt-50),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2)
        elif numClicked<2:
            drawn=img.copy()
            cv2.putText(drawn, "click the ball 2 more times", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 5)
            cv2.putText(drawn, "balls selected: " + str(numBalls), (10, hgt - 50), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (0, 0, 0), 5)
            cv2.putText(drawn, "click the ball 2 more times", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
            cv2.putText(drawn, "balls selected: " + str(numBalls), (10, hgt - 50), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255), 2)
            for pt in cpts:
                cv2.rectangle(drawn, (pt[0] - 1, pt[1]-3), (pt[0]+1, pt[1] - 7), (0, 0, 0), 2)
                cv2.rectangle(drawn, (pt[0] - 1, pt[1]+3), (pt[0]+1, pt[1] +7), (0, 0, 0), 2)
                cv2.rectangle(drawn, (pt[0] - 3, pt[1] - 1), (pt[0] -7, pt[1] +1), (0, 0, 0), 2)
                cv2.rectangle(drawn, (pt[0] +3, pt[1] -1), (pt[0] + 7, pt[1]+1), (0, 0, 0), 2)
                cv2.rectangle(drawn, (pt[0] - 1, pt[1]-3), (pt[0]+1, pt[1] - 7), (255, 255, 255), -1)
                cv2.rectangle(drawn, (pt[0] - 1, pt[1]+3), (pt[0]+1, pt[1] +7), (255, 255, 255), -1)
                cv2.rectangle(drawn, (pt[0] - 3, pt[1] - 1), (pt[0] -7, pt[1] +1), (255, 255, 255), -1)
                cv2.rectangle(drawn, (pt[0] +3, pt[1] -1), (pt[0] + 7, pt[1]+1), (255, 255, 255), -1)
        else:
            drawn = img.copy()
            cv2.putText(drawn, "click the ball 1 more time", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 5)
            cv2.putText(drawn, "balls selected: " + str(numBalls), (10, hgt - 50), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (0, 0, 0), 5)
            cv2.putText(drawn, "click the ball 1 more time", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
            cv2.putText(drawn, "balls selected: " + str(numBalls), (10, hgt - 50), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255), 2)
            for pt in cpts:
                cv2.rectangle(drawn, (pt[0] - 1, pt[1] - 3), (pt[0] + 1, pt[1] - 7), (0, 0, 0), 2)
                cv2.rectangle(drawn, (pt[0] - 1, pt[1] + 3), (pt[0] + 1, pt[1] + 7), (0, 0, 0), 2)
                cv2.rectangle(drawn, (pt[0] - 3, pt[1] - 1), (pt[0] - 7, pt[1] + 1), (0, 0, 0), 2)
                cv2.rectangle(drawn, (pt[0] + 3, pt[1] - 1), (pt[0] + 7, pt[1] + 1), (0, 0, 0), 2)
                cv2.rectangle(drawn, (pt[0] - 1, pt[1] - 3), (pt[0] + 1, pt[1] - 7), (255, 255, 255), -1)
                cv2.rectangle(drawn, (pt[0] - 1, pt[1] + 3), (pt[0] + 1, pt[1] + 7), (255, 255, 255), -1)
                cv2.rectangle(drawn, (pt[0] - 3, pt[1] - 1), (pt[0] - 7, pt[1] + 1), (255, 255, 255), -1)
                cv2.rectangle(drawn, (pt[0] + 3, pt[1] - 1), (pt[0] + 7, pt[1] + 1), (255, 255, 255), -1)

        cv2.imshow(prgmName, drawn)
        cv2.setMouseCallback(prgmName, onmouse)
        # img=drawn.copy()


        ch = chr(0xFF & cv2.waitKey(5))
        if ch == 'q':
            return
        elif ch ==' ' and numClicked <1:
            break


    def hueUpper (hue, range):
        if hue<179-range*(3/4)+15:
            return int (hue)+range*(3/4)+15
        else:
            return 179
    def hueLower (hue, range):
        if hue>range*(3/4)-15:
            return int (hue)-range*(3/4)-15
        else:
            return 0
    def satValUpper (satVal, range):
        if satVal<255-range*(3/4)+20:
            return int (satVal)+range*(3/4)+20
        else:
            return 255
    def satValLower (satVal, range):
        if satVal>range*(3/4)-20:
            return int (satVal)-range*(3/4)-2
        else:
            return 0

    frames = []
    ret = True
    _,imgCam=cam.read()
    black=np.zeros((hgt,wid,3),np.uint8)
    cv2.putText(black,"processing...",(10,100),cv2.FONT_HERSHEY_DUPLEX,2.5,(255,255,255),5)
    cv2.imshow(prgmName,black)

    zev=cv2.VideoCapture("loading.mp4")
    fr=0
    while ret:
        fr+=1
        loop,load=zev.read()
        if not loop:
            zev.set(cv2.CAP_PROP_POS_FRAMES,0)
            loop,load=zev.read()
        load=cv2.rotate(load,cv2.ROTATE_90_CLOCKWISE)
        black[200:920,(wid-480)//2:(wid-480)//2+480,:]=load
        prog=fr/int(cam.get(cv2.CAP_PROP_FRAME_COUNT))*(wid-100)+50
        print(fr/int(cam.get(cv2.CAP_PROP_FRAME_COUNT)))
        cv2.rectangle(black,(50,140),(int(prog*1.02),180),(255,255,255),-1)
        cv2.rectangle(black, (50, 140), (wid-50, 180),
                      (255, 255, 255),2)
        cv2.rectangle(black,(wid-50+2,140),(wid,180),(0,0,0),-1)
        cv2.imshow(prgmName,black)
        # print(ret)
        if not ret: break
        # imgCam=cv2.resize(imgCam,(int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))))
        imgCam=cv2.resize(imgCam,(hgt,wid))

        #imgCam = cv2.rotate(imgCam, cv2.ROTATE_90_CLOCKWISE)
        hsv=cv2.cvtColor(imgCam,cv2.COLOR_BGR2HSV)
        img = imgCam
        (height,width,depth) = img.shape
        fakeImage = np.zeros((height, width, depth), np.uint8)
        mask=np.zeros((img.shape[0],img.shape[1],1), np.uint8)

        for values in range(numBalls):
            kernel = np.ones((3, 3), np.uint8)
            # hsv_filtered = cv2.morphologyEx(hsv, cv2.MORPH_OPEN, kernel)
            # hsv_filtered2 = cv2.GaussianBlur(hsv_filtered, (17,17), 0)
            threshold = cv2.inRange(hsv, (hueLower(hsv_values2[values][0], hsv_ranges[3 * values]),
                                          (satValLower(hsv_values2[values][1], hsv_ranges[3 * values + 1])), 30),
                                    (hueUpper(hsv_values2[values][0], hsv_ranges[3 * values]),
                                     (satValUpper(hsv_values2[values][1], hsv_ranges[3 * values + 1])), 225))
            threshold_filtered = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
            existsLine = 0
            contrs, hier = cv2.findContours(threshold_filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contrs) != 0:
                for i in range(len(contrs)):
                    if len(contrs[i]) >= 5:
                        existsLine = 1
                        img3 = img
                        hsv_filtered = cv2.morphologyEx(img3, cv2.MORPH_OPEN, kernel)
                        cv2.drawContours(hsv_filtered, contrs, -1, (150, 10, 255), 3)
                        ellipse = cv2.fitEllipse(contrs[i])
                        # cv2.ellipse(img, ellipse, (0, 255, 0), 2)
                        # cv2.circle(img, (int((int(ellipse[0][1])+int(ellipse[1][1]))/2), int((int(ellipse[0][0])+int(ellipse[1][0]))/2)), 20, (255, 255, 255))
                        # cv2.circle(img, (int(ellipse[0][0]), int(ellipse[0][1])), 20, (255, 255, 255))

                        print(positions)
                        if len(positions[0])>numBalls*2:
                            prev=positions[values][-1]
                            preprev=positions[values][-2]
                            # print(prev,"    ",(int(ellipse[0][0]), int(ellipse[0][1])))
                            positions[values].append([int((ellipse[0][0]+prev[0]+preprev[0])//3), int((ellipse[0][1]+prev[1]+preprev[1])//3)])
                            # print (positions[values])
                        else:
                            positions[values].append([int(ellipse[0][0]), int(ellipse[0][1])])

                        frameNum[values] += 1
                        if frameNum[values] >= 2:
                            # xVelocityPrev[values] = positions[values][frameNum[values]-1][0] - positions[values][frameNum[values]-2][0]
                            # xVelocity[values] = positions[values][frameNum[values]][0] - positions[values][frameNum[values] - 1][0]
                            # yVelocityPrev[values] = positions[values][frameNum[values] - 1][1] - positions[values][frameNum[values] - 2][1]
                            # yVelocity[values] = positions[values][frameNum[values]][1] - positions[values][frameNum[values] - 1][1]
                            # totalVelocityPrev = math.sqrt(xVelocityPrev[values]*xVelocityPrev[values] + yVelocityPrev[values]*yVelocityPrev[values])
                            # totalVelocity = math.sqrt(xVelocity[values] * xVelocity[values] + yVelocity[values] * yVelocity[values])
                            (height, width, depth) = img.shape
                            nonImage = np.zeros((height, width, depth), np.uint8)
                            # # print (xVelocity[values])
                            # if yVelocity[values] < 0 and yVelocityPrev[values] > 0:
                            # print (isAbove[values])
                            if (positions[values][frameNum[values]][1]>yHeight and isAbove[values] == 1):
                                isAbove[values] = 0
                            if (positions[values][frameNum[values]][1]<yHeight and isAbove[values] == 0):
                                numThrown+=1
                                isAbove[values] = 1
                                print (numThrown)
                            for j in range(2, frameNum[values]):
                                lineColor = np.uint8(
                                    [[[hsv_values2[values][0], hsv_values2[values][1], hsv_values2[values][2]]]])
                                #
                                # print(cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)[0][0][0])
                                bgrColor = cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)
                                actualbgr = bgrColor[0][0]
                                aaa = tuple([int(x) for x in actualbgr])
                                cv2.line(nonImage, (positions[values][j - 1][0], positions[values][j - 1][1]),
                                         (positions[values][j][0], positions[values][j][1]),
                                        aaa , thickness=5)
                            fakeImage = cv2.addWeighted(fakeImage, 1, nonImage, 1/3, 0)
                        break
            if existsLine == 0:
                if frameNum[values] >= 2:
                    (height, width, depth) = img.shape
                    nonImage = np.zeros((height, width, depth), np.uint8)
                    for j in range(2, frameNum[values]):
                        lineColor = np.uint8(
                            [[[hsv_values2[values][0], hsv_values2[values][1], hsv_values2[values][2]]]])
                        #
                        # print(cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)[0][0][0])
                        bgrColor = cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)
                        actualbgr = bgrColor[0][0]
                        aaa = tuple([int(x) for x in actualbgr])
                        cv2.line(nonImage, (positions[values][j - 1][0], positions[values][j - 1][1]),
                                 (positions[values][j][0], positions[values][j][1]),
                                 aaa, thickness=5)
                    fakeImage = cv2.addWeighted(fakeImage, 1, nonImage, 1 / 3, 0)
        img = cv2.addWeighted(fakeImage, 0.9, imgCam, 0.1, 100)
                    # else:
                    #     # optional to "delete" the small contours
                    #     cv2.drawContours(img, contrs, -1,  (0, 0, 0), -1)1
        #     cv2.drawContours(img, contrs, -1, (0, 255, 0), 3)
        #     mask=cv2.bitwise_or(mask,threshold)
        #
        # maskedimg=cv2.bitwise_and(img,img,mask=mask)

        ret, imgCam = cam.read()

        frames.append(img)
        ch = chr(0xFF & cv2.waitKey(1))
        if ch == 'q':
            return


    def ontrack(val):
        global i
        global play
        play=False
        i=val

    def speedchange(val):
        global speed
        speed=val+20

    # frames[0]=frames[1].copy()

    cv2.createTrackbar("Frame: ",prgmName,0,len(frames)-2,ontrack)
    cv2.createTrackbar("Speed: ", prgmName, 45, 57, speedchange)
    while True:
        frame = cv2.rotate(frames[i], cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.resize(frame, (wid,hgt))

        cv2.imshow(prgmName,frame)
        if play and i<len(frames)-1:
            cv2.setTrackbarPos("Frame: ",prgmName,i)
            play=True
            i+=1
        ch = chr(0xFF & cv2.waitKey(80-speed))
        if ch == 'q':
            cv2.destroyWindow(prgmName);
            return
        if ch==" ":
            play=not play


    #RGB code:	R: 175 G: 15 B: 17
    # HSV:	359.25° 91.43% 68.63%
