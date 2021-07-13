import logging
import time

import cv2
import imutils
from PIL import Image, ImageDraw

from mylib import config, epd4in2, thread

epd = epd4in2.EPD()
print('height:', epd.height, 'width:', epd.width)
logging.info("init and Clear")
epd.init()
epd.Clear()

time.sleep(1)

while True:
    print('frame…')
    HRYimage = Image.new('1', (epd.width, epd.height), 255)
    drawblack = ImageDraw.Draw(HRYimage)
    drawblack.text((10, 0), 'hello world', fill=0)
    drawblack.text((10, 20), '4.2inch e-Paper bc', fill=0)
    drawblack.line((20, 50, 70, 100), fill=0)
    drawblack.line((70, 50, 20, 100), fill=0)
    drawblack.rectangle((20, 50, 70, 100), outline=0)
    epd.display(epd.getbuffer(HRYimage))
    time.sleep(2)
