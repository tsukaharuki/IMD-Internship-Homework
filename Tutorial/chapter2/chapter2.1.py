import cv2
import numpy as np

img=cv2.imread("../Resources/VW2.png")
kernel=np.ones((5,5),np.uint8)

imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)        #cvtColorは色空間の変換を行うもの。(「変換する画像」,「変換後の色」)
imgBlur=cv2.GaussianBlur(imgGray,(7,7),0)      #ガウスフィルタ(GaussianBlur)をかける
imgCanny=cv2.Canny(img,100,100)         #cannyエッジ検出
imgDialation=cv2.dilate(imgCanny,kernel,iterations=1)     #膨張処理
imgErode=cv2.erode(imgDialation,kernel,iterations=1)

cv2.imshow("Gray Image",imgGray)        #imgGrayを「Gray Image」というデスクトップに表示する
cv2.imshow("Blur Image",imgBlur)        #imgBlurを「Blur Image」というデスクトップに表示する
cv2.imshow("Canny Image",imgCanny)
cv2.imshow("Dialation Image",imgDialation)
cv2.imshow("Eroded Image",imgErode)
cv2.waitKey(0)