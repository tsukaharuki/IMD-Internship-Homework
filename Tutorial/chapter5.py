import cv2
import numpy as np


img = cv2.imread("Resources/cards.jpg")

width,height = 250,350      #切り取った後表示する画像のサイズ
pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])        #cards.jpgにおけるスペードのキングの四つ角座標
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])      #
matrix = cv2.getPerspectiveTransform(pts1,pts2)         #斜め画像を真正面に投影する変換行列を取得
imgOutput = cv2.warpPerspective(img,matrix,(width,height))     #取得した変換行列を適用

cv2.imshow("Image",img)
cv2.imshow("Output",imgOutput)

cv2.waitKey(0)