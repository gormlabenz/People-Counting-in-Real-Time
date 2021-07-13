import logging
import time

import cv2
import imutils
from imutils.video import FPS, VideoStream
from PIL import Image

from mylib import config, epd4in2, thread

print("[INFO] Starting the live stream..")
vs = VideoStream(config.url).start()
time.sleep(2.0)
fps = FPS().start()

epd = epd4in2.EPD()
print('height:', epd.height, 'width:', epd.width)
logging.info("init and Clear")
epd.init()
epd.Clear()

time.sleep(1)

while True:
    print('frame…')
    frame = vs.read()
    frame = imutils.resize(frame, width=epd.width, height=epd.height)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_thres = cv2.adaptiveThreshold(
        img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    frame_out = cv2.cvtColor(frame_thres, cv2.COLOR_GRAY2BGR)

    frame_out_pil = Image.fromarray(frame_out)
    epd.display(epd.getbuffer(frame_out_pil))
