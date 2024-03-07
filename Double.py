#### Importing Necessary Libraries

import datetime
import re
import cv2
import face_recognition
import numpy as np
import os

#### Defining Paths and Declaring Lists

path = 'CS-IV(Student)'
path2 = 'CS-IV(Teacher)'
images = []
classNames = []
myList = os.listdir(path)
myList2 = os.listdir(path2)
print('Retrieving Image Dataset...')

#### Splitting Path Names and Appends it to 'classNames' List

for cls in myList2:
    curImg1 = cv2.imread(f'{path2}/{cls}')
    images.append(curImg1)
    classNames.append(os.path.splitext(cls)[0])
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print('Splitting Paths...')

#### Defining Extract Features and Return 'encodeList' List

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
print("Encoding...")

encodeListKnown = findEncodings(images)
print('\nEncoding Complete, Starting Webcam')

imgPath = path
imgTPath = path2

#### Initializing 'writepath' and 'location' to a Filename to Store Attendance

writepath = 'StudentAttendance.csv'
location = 'TeacherAttendance.csv'

#### A Boolean Var Initialized To Know If The Attendance Is Already Marked or Not

check = False

#### Defining Method For Marking Attendance in 'StudentAttendance.csv' or in 'TeacherAttendance.csv'

def markAttendance(name):
    filenames = []
    for imgname in myList2:
        filename = re.search(r'(.+?)\.[^.]+$', imgname).group(1)
        filenames.append(filename)

    if name in filenames:
        with open(location, 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.datetime.now()
                date = datetime.date.today()
                dtString = now.strftime('%H:%M:%S')
                date_string = date.strftime('%d/%m/%Y')
                f.writelines(f'\n{name}, {imgTPath},{dtString},{date_string}')
                print('Attendance Marked Successfully!')
    else:
        with open(writepath, 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.datetime.now()
                date = datetime.date.today()
                dtString = now.strftime('%H:%M:%S')
                date_string = date.strftime('%d/%m/%Y')
                f.writelines(f'\n{name}, {imgPath},{dtString},{date_string}')
                print('Attendance Marked Successfully!!')

# Defining Method To Display If His/Her Attendance Is Marked in 'StudentAttendance.csv' or 'TeacherAttendance.csv' or Not

def checkAttendance(name):
    for imgname in myList2:
        filename = re.search(r'(.+?)\.[^.]+$', imgname).group(1)
        if filename == name:
            mode = 'r+' if os.path.exists(location) else 'a+'
            with open(location, mode) as f:
                if mode == 'a+':
                    f.write('Name,Class,Time,Date\n')
                myDataList = f.readlines()
                nameList = [entry.split(',')[0] for entry in myDataList]
                if name in nameList:
                    label = 'Attendance Marked'
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0))
                    cv2.putText(img, label, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            mode = 'r+' if os.path.exists(writepath) else 'a+'
            with open(writepath, mode) as f:
                if mode == 'a+':
                    f.write('Name,Class,Time,Date\n')
                myDataList = f.readlines()
                nameList = [entry.split(',')[0] for entry in myDataList]
                if name in nameList:
                    label = 'Attendance Marked'
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0))
                    cv2.putText(img, label, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#### Starting Capturing Image Frame By Frame

cap = cv2.VideoCapture(0)

#### Initializing 'countName' To Empty String To Count Frames For Each Individual

countName = ''

#### Initializing 'countName' To '1' For Initial Frame Captured

count = 1

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex]
            if name == countName:
                count = count + 1
            else:
                print('__________________')
                count = 1
            countName = name
            print(name, ' [', count, ']')

            for imgname in myList2:
                filename_without_extension = re.search(r'(.+?)\.[^.]+$', imgname).group(1)

                if filename_without_extension == name:
                    nameClass = name + " " + imgTPath
                    imgPath = imgTPath
                else:
                    nameClass = name + " " + imgPath


            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2), (x2, y2), (0, 255, 0), cv2.FILLED)

        #### If check remains "False" It will Mark the Attendance else it will not

        if check == False:
            checkAttendance(name)
        cv2.putText(img, nameClass, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        #### Marks Attendance If The Condition Satisfies To Avoid Bad Frame Occurrence

        if count > 6:
            markAttendance(name)
        ### Resetting ImgPath To Default
        imgPath = path

    #### Showing Result Window and Exit The Loop On Pressing 'x'

    cv2.imshow('Webcam, Scanning...', img)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

#### Release Video Capture

cap.release()
cv2.destroyAllWindows()
print('--Project Runs Smoothly!--')