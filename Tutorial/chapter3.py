import cv2
import numpy as np

img = cv2.imread("Tutorial/Resources/lambo.png")
print(img.shape)

imgResize = cv2.resize(img,(300,200))

cv2.imshow("Image",img)
cv2.imshow("Image Resize", imgResize)

cv2.waitKey(0)