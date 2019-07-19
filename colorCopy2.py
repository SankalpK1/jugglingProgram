import cv2
import numpy as np


cam = cv2.VideoCapture(0)

global img

numClicked = 0

numBalls = 0

hsv_values = []

hsv_values2 = []

hsv_ranges = []

def onmouse(event, x, y, flags, param):
    global numBalls
    global numClicked
    if event == cv2.EVENT_LBUTTONDOWN:
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        (h,s,v) = cv2.split(img2)
        print(h[y][x])
        # print(countSelected)
        hsv_values.append([h[y][x],s[y][x],v[y][x]])
        numClicked+=1
        if numClicked == 3:
            numBalls+=1
            numClicked = 0


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
    elif ch==' ':
        break


def hueUpper (hue):
    if hue<179-15:
        return int (hue)+15
    else:
        return 179
def hueLower (hue):
    if hue>15:
        return int (hue)-15
    else:
        return 0
def satValUpper (satVal):
    if satVal<255-20:
        return int (satVal)+20
    else:
        return 255
def satValLower (satVal):
    if satVal>20:
        return int (satVal)-20
    else:
        return 0

while True:
    _,img=cam.read()
    img=cv2.resize(img,(1000,563))
    img=cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # threshold = cv2.inRange(hsv, (101, 129, 22), (115, 255, 255))
    mask=np.zeros((img.shape[0],img.shape[1],1), np.uint8)

    for values in hsv_values:
        kernel = np.ones((7, 7), np.uint8)
        hsv_filtered = cv2.morphologyEx(hsv, cv2.MORPH_OPEN, kernel)
        hsv_filtered2 = cv2.blur(hsv_filtered, (15,15))
        threshold = cv2.inRange(hsv, (hueLower(values[0]), (satValLower(values[1])), 0),
                                (hueUpper(values[0]), (satValUpper(values[1])), 255))


        mask=cv2.bitwise_or(mask,threshold)

    maskedimg=cv2.bitwise_and(img,img,mask=mask)

    cv2.imshow("wow", maskedimg)
    ch = chr(0xFF & cv2.waitKey(1))
    if ch == 'q':
        break



#RGB code:	R: 175 G: 15 B: 17
# HSV:	359.25° 91.43% 68.63%