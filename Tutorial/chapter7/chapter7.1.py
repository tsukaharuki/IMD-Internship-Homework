import cv2
from cv2 import COLOR_BGR2HSV

path='../Resources/VW2.png'
img=cv2.imread(path)

imgHSV=cv2.cvtColor(img,cv2,COLOR_BGR2HSV)      #BGRをHSVに変換

cv2.imshow("Original",img)
cv2.waitKey(0)