import cv2
import numpy as np

image = cv2.imread('Project/Resources/input_img.png')

lower_white = np.array([200,200,200],dtype=np.uint8)
upper_white = np.array([255,255,255],dtype=np.uint8)

#Creating mask on white areas
mask = cv2.inRange(image, lower_white, upper_white)

mask_inv = cv2.bitwise_not(mask)

image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

image_rgba[:,:,3] = mask_inv

cv2.imwrite('Project/Resources/overlay_img.png', image_rgba)

cv2.imshow('Transparent Image', image_rgba)
cv2.waitKey(0)
cv2.destroyAllWindows()
