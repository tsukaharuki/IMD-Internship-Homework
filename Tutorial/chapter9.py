import cv2

faceCascade= cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")     #OpenCVで顔検出をするために必要な物(haarcascade_frontalface_default.xml)
img = cv2.imread('Resources/lena.png')
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)      #グレイスケール

faces = faceCascade.detectMultiScale(imgGray,1.1,4)     #顔を検出する

for (x,y,w,h) in faces:     #顔の数だけループ
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)     #顔にBoudingBoxを作る


cv2.imshow("Result", img)
cv2.waitKey(0)