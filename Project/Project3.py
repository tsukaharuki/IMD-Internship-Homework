import cv2
import numpy as np

widthIMG = 640
heightIMG = 480
nplateCascade = cv2.CascadeClassifier("Tutorial/Resources/haarcascade_russian_plate_number.xml")
color = (255,0,255)
count = 0

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,150)

while True:
    success,img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    numberplates = nplateCascade.detectMultiScale(imgGray,1.1,4)
    for(x,y,w,h)in numberplates:
        area = w*h
        if area > 500:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(img,"NUMber Plate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,color,2)
            imgROi = img[y:y+h,x:x+w]
            cv2.imshow("ROI",imgROi)
    
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("Tutorial/Resources/Scanned/Noplate_"+str(count)+".jpg")
        cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(img,"Scan Saved",(150,265),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        cv2.imshow("Result",img)
        cv2.waitKey(500)
        count += 1