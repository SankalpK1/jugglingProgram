import cv2
import numpy as np
import math
import colorsys
import socket
from window_info import *

cam = cv2.VideoCapture(0)

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

numThrown = 0
cpts=[]
sock1 = socket.socket()
host = 'localhost'
port1 = 2343
sock1.connect((host, port1))
sock2 = socket.socket()
port2 = 2344
sock2.connect((host, port2))

def main(live):
    cam = cv2.VideoCapture(0)

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
    global cpts

    global yVelocity

    global xVelocityPrev

    global yVelocityPrev

    global numThrown

    cam = cv2.VideoCapture(0)

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

    numThrown = 0
    def onmouse(event, x, y, flags, param):
        global numBalls
        global numClicked
        global cpts
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


    _, drawn = cam.read()
    drawn = cv2.resize(drawn, (hgt, wid))
    drawn = cv2.rotate(drawn, cv2.ROTATE_90_CLOCKWISE)
    while True:
        if numClicked < 1:
            cpts.clear()
            __,img = cam.read()

            img = cv2.resize(img, (hgt,wid))
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
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
        else:
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

    while True:
        _,imgCam=cam.read()
        imgCam=cv2.resize(imgCam,(hgt,wid))
        imgCam=cv2.rotate(imgCam, cv2.ROTATE_90_CLOCKWISE)
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
                                          (satValLower(hsv_values2[values][1], hsv_ranges[3 * values + 1])), 50),
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
                        positions[values].append([int(ellipse[0][0]), int(ellipse[0][1])])
                        frameNum[values] += 1
                        if frameNum[values] >= 2:
                            xVelocityPrev[values] = positions[values][frameNum[values]-1][0] - positions[values][frameNum[values]-2][0]
                            xVelocity[values] = positions[values][frameNum[values]][0] - positions[values][frameNum[values] - 1][0]
                            yVelocityPrev[values] = positions[values][frameNum[values] - 1][1] - positions[values][frameNum[values] - 2][1]
                            yVelocity[values] = positions[values][frameNum[values]][1] - positions[values][frameNum[values] - 1][1]
                            totalVelocityPrev = math.sqrt(xVelocityPrev[values]*xVelocityPrev[values] + yVelocityPrev[values]*yVelocityPrev[values])
                            totalVelocity = math.sqrt(xVelocity[values] * xVelocity[values] + yVelocity[values] * yVelocity[values])
                            velocityAngle = math.atan2(float(yVelocity[values]), float(xVelocity[values]))
                            if (positions[values][frameNum[values]][0]>int(wid/2) and (frameNum[values] + (values+1)*20)%(20*values) == 0):
                                sock1.sendall((str(positions[values][frameNum[values]][1] + 200 * values) + ' ' + (str(totalVelocity/10) + ';')).encode())
                            elif (positions[values][frameNum[values]][0]<int(wid/2) and (frameNum[values] + (values+1)*20)%(20*values) == 0):
                                sock2.sendall((str(positions[values][frameNum[values]][1] + 200 * values) + ' ' + (str(totalVelocity/10) + ';')).encode())
                            # (height, width, depth) = img.shape
                            # nonImage = np.zeros((height, width, depth), np.uint8)
                            # # print (xVelocity[values])
                            # if yVelocity[values] < 0 and yVelocityPrev[values] > 0:
                            # print (isAbove[values])
                        #     if (positions[values][frameNum[values]][1]>yHeight and isAbove[values] == 1):
                        #         isAbove[values] = 0
                        #     if (positions[values][frameNum[values]][1]<yHeight and isAbove[values] == 0):
                        #         numThrown+=1
                        #         isAbove[values] = 1
                        #         print (numThrown)
                        #     for j in range(2, frameNum[values]):
                        #         lineColor = np.uint8(
                        #             [[[hsv_values2[values][0], hsv_values2[values][1], hsv_values2[values][2]]]])
                        #         #
                        #         # print(cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)[0][0][0])
                        #         bgrColor = cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)
                        #         actualbgr = bgrColor[0][0]
                        #         aaa = tuple([int(x) for x in actualbgr])
                        #         cv2.line(nonImage, (positions[values][j - 1][0], positions[values][j - 1][1]),
                        #                  (positions[values][j][0], positions[values][j][1]),
                        #                 aaa , thickness=5)
                        #     fakeImage = cv2.addWeighted(fakeImage, 1, nonImage, 1/3, 0)
                        # break
            # if existsLine == 0:
            #     if frameNum[values] >= 2:
            #         (height, width, depth) = img.shape
            #         nonImage = np.zeros((height, width, depth), np.uint8)
            #         for j in range(2, frameNum[values]):
            #             lineColor = np.uint8(
            #                 [[[hsv_values2[values][0], hsv_values2[values][1], hsv_values2[values][2]]]])
            #             #
            #             # print(cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)[0][0][0])
            #             bgrColor = cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)
            #             actualbgr = bgrColor[0][0]
            #             aaa = tuple([int(x) for x in actualbgr])
            #             cv2.line(nonImage, (positions[values][j - 1][0], positions[values][j - 1][1]),
            #                      (positions[values][j][0], positions[values][j][1]),
            #                      aaa, thickness=5)
            #         fakeImage = cv2.addWeighted(fakeImage, 1, nonImage, 1 / 3, 0)
        # img = cv2.addWeighted(fakeImage, 0.9, imgCam, 0.1, 100)
                    # else:
                    #     # optional to "delete" the small contours
                    #     cv2.drawContours(img, contrs, -1,  (0, 0, 0), -1)1
        #     cv2.drawContours(img, contrs, -1, (0, 255, 0), 3)
        #     mask=cv2.bitwise_or(mask,threshold)
        #
        # maskedimg=cv2.bitwise_and(img,img,mask=mask)

        cv2.imshow(prgmName, img)
        ch = chr(0xFF & cv2.waitKey(1))
        if ch == 'q':
            sock1.sendall('00;'.encode())
            sock2.sendall('00;'.encode())
            break



    #RGB code:	R: 175 G: 15 B: 17
    # HSV:	359.25° 91.43% 68.63%