# import the necessary packages
import cv2
import numpy as np
from imutils.video import VideoStream
from PIL import Image
import copy

from mylib import config, epd4in2
from mylib.detector import Detector

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# cv2.startWindowThread()

# open webcam video stream
# cap = cv2.VideoCapture(0)
cap = VideoStream(config.url).start()

epd = epd4in2.EPD()
epd.init()
epd.Clear()

detector = Detector()

frame_init = None

# Capture frame-by-frame
frame = cap.read()
# resizing for faster detection
frame = cv2.resize(frame, (epd.width, epd.height))


while True:
    # Capture frame-by-frame
    frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (epd.width, epd.height))

    # Display the resulting frame
    frame_out = color_frame(frame)
    t = type(frame_init)
    if t is 'NoneType':
        print('frame_init', frame_init)
        frame_init = copy.copy(frame_out)
    print('eqals: ', frame_init is frame_out)
    frame_out = cv2.absdiff(frame_init, frame_out)
    frame_out_pil = Image.fromarray(frame_out)

    # if boxes:
    epd.display(epd.getbuffer(frame_out_pil))

    # cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)


""" # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
     """

""" boxes = detector.detect(frame)

    print(boxes)

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                      (0, 0, 0), 2) """
