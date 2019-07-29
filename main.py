import cv2
import numpy as np
from random import randint
import colorsys
from ColoredLines import main as Lines
from musicMode import main as music
from competitiveMode import main as comp
from window_info import *
import math
from BackEndMode import main as back


def empty(live):
    print("coming soon")


def drawButtons(number, margin):
    global modes
    global titlefeed
    global mouseX
    global mouseY

    height = int((hgt - 350 - margin * (number + 1)) / number)
    top = 350 + margin
    temp = titlefeed.copy()
    if (live):
        modes = [("practice", (0, 0, 255), Lines), ("competitive", (0, 210, 0), comp),
         ("back end", (255, 0, 0), back)]
    elif (not live):
        modes = [("lines", (0, 0, 255), Lines), ("identifier", (0, 210, 0), empty),
                 ("musical", (255, 0, 0), music)]
    for i in range(number):
        blur = titlefeed[top: top + height, margin:wid - margin, :]
        blur = cv2.blur(blur, (75, 75))
        titlefeed[top: top + height, margin:wid - margin, :] = blur
        pt1 = (margin, top)
        pt2 = (wid - margin, top + height)
        (b, g, r) = modes[i][1]
        if mouseX <= pt2[0] and mouseX >= pt1[0] and mouseY <= pt2[1] and mouseY >= pt1[1]:
            b -= 100  # 190
            g -= 100
            r -= 100
        if b < 0:
            b = 0
        elif g < 0:
            g = 0
        elif r < 0:
            r = 0
        cv2.rectangle(temp, pt1, pt2,
                      (b, g, r) if mouseX <= pt2[0] and mouseX >= pt1[0] and mouseY <= pt2[1] and mouseY >= pt1[
                          1] else (255, 255, 255), -1)

        top += height + margin

    titlefeed = cv2.addWeighted(temp, .7, titlefeed, .3, 0)

    top = 350 + margin
    for i in range(number):
        pt1 = (margin, top)
        pt2 = (wid - margin, top + height)
        top += height + margin
        (b, g, r) = (255, 255, 255)
        font = cv2.FONT_HERSHEY_DUPLEX
        size, _ = cv2.getTextSize(modes[i][0], font, 2, 4)
        cv2.putText(titlefeed, modes[i][0],
                    (wid // 2 - size[0] // 2, top - margin - height // 2 + size[1] // 2), font, 2,
                    (b, g, r) if mouseX <= pt2[0] and mouseX >= pt1[0] and mouseY <= pt2[1] and mouseY >= pt1[1] else
                    modes[i][1], 4)
        if mouseX <= pt2[0] and mouseX >= pt1[0] and mouseY <= pt2[1] and mouseY >= pt1[1]:
            frameCol = modes[i][1]
        else:
            frameCol = (0, 0, 0)
        cv2.rectangle(titlefeed, pt1, pt2, frameCol, 3)


def drawTitle():
    global titlefeed
    global hue
    blur = titlefeed[0: 250, :, :]
    blur = cv2.blur(blur, (75, 75))
    titlefeed[0: 250, :, :] = blur

    mask = np.ones((hgt, wid, 3), np.uint8) * 255
    cv2.putText(mask, "Choose", (86, 100), titlefont, 3, (0, 0, 0), 5)
    cv2.putText(mask, "a mode!", (63, 200), titlefont, 3, (0, 0, 0), 5)
    _, dimmed = cv2.threshold(titlefeed, 254, 100, cv2.THRESH_TRUNC)
    text = cv2.subtract(dimmed, mask)
    text = cv2.bitwise_not(text)
    _, text = cv2.threshold(text, 254, 100, cv2.THRESH_TOZERO_INV)

    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

    white = titlefeed.copy()
    cv2.rectangle(white, (0, 0), (wid, 250), (255, 255, 255), -1)
    titlefeed = cv2.addWeighted(white, .7, titlefeed, .3, 0)

    cv2.putText(titlefeed, "Choose", (86, 100), titlefont, 3, (b * 255, g * 255, r * 255), 11)
    cv2.putText(titlefeed, "a mode!", (63, 200), titlefont, 3, (b * 255, g * 255, r * 255), 11)
    cv2.putText(titlefeed, "Choose", (86, 100), titlefont, 3, (0, 0, 0), 5)
    cv2.putText(titlefeed, "a mode!", (63, 200), titlefont, 3, (0, 0, 0), 5)
    titlefeed = cv2.add(titlefeed, text)

    cv2.line(titlefeed, (-10, 250), (wid + 10, 250), (0, 0, 0), 3)


def processClick(number, margin):
    global live
    global clickupX
    global clickupY
    X = clickupX
    Y = clickupY
    clickupX = 0
    clickupY = 0
    height = int((hgt - 350 - margin * (number + 1)) / number)
    top = 350 + margin
    for i in range(number):
        pt1 = (margin, top)
        pt2 = (wid - margin, top + height)
        top += height + margin
        if X <= pt2[0] and X >= pt1[0] and Y <= pt2[1] and Y >= pt1[1]: return i

    if math.sqrt(pow(X - wid / 2 + 50, 2) + pow(Y - 325, 2)) < 25 or math.sqrt(
            pow(X - wid / 2 - 50, 2) + pow(Y - 325, 2)) < 25 or (
            X > wid / 2 - 50 and X < wid / 2 + 50 and Y < 350 and Y > 300):
        live = not live

    return -1


def mouse(event, x, y, flags, param):
    global mouseX
    global mouseY
    global clickupX
    global clickupY
    if (event == cv2.EVENT_MOUSEMOVE):
        mouseX = x
        mouseY = y
    if (event == cv2.EVENT_LBUTTONDOWN):
        clickupX = x
        clickupY = y


def drawSwitch():
    global titlefeed
    mid = wid // 2

    blurred = cv2.blur(titlefeed, (75, 75))
    mask = np.zeros((hgt, wid, 3), dtype=np.uint8)
    cv2.rectangle(mask, (mid - 50, 300), (mid + 50, 350), (255, 255, 255), -1)
    cv2.circle(mask, (mid - 50, 325), 25, (255, 255, 255), -1)
    cv2.circle(mask, (mid + 50, 325), 25, (255, 255, 255), -1)
    mask = cv2.bitwise_and(mask, blurred)
    cv2.rectangle(titlefeed, (mid - 50, 300), (mid + 50, 350), (0, 0, 0), -1)
    cv2.circle(titlefeed, (mid - 50, 325), 25, (0, 0, 0), -1)
    cv2.circle(titlefeed, (mid + 50, 325), 25, (0, 0, 0), -1)
    titlefeed = mask + titlefeed

    temp = titlefeed.copy()
    cv2.rectangle(titlefeed, (mid - 50, 300), (mid + 50, 350), (255, 255, 255), -1)
    cv2.circle(titlefeed, (mid - 50, 325), 25, (255, 255, 255), -1)
    cv2.circle(titlefeed, (mid + 50, 325), 25, (255, 255, 255), -1)
    titlefeed = cv2.addWeighted(temp, .3, titlefeed, .7, 0)

    cv2.line(titlefeed, (mid - 50, 300), (mid + 50, 300), (0, 0, 0), 3)
    cv2.line(titlefeed, (mid - 50, 350), (mid + 50, 350), (0, 0, 0), 3)
    cv2.ellipse(titlefeed, (mid - 50, 325), (25, 25), 0, 90, 270, (0, 0, 0), 3)
    cv2.ellipse(titlefeed, (mid + 50, 325), (25, 25), 0, 270, 450, (0, 0, 0), 3)
    cv2.circle(titlefeed, (mid - (50 if live else -50), 325), 30, (255, 255, 255), -1)
    cv2.circle(titlefeed, (mid - (50 if live else -50), 325), 30, (0, 0, 0), 3)

    font = cv2.FONT_HERSHEY_DUPLEX
    size, _ = cv2.getTextSize("real time", font, .7, 2)
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    cv2.putText(titlefeed, "real time", (wid // 2 - 75 - size[0] - 40, 325 + size[1] // 2), font, .7,
                (b * 255, g * 255, r * 255) if live else (0, 0, 0), 4)
    cv2.putText(titlefeed, "real time", (wid // 2 - 75 - size[0] - 40, 325 + size[1] // 2), font, .7, (255, 255, 255),
                1)
    cv2.putText(titlefeed, "recorded", (wid // 2 + 75 + 40, 325 + size[1] // 2), font, .7,
                (0, 0, 0) if live else (b * 255, g * 255, r * 255), 4)
    cv2.putText(titlefeed, "recorded", (wid // 2 + 75 + 40, 325 + size[1] // 2), font, .7, (255, 255, 255), 1)


live = True
clickupX = 0
clickupY = 0
mouseX = 0
mouseY = 0
cam = cv2.VideoCapture(0)

titlefont = cv2.FONT_HERSHEY_DUPLEX
hue = 0
_, titlefeed = cam.read()
modes = [("practice", (0, 0, 255), Lines), ("competitive", (0, 210, 0), comp),
         ("back end", (255, 0, 0), empty)]  # name,bgr,method

cv2.imshow(prgmName, titlefeed)
cv2.setMouseCallback(prgmName, mouse)

while True:
    _, titlefeed = cam.read()
    titlefeed = cv2.resize(titlefeed, (hgt, wid))
    titlefeed = cv2.rotate(titlefeed, cv2.ROTATE_90_CLOCKWISE)

    hue += .05
    if hue >= 1: hue = 0

    drawTitle()

    numModes = len(modes)
    margin = 50

    drawButtons(numModes, margin)

    drawSwitch()

    prgm = processClick(numModes, margin)
    if prgm >= 0:
        print("ran ", modes[prgm][0])
        modes[prgm][2](live)
        cv2.imshow(prgmName,titlefeed)
        cv2.setMouseCallback(prgmName, mouse)

    cv2.imshow(prgmName, titlefeed)

    ch = chr(0xFF & cv2.waitKey(5))
    if ch == 'q':
        break
