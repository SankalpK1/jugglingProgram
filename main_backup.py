import cv2
import numpy as np
from random import randint
import colorsys
# from colorCopy import main as color

def empty():
    print("coming soon")



def drawButtons(number,margin):
    global titlefeed
    global mouseX
    global mouseY

    height=int((hgt-250-margin*(number+1))/number)
    top=250+margin
    temp=titlefeed.copy()
    for i in range(number):
        blur = titlefeed[top: top+height, margin:wid-margin, :]
        blur = cv2.blur(blur, (75,75) )
        titlefeed[top: top + height, margin:wid - margin, :] = blur
        pt1=(margin, top)
        pt2=(wid - margin, top+height)
        (b,g,r)=modes[i][1]
        if mouseX<=pt2[0] and mouseX>=pt1[0] and mouseY<=pt2[1] and mouseY>=pt1[1]:
            b-=100 #190
            g-=100
            r-=100
        if b<0: b=0
        elif g < 0: g = 0
        elif r < 0: r = 0
        cv2.rectangle(temp, pt1,pt2, (b,g,r) if mouseX<=pt2[0] and mouseX>=pt1[0] and mouseY<=pt2[1] and mouseY>=pt1[1] else (255, 255, 255), -1)

        top+=height+margin

    titlefeed=cv2.addWeighted(temp,.7,titlefeed,.3,0)

    top = 250 + margin
    for i in range(number):
        pt1=(margin, top)
        pt2=(wid - margin, top+height)
        top+=height+margin
        (b,g,r)=(255,255,255)
        font = cv2.FONT_HERSHEY_DUPLEX
        size,_ = cv2.getTextSize(modes[i][0], font, 2, 4)
        cv2.putText(titlefeed,modes[i][0],(wid//2-size[0]//2,top-margin-height//2+size[1]//2),font,2,(b,g,r) if mouseX<=pt2[0] and mouseX>=pt1[0] and mouseY<=pt2[1] and mouseY>=pt1[1] else modes[i][1],4)
        if mouseX<=pt2[0] and mouseX>=pt1[0] and mouseY<=pt2[1] and mouseY>=pt1[1]:
            frameCol=modes[i][1]
        else: frameCol=(0,0,0)
        cv2.rectangle(titlefeed, pt1,pt2, frameCol, 3)

def drawTitle():
    global titlefeed
    global hue
    blur = titlefeed[0: 250, :, :]
    blur = cv2.blur(blur, (75, 75) )
    titlefeed[0: 250, :, :] = blur

    mask = np.ones((hgt, wid, 3), np.uint8) * 255
    cv2.putText(mask, "Choose", (86, 100), titlefont, 3, (0, 0, 0), 5)
    cv2.putText(mask, "a mode!", (63, 200), titlefont, 3, (0, 0, 0), 5)
    _, dimmed = cv2.threshold(titlefeed, 254, 100, cv2.THRESH_TRUNC)
    text = cv2.subtract(dimmed, mask)
    text = cv2.bitwise_not(text)
    _, text = cv2.threshold(text, 254, 100, cv2.THRESH_TOZERO_INV)
    hue += .05
    if hue >= 1: hue = 0
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

    white=titlefeed.copy()
    cv2.rectangle(white,(0,0),(wid,250),(255,255,255),-1)
    titlefeed =cv2.addWeighted(white, .7, titlefeed, .3, 0)

    cv2.putText(titlefeed, "Choose", (86, 100), titlefont, 3, (b * 255, g * 255, r * 255), 11)
    cv2.putText(titlefeed, "a mode!", (63, 200), titlefont, 3, (b * 255, g * 255, r * 255), 11)
    cv2.putText(titlefeed, "Choose", (86, 100), titlefont, 3, (0, 0, 0), 5)
    cv2.putText(titlefeed, "a mode!", (63, 200), titlefont, 3, (0, 0, 0), 5)
    titlefeed = cv2.add(titlefeed, text)

    cv2.line(titlefeed, (-10, 250), (wid + 10, 250), (0, 0, 0), 3)

def processClick(number,margin):
    global clickupX
    global clickupY
    X=clickupX
    Y=clickupY
    clickupX=0
    clickupY=0
    height = int((hgt - 250 - margin * (number + 1)) / number)
    top = 250 + margin
    for i in range(number):
        pt1=(margin, top)
        pt2=(wid - margin, top+height)
        top += height + margin
        if X <= pt2[0] and X >= pt1[0] and Y <= pt2[1] and Y >= pt1[1]: return i
    return -1

def mouse(event, x, y, flags, param):
    global mouseX
    global mouseY
    global clickupX
    global clickupY
    if (event == cv2.EVENT_MOUSEMOVE):
        mouseX=x
        mouseY=y
    if (event==cv2.EVENT_LBUTTONDOWN):
        clickupX=x
        clickupY=y
clickupX=0
clickupY=0
mouseX=0
mouseY=0

# color()

cam = cv2.VideoCapture(0)
hgt=950
wid=int(9/16*hgt)
titlefont = cv2.FONT_HERSHEY_DUPLEX
hue=0
_, titlefeed = cam.read()
modes=[("practice",(0,0,255)),("training",(0,220,0)),("points",(255,0,0))] # name,bgr,method
prgmName="Juggle _________"
cv2.imshow(prgmName, titlefeed)
cv2.setMouseCallback(prgmName,mouse)



while True:

    _, titlefeed = cam.read()
    titlefeed = cv2.resize(titlefeed, (hgt, wid))
    titlefeed = cv2.rotate(titlefeed, cv2.ROTATE_90_CLOCKWISE)

    drawTitle()

    numModes=len(modes)
    margin=50

    drawButtons(numModes,margin)

    prgm= processClick(numModes,margin)
    if prgm>=0:print("ran ",modes[prgm][0])



    cv2.imshow(prgmName, titlefeed)



    ch = chr(0xFF & cv2.waitKey(5))
    if ch == 'q' :
        break

def prgmName():
    return prgmName