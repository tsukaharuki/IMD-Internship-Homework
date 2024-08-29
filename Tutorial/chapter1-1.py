import cv2

img = cv2.imread("Resources/mochi_moon.jpeg")

cv2.imshow("Moon", img)
cv2.waitKey(0)