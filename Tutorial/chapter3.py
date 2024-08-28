import cv2
import numpy as np      #numpyライブラリをnpとしてインポート

img=cv2.imread("Resources/VW2.png")
print(img.shape)        #imgのサイズを表示する(縦,横,チャンネル数)

imgResize=cv2.resize(img,(1000,500))        #サイズ変更resize(「画像」,(横,縦))
print(imgResize.shape)

imgCropped=img[0:200,200:500]       #トリミング　「画像」[縦の範囲,横の範囲]

cv2.imshow("Image",img)
cv2.imshow("Image Resize",imgResize)
cv2.imshow("Image Cropped",imgCropped)
cv2.waitKey(0)