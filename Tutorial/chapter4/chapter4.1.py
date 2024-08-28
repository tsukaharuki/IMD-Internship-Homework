import cv2
import numpy as np

img=np.zeros((512,512,3),np.uint8)      #真っ黒のキャンパスを作るサイズは512*512
#print(img)
#img[200:300,100:300]=255,0,0        #任意の範囲を青(255,0,0)にする

cv2.line(img,(0,0),(img.shape[1],img.shape[0]),(0,255,0),1)       #線を描くファンクション
cv2.rectangle(img,(0,0),(250,250),(0,0,255),2)      #四角を描くファンクション
cv2.circle(img,(400,50),30,(255,255,0),2)       #円を描くファンクション
cv2.putText(img,"OPENCV",(300,200),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(0,150,0),1)

cv2.imshow("image",img)

cv2.waitKey(0)