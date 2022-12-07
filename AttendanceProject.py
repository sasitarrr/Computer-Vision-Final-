import cv2 as cv
import numpy as np
import face_recognition
import os
from datetime import datetime
from cvzone.SerialModule import SerialObject
from cvzone.FaceDetectionModule import FaceDetector

path = "TestImages"
images = []
testName = []
fileList = os.listdir(path)
print(fileList)
for cl in fileList:
    curImg = cv.imread(f'{path}/{cl}')
    images.append(curImg)
    testName.append(os.path.splitext(cl)[0])
print(testName)

def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncoding(images)
print("Encoding Complete")
def checkAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(",")
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f"{name},{dtString}\n")

cap = cv.VideoCapture(0)

arduino = SerialObject('/dev/cu.usbserial-1410')
detector = FaceDetector()

while True:
    success, img = cap.read()
    imgS = cv.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = testName[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv.rectangle(img, (x1, y1), (x2, y2), (204, 102, 0), 2)
            cv.rectangle(img, (x1, y2-35), (x2, y2), (204, 102, 0), cv.FILLED)
            cv.putText(img, name, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
            checkAttendance(name)

    imgS, bbox = detector.findFaces(imgS)
    if bbox:
        arduino.sendData([1])
    else:
        arduino.sendData([0])

    cv.imshow("webcam", img)
    cv.waitKey(1)
