import numpy as np
import cv2
import time
from utils import handleTensorflowSession
from drawingutils import drawBallsAndHands
from keras.models import load_model
from gridmodel import GridModel
from frameratechecker import FramerateChecker
import multiprocessing
#import Tkinter as Tk
import time
from window_info import *
def patterndetect(theParameter):
    handleTensorflowSession(memoryLimit=0.2)
    trickDetected = 0
    gridModel = GridModel("grid_model_submovavg_64x64.h5")
    patternModel = load_model("3b_pattern_model.h5")
    #cap = theParameter.read()   # todo
    trickAvgstore = [0, 0, 0, 0 , 0 , 0 , 0 , 0 , 0 , 0, 0 , 0]
    history = []
    start = time.time()
    PERIOD_OF_TIME = 18
    font = cv2.FONT_HERSHEY_SIMPLEX
    framerateChecker = FramerateChecker(expected_fps=30)
    names = ["441", "box", "cascade", "42, left hand", "shower, left hand", "mill's mess", "one up two up",
             "42, right hand", "reverse cascade", "shower, right hand", "takeouts", "tennis"]
    img3 = np.zeros((512, 1920, 3), dtype=np.uint8)
    cv2.putText(img3, "The AI model will analyze you juggling for 15 seconds and then attempt to determine what trick you performed. ", (10, 40), font, 1.05, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(img3,
                "NOTE: only perform ONE trick, otherwise the AI model won't produce the desired result.",
                (400, 100), font, .8, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img3,
                "Press 's' to start",
                (800, 200), font, .7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow(prgmName, img3)
    cv2.moveWindow(prgmName, 0, 0)
    while (True):
        ch = chr(0xFF & cv2.waitKey(0))
        if ch == 's':
            break
    cv2.destroyAllWindows()
    start = time.time()
    PERIOD_OF_TIME = 18
    while (True):
        framerateChecker.check()
        original_img = theParameter.read()


        height, width, channels = original_img.shape
        tocrop = int((width - height) / 2)
        original_img = original_img[:, tocrop:-tocrop]
        ballsAndHands = gridModel.predict(original_img.copy())
        coordinates = []
        coordinates.extend(ballsAndHands["rhand"])
        coordinates.extend(ballsAndHands["lhand"])
        coordinates.extend(ballsAndHands["balls"].flatten())
        history.append(coordinates)
        if len(history) > 30:
            del history[0]
        else:
            continue

        pattern = np.array(history)
        pattern[:, ::2] = pattern[:, ::2] - np.mean(pattern[:, ::2])
        pattern[:, 1::2] = pattern[:, 1::2] - np.mean(pattern[:, 1::2])
        pattern = pattern / pattern.std()
        pattern = np.expand_dims(pattern, axis=0)
        pattern_activations = patternModel.predict(pattern)[0]

        img = np.zeros((256, 512 + 128, 3), dtype=np.uint8)
        '''for i in range(12):
            img[int(255 - pattern_activations[i] * 200):, 256 + i * 32:256 + i * 32 + 32, :] = 100'''

        font = cv2.FONT_HERSHEY_SIMPLEX
        img[:, :256, :] = cv2.resize(original_img, (256, 256), cv2.INTER_CUBIC)
        cv2.putText(img, names[np.argmax(pattern_activations)], (265, 30), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        trickAvgstore[np.argmax(pattern_activations)] += 1
        trickDetected = trickAvgstore.index(max(trickAvgstore))
        #cv2.putText(img, names[trickDetected], (300, 30), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        drawBallsAndHands(img, ballsAndHands)
        img = cv2.resize(img, (640 * 2 + 480, 768), cv2.INTER_CUBIC)

        cv2.imshow(prgmName, img)
        cv2.moveWindow(prgmName, 90, 125)
        #cv2.waitKey(1)
        ch = chr(0xFF & cv2.waitKey(1))

        if ch == 'q':
            print("mash is cool")
            break
        if time.time() > start + PERIOD_OF_TIME: break

    cv2.destroyAllWindows()

    img2 = np.zeros((256, 1024 + 128, 3), dtype=np.uint8)
    cv2.putText(img2, 'Trick Performed: '+ names[trickDetected], (50, 90), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img2, "(Press 'q' to close the window)", (90, 220), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow(prgmName, img2)
    cv2.moveWindow(prgmName, 300, 300)
    '''label = Tk.Label(None, text=names[trickDetected], font=('Times', '18'), fg='blue')
    label.pack()
    label.mainloop()'''
    while (True):
        ch = chr(0xFF & cv2.waitKey(0))
        if ch == 'q':
            break
    cv2.destroyAllWindows()


    '''trickDetected = max(trickAvgstore[:].index())
    cv2.putText(img, names[trickDetected], (265, 30), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    #cv2.imshow('Webcam', img)
    #cap.release()
    #cv2.destroyAllWindows()'''
