import cv2
import numpy as np

img = cv2.imread("Resources/mochi_moon.jpeg")
print(img.shape)
imgResize = cv2.resize(img, (400, 200))
print(imgResize.shape)
imgCropped = img[50:150, 46:216]

cv2.imshow("Futsu Moon", img)
cv2.imshow("Debu Moon", imgResize)
cv2.imshow("Moon Face", imgCropped)
cv2.waitKey(0)