import WebcamVideoStream
import FPS
import cv2
import thePatterndetectDemoFunction
import multiprocessing
import time
def maindetect(live):
    print("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream.WebcamVideoStream(src=0).start()
    fps = FPS.FPS().start()

    thePatterndetectDemoFunction.patterndetect(vs)

    vs.stop()
maindetect(1)