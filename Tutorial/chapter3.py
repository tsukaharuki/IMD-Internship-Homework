import cv2
import numpy as np
print("Package Imported")

img = cv2.imread("Resources/lambo.png")
print(img.shape)

imgResize = cv2.resize(img, (1000,500))
print(imgResize.shape)

imgCropped = img[100:600, 300:500]

cv2.imshow("Image", img)
cv2.imshow("Image Rsize", imgResize)
cv2.imshow("Image Cropped", imgCropped)
cv2.waitKey(0)
