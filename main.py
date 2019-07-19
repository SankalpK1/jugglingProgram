import cv2
import numpy as np
from random import randint
import colorsys

def drawButtons(number,height,margin):
    global titlefeed
    top=250+margin
    temp=titlefeed.copy()
    for _ in range(number):
        blur = titlefeed[top: top+height, margin:wid-margin, :]
        blur = cv2.blur(blur, (69, 69), )
        titlefeed[top: top + height, margin:wid - margin, :] = blur
        cv2.rectangle(temp, (margin, top), (wid - margin, top+height), (255, 255, 255), -1)
        cv2.rectangle(temp, (margin, top), (wid - margin, top + height), (0, 0, 0), 3)
        top+=height+margin
    titlefeed=cv2.addWeighted(temp,.7,titlefeed,.3,0)

cam = cv2.VideoCapture(0)
hgt=950
wid=int(9/16*hgt)
titlefont = cv2.FONT_HERSHEY_DUPLEX
hue=0

_, titlefeed = cam.read()

while True:
    _, titlefeed = cam.read()
    titlefeed = cv2.resize(titlefeed, (hgt, wid))
    titlefeed = cv2.rotate(titlefeed, cv2.ROTATE_90_CLOCKWISE)

    blur = titlefeed[0: 250,: ,:]
    blur=cv2.blur(blur,(100,100),)
    titlefeed[0: 250, :, :]=blur

    mask=np.ones((hgt,wid,3),np.uint8)*255
    cv2.putText(mask, "Choose", (86, 100), titlefont, 3, (0,0,0), 5)
    cv2.putText(mask, "a mode!", (63, 200), titlefont, 3, (0,0,0), 5)
    _,dimmed=cv2.threshold(titlefeed,254,100,cv2.THRESH_TRUNC)
    text=cv2.subtract(dimmed,mask)
    text=cv2.bitwise_not(text)
    _,text=cv2.threshold(text,254,100,cv2.THRESH_TOZERO_INV)
    hue+=.05
    if hue>=1:hue=0
    r,g,b=colorsys.hsv_to_rgb(hue,1,1)
    cv2.putText(titlefeed, "Choose", (86,100), titlefont, 3, (b*255,g*255,r*255), 11)
    cv2.putText(titlefeed, "a mode!", (63, 200), titlefont, 3, (b*255,g*255,r*255), 11)
    cv2.putText(titlefeed, "Choose", (86,100), titlefont, 3, (0,0,0), 5)
    cv2.putText(titlefeed, "a mode!", (63, 200), titlefont, 3, (0,0,0), 5)
    titlefeed=cv2.add(titlefeed,text)

    cv2.line(titlefeed,(-10,250),(wid+10,250),(255,255,255),5)

    drawButtons(3,200,50)

    cv2.imshow("Juggle _________", titlefeed)

    ch = chr(0xFF & cv2.waitKey(5))
    if ch == 'q':
        break

