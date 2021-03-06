import cv2
import objects
import pandas as pd
import make_json
import serial
# https://github.com/trane293/Palm-Fist-Gesture-Recognition - open_palm.xml
# https://github.com/Aravindlivewire/Opencv/tree/master/haarcascade - fist.xml
# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml - face.xml

x = objects.Item("empty", 0, 0, 0, 0)
objects.trash.append(x)

ser = serial.Serial('COM3', 500000)

centerx = 0
centery = 0

a = False

imcap = cv2.VideoCapture(0)
imcap.set(3, 640) # width = 640
imcap.set(4, 480) # height = 480

fistCascade = cv2.CascadeClassifier("fist.xml")
handCascade = cv2.CascadeClassifier("open_palm.xml")
faceCascade = cv2.CascadeClassifier("face.xml")

frame_number = 0
while True:
    frame_number += 1
    # captures image
    success, img = imcap.read() 
   
    # grayscales image
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plastic = fistCascade.detectMultiScale(imgGray, 1.5, 5)
    paper = handCascade.detectMultiScale(imgGray, 1.3, 5)
    garbage = faceCascade.detectMultiScale(imgGray, 1.5, 5)

    # puts boxes
    for (x, y, w, h) in paper: 
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        objects.AddTrash("paper", x, y, w, h)
        print("Paper detected")

    for (x, y, w, h) in plastic: 
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
        objects.AddTrash("plastic", x, y, w, h)
        print("Plastic detected")

    for (x, y, w, h) in garbage:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        objects.AddTrash("garbage", x, y, w, h)
        print("Garbage detected")

    objects.Sort()

    # displays image with boxes
    cv2.imshow('ObjectDetection', img)
    
    # f = open("datafile", "w")
    # f.write(str(objects.GetBin()))
    # f.close()
    print(frame_number)
    if frame_number % 50 == 0:
        if ser.isOpen() == False:
            ser = serial.Serial('COM3', 500000)
    if frame_number % 100 == 0:
        make_json.makeJSONatFrame(objects.GetTotals(), objects.GetBin())
        ser.write(objects.GetBin())
        ser.close()
    make_json.final_dataframe_list.append(objects.GetTotals() + [objects.GetBin()])

    # space key to close
    if cv2.waitKey(1) & 0xFF == ord('q'):
        make_json.makeFinalJSON(make_json.final_dataframe_list)
        break

imcap.release()
cv2.destroyAllWindows()