import cv2
import numpy as np


cam = cv2.VideoCapture(0)



global img

numBalls = 0

hsv_values = []

def onmouse(event, x, y, flags, param):
    global numBalls

    if event == cv2.EVENT_LBUTTONDOWN:
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        (h,s,v) = cv2.split(img2)
        print(h[y][x])
        # print(countSelected)
        hsv_values.append((h[y][x],s[y][x],v[y][x]))
        print (hsv_values)
        numBalls+=1


while True:
    __,img = cam.read()
    img = cv2.resize(img,(1000, 563))
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
    if hue<164:
        return int (hue)+15
    else:
        return 179
def hueLower (hue):
    if hue>15:
        return int (hue)-15
    else:
        return 0
def satValUpper (satVal):
    if satVal<225:
        return int (satVal)+30
    else:
        return 255
def satValLower (satVal):
    if satVal>30:
        return int (satVal)-30
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
        print(values[0])
        threshold = cv2.inRange(hsv, (hueLower(values[0]), (satValLower(values[1])), 0), (hueUpper(values[0]),(satValUpper(values[1])), 255))


        mask=cv2.bitwise_or(mask,threshold)

    maskedimg=cv2.bitwise_and(img,img,mask=mask)

    cv2.imshow("wow", maskedimg)
    ch = chr(0xFF & cv2.waitKey(1))
    if ch == 'q':
        break



#RGB code:	R: 175 G: 15 B: 17
# HSV:	359.25° 91.43% 68.63%
