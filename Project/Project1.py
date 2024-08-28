import cv2
import numpy as np

framewidth = 640
frameheight = 480

cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,150)

myColors = [[5,107,0,19,255,255],[133,56,0,159,156,255],[57,76,0,100,255,255]]
mycolorvalues = [[51,153,255],[255,0,255],[0,255,0]]
myPoints = []

def findColor(img,myColors,mycolorvalues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newpoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getCounters(mask)
        if x != 0 and y != 0:
            newpoints.append([x,y,count])
        count += 1
        #cv2.imshow(str(color[0]),mask)
    return newpoints

def getCounters(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print(len(approx))
            objCor = len(approx)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

def DrawOnCanvas(myPoints,MyColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,mycolorvalues[point[2]],cv2.FILLED)

while True:
    success,img = cap.read()
    imgResult = img.copy()
    newpoints = findColor(img,myColors,mycolorvalues)
    if len(newpoints) != 0:
        for newP in newpoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        DrawOnCanvas(myPoints,mycolorvalues)
        
    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break