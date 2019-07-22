import cv2
import numpy as np
import math
import colorsys


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

def onmouse(event, x, y, flags, param):
    global numBalls
    global numClicked
    if event == cv2.EVENT_LBUTTONDOWN:
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


while True:
    if numClicked < 1:
        __,img = cam.read()
        img = cv2.resize(img, (1000, 563))
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow('juggling', img)
    cv2.setMouseCallback('juggling', onmouse)
    cv2.waitKey(10)
    ch = chr(0xFF & cv2.waitKey(5))
    if ch == 'q':
        exit(0)
    elif ch ==' ':
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
    _,img=cam.read()
    img=cv2.resize(img,(1000,563))
    img=cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # threshold = cv2.inRange(hsv, (101, 129, 22), (115, 255, 255))
    mask=np.zeros((img.shape[0],img.shape[1],1), np.uint8)

    for values in range(numBalls):
        kernel = np.ones((3, 3), np.uint8)
        # hsv_filtered = cv2.morphologyEx(hsv, cv2.MORPH_OPEN, kernel)
        # hsv_filtered2 = cv2.GaussianBlur(hsv_filtered, (17,17), 0)
        threshold = cv2.inRange(hsv, (hueLower(hsv_values2[values][0], hsv_ranges[3*values]),
                                                (satValLower(hsv_values2[values][1], hsv_ranges[3*values+1])), 0),
                                                (hueUpper(hsv_values2[values][0], hsv_ranges[3*values]),(satValUpper(hsv_values2[values][1],  hsv_ranges[3*values+1])), 255))
        threshold_filtered = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
        existsLine = 0
        contrs, hier = cv2.findContours(threshold_filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contrs) != 0:
            for i in range(len(contrs)):
                if len(contrs[i]) >= 15:
                    existsLine = 1
                    cv2.drawContours(img, contrs, -1, (150, 10, 255), 3)
                    ellipse = cv2.fitEllipse(contrs[i])
                    cv2.ellipse(img, ellipse, (0, 255, 0), 2)
                    # cv2.circle(img, (int((int(ellipse[0][1])+int(ellipse[1][1]))/2), int((int(ellipse[0][0])+int(ellipse[1][0]))/2)), 20, (255, 255, 255))
                    # cv2.circle(img, (int(ellipse[0][0]), int(ellipse[0][1])), 20, (255, 255, 255))
                    positions[values].append([int(ellipse[0][0]), int(ellipse[0][1])])
                    frameNum[values] += 1
                    if frameNum[values] >= 2:
                        for j in range(2, frameNum[values]):
                            lineColor = np.uint8(
                                [[[hsv_values2[values][0], hsv_values2[values][1], hsv_values2[values][2]]]])
                            #
                            # print(cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)[0][0][0])
                            bgrColor = cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)
                            actualbgr = bgrColor[0][0]
                            aaa = tuple([int(x) for x in actualbgr])
                            cv2.line(img, (positions[values][j - 1][0], positions[values][j - 1][1]),
                                     (positions[values][j][0], positions[values][j][1]),
                                    aaa , thickness=5)
                    break
        if existsLine == 0:
            if frameNum[values] >= 2:
                for j in range(2, frameNum[values]):
                    lineColor = np.uint8(
                        [[[hsv_values2[values][0], hsv_values2[values][1], hsv_values2[values][2]]]])
                    #
                    # print(cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)[0][0][0])
                    bgrColor = cv2.cvtColor(lineColor, cv2.COLOR_HSV2BGR)
                    actualbgr = bgrColor[0][0]
                    aaa = tuple([int(x) for x in actualbgr])
                    cv2.line(img, (positions[values][j - 1][0], positions[values][j - 1][1]),
                             (positions[values][j][0], positions[values][j][1]),
                             aaa, thickness=5)

                # else:
                #     # optional to "delete" the small contours
                #     cv2.drawContours(img, contrs, -1,  (0, 0, 0), -1)1
        # cv2.drawContours(img, contrs, -1, (0, 255, 0), 3)
        # mask=cv2.bitwise_or(mask,threshold)

    maskedimg=cv2.bitwise_and(img,img,mask=mask)

    cv2.imshow("wow", img)
    ch = chr(0xFF & cv2.waitKey(1))
    if ch == 'q':
        break



#RGB code:	R: 175 G: 15 B: 17
# HSV:	359.25° 91.43% 68.63%
