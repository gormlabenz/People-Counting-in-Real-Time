import cv2
import numpy as np

prototxt = "./mobilenet_ssd/MobileNetSSD_deploy.prototxt"
model = "./mobilenet_ssd/MobileNetSSD_deploy.caffemodel"
confidence_min = 0.4
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


class Detector:
    def __init__(self):
        self.net = cv2.dnn.readNetFromCaffe(prototxt, model)

    def detect(self, frame):
        H, W = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        boxes = []

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated
            # with the prediction
            confidence = detections[0, 0, i, 2]
            # filter out weak detections by requiring a minimum
            # confidence
            if confidence > confidence_min:
                # extract the index of the class label from the
                # detections list
                idx = int(detections[0, 0, i, 1])
                # if the class label is not a person, ignore it
                if CLASSES[idx] != "person":
                    continue
                # compute the (x, y)-coordinates of the bounding box
                # for the object
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                startX, startY, endX, endY = box.astype("int")
                boxes.append((startX, startY, endX, endY))

        return boxes
